from uuid import UUID
from importlib.util import spec_from_file_location, module_from_spec
from src.engine.config import (
    SCRIPT_DIR,
    MANUAL_TASK,
    SCRIPT_TASK,
    USER_TASK,
)
from src.engine.main import WorkflowEngine
from src.engine.classes.ElementClass import get_class_from_task_name
from src.engine.utils.Generators import getId
from src.engine.utils.TemplateUtils import pending_and_waiting_template
from src.schemas.RequestBodySchema import TaskMetadataBodyParameter
from src.clients.artificialintelligence import client as ai_client
from src.models._all import RunModel


class BaseEngineController:
    def initialize(self, tasks):
        engine = WorkflowEngine(tasks)
        engine.initialize()
        engine.complete_step()
        state, steps, queue = engine.get_workflow_status()

        return state, steps, queue

    def _continue_from(self, tasks, state, steps, queue):
        engine = WorkflowEngine(tasks)
        engine.continue_from(state, steps, queue)
        return engine

    def get_waiting_steps(self, tasks, state, steps, queue):
        engine = self._continue_from(tasks, state, steps, queue)
        return engine.get_waiting_steps()

    def run_pending_step(self, tasks, state, steps, queue, step_id: UUID):
        engine = self._continue_from(tasks, state, steps, queue)

        # check if current step is not completed
        # if not, then return current info
        current_step_completed = engine.check_if_current_step_completed()
        if current_step_completed is not None:
            return current_step_completed
        # else, check for next steps to display

        index, active = engine.find_active_step(queue, step_id)

        details = engine.graph.find_task_by_id(active["sid"])
        element = get_class_from_task_name(details["type"])()
        actions = element.pre()

        if actions["complete"]:
            engine.set_step_completed(active)

        if actions["next_steps"]:
            engine.add_to_queue(active["sid"])
            engine.set_task_as_active_step(active)
            engine.remove_from_bucket(queue, index)

        if actions.get("end_event") is not None and actions.get("end_event"):
            engine.set_task_as_active_step(active)
            engine.remove_from_bucket(queue, index)

        return pending_and_waiting_template(active, queue)

    def _set_parallelqueue_task_to_queue(self, engine, active, step_id):
        index, next_step = engine.find_active_step(engine.queue, step_id)
        engine.add_current_to_queue(next_step["sid"])
        engine.remove_from_bucket(
            engine.queue[index]["and"],
            engine.get_step_position_index(engine.queue[index]["and"], next_step["id"]),
        )
        steps_waiting = engine.count_waiting_steps_in_bucket(engine.queue[index]["and"])

        if steps_waiting == 0:
            engine.set_step_completed(active)
            engine.remove_from_bucket(engine.queue, index)

        return next_step

    def _prepare_step(self, tasks, state, steps, queue, step_id: UUID):
        engine = self._continue_from(tasks, state, steps, queue)

        (_, active) = engine.find_active_step(engine.steps, step_id)

        details = engine.graph.find_task_by_id(active["sid"])
        element = get_class_from_task_name(details["type"])()
        try:
            rules = (element.post(details))["rules"]
        except TypeError:
            rules = (element.post())["rules"]

        return (engine, active, details, rules)

    def gateway_exclusive_choice(
        self, tasks, state, steps, queue, step_id: UUID, next_step_id: UUID
    ):
        (engine, active, _, rules) = self._prepare_step(
            tasks, state, steps, queue, step_id
        )

        if "choice" in rules.keys() and rules["choice"] == "one":
            index, next_step = engine.find_active_step(engine.queue, next_step_id)
            engine.set_step_completed(active)
            engine.add_current_to_queue(next_step["sid"])
            engine.remove_from_bucket(engine.queue, index)
            active = next_step

        return {"pending": active}

    def gateway_parallel_choice(
        self, tasks, state, steps, queue, step_id: UUID, next_step_id: UUID
    ):
        (engine, active, _, rules) = self._prepare_step(
            tasks, state, steps, queue, step_id
        )

        if "choice" in rules.keys():
            if rules["choice"] == "all":
                self._set_parallelqueue_task_to_queue(engine, active, next_step_id)
            elif rules["choice"] == "wait_all":
                # check for previous steps completion
                waiting = engine.get_not_completed_converging_tasks()

                if len(waiting) > 0:
                    return {
                        "display": "Please complete the following tasks first",
                        "queue": waiting,
                    }

                self._set_parallelqueue_task_to_queue(engine, active, next_step_id)

        return {"pending": active}

    def task_exec(self, tasks, state, steps, queue, step_id: UUID):
        (_, active, details, rules) = self._prepare_step(
            tasks, state, steps, queue, step_id
        )

        if "task" in rules.keys():
            active["data"] = []

            for script_file_name in details["class"]:
                spec = spec_from_file_location(
                    "main", f"{SCRIPT_DIR}/{script_file_name}.py"
                )
                script = module_from_spec(spec)
                spec.loader.exec_module(script)

                active["data"].append(script.main())

        return {"pending": active}

    def task_send(self, tasks, state, steps, queue, step_id: UUID, data: list[dict]):
        (_, active, details, rules) = self._prepare_step(
            tasks, state, steps, queue, step_id
        )

        if "store" in rules.keys():
            active["data"] = []

            for ai_class in details["class"]:
                # call api and show response
                # on success complete
                # on then get next and use as step_id
                ai_client.post_algo(
                    {
                        "workflow_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "run_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "step_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    }
                )
                pass

        return {"pending": active}

    def task_complete(
        self,
        tasks,
        state,
        steps,
        queue,
        step_id: UUID,
        metadata: TaskMetadataBodyParameter | None = None,
    ):
        (engine, active, details, rules) = self._prepare_step(
            tasks, state, steps, queue, step_id
        )

        if "complete" in rules.keys():
            # task = engine.find_task_in_bucket_by_id(engine.steps, step_id)

            if details["type"] not in [MANUAL_TASK, SCRIPT_TASK, USER_TASK]:
                raise Exception("Action forbidden.")

            task_stores = tasks[active["sid"]].get("stores")
            if task_stores and len(task_stores) > 0:
                to_store = {}

                ### Start Bad Code
                for store in task_stores:
                    sid = list(store.keys())[0]
                    mode = store[sid].get("mode")

                    if metadata.error:
                        to_store["error"] = metadata.error
                    elif metadata.store.get(sid):
                        if mode not in ["set", "get"]:
                            continue

                        data = {}
                        data[mode] = metadata.store.get(sid).get(mode)

                        # deserialize data because of python's/pydantic's poor handling
                        deserialized = []
                        for raw_data in data[mode]:
                            deserialized.append(raw_data.dict())

                        to_store[sid] = {}
                        to_store[sid][mode] = deserialized
                ### End Bad Code

                state_id = getId()

                engine.append_workflow_state_data(
                    {
                        "id": state_id,
                        "sid": active["sid"],
                        "step_number": active["number"],
                        "data": to_store,
                    }
                )

                active["metadata"] = {
                    "data": {
                        "state_data_id": state_id,
                        "state_data_number": len(state["data"]) - 1,
                    }
                }

            engine.set_step_completed(active)

            # if "task" in rules.keys():
            #     (_, next_step) = engine.find_active_step(engine.queue)
            #     engine.set_task_as_active_step(next_step)
            #     engine.remove_from_bucket(
            #         engine.queue,
            #         engine.get_step_position_index(engine.queue, next_step["id"]),
            #     )

        return {"pending": active}

    def event_actions(self, tasks, state, steps, queue, step_id: UUID):
        (engine, active, _, rules) = self._prepare_step(
            tasks, state, steps, queue, step_id
        )

        if "event" in rules.keys():
            if rules["complete"]:
                engine.set_step_completed(active)
                active = {}

            if rules["finish"]:
                engine.set_workflow_as_finished()

        return {"pending": active}

    def ping_step_status(self, tasks, state, steps, queue, step_id: UUID):
        engine = self._continue_from(tasks, state, steps, queue)

        (_, active) = engine.find_active_step(engine.steps, step_id)

        if "completed" not in active.keys():
            active["completed"] = False

        return {"step": active, "completed": active["completed"]}

    def get_dataobject_refs(self, run: RunModel):
        file_refs = []

        for activity in run.state["data"]:
            for sid, data in activity["data"].items():
                if sid in run.workflow.stores.keys():
                    if run.workflow.stores[sid]["type"] == "DataObject":
                        if "get" in data.keys():
                            file_refs.extend(data["get"])
                        if "set" in data.keys():
                            file_refs.extend(data["set"])

        return file_refs


WorkflowEngineController = BaseEngineController()
