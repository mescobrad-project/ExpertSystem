from uuid import UUID
from src.engine.config import (
    RECEIVE_TASK,
    SEND_TASK,
    MANUAL_TASK,
    SCRIPT_TASK,
    USER_TASK,
)
from src.engine.main import WorkflowEngine
from src.engine.classes.ElementClass import get_class_from_task_name
from src.engine.utils.Generators import getId
from src.engine.utils.TemplateUtils import pending_and_waiting_template
from src.schemas.RequestBodySchema import TaskMetadataBodyParameter
from src.schemas.ExternalApiSchema import DataAnalyticsInput
from src.clients.artificialintelligence import client as ai_client
from src.clients.querybuilder import client as qb_client
from src.clients.dataanalytics import client as da_client
from src.models._all import RunModel


class BaseEngineController:
    def initialize(self, tasks):
        engine = WorkflowEngine(tasks)
        engine.initialize()
        engine.complete_step()
        state, steps, queue = engine.get_workflow_status()

        return state, steps, queue

    def _continue_from(self, workflow, run):
        engine = WorkflowEngine(workflow["tasks"])
        engine.continue_from(
            run["workflow_id"], run["id"], run["state"], run["steps"], run["queue"]
        )
        return engine

    def get_waiting_steps(self, workflow, run):
        engine = self._continue_from(workflow, run)
        return engine.get_waiting_steps()

    def run_pending_step(self, workflow, run, step_id: UUID):
        engine = self._continue_from(workflow, run)

        # check if current step is not completed
        # if not, then return current info
        current_step_completed = engine.check_if_current_step_completed()
        if current_step_completed is not None:
            return current_step_completed
        # else, check for next steps to display

        index, active = engine.find_active_step(engine.queue, step_id)

        details = engine.graph.find_task_by_id(active["sid"])
        element = get_class_from_task_name(details["type"])()
        actions = element.pre()

        if actions["complete"]:
            engine.set_step_completed(active)

        if actions["next_steps"]:
            engine.add_to_queue(active["sid"])
            engine.set_task_as_active_step(active)
            engine.remove_from_bucket(engine.queue, index)

        if actions.get("end_event") is not None and actions.get("end_event"):
            engine.set_task_as_active_step(active)
            engine.remove_from_bucket(engine.queue, index)

        return pending_and_waiting_template(active, engine.queue)

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

    def _prepare_step(self, workflow, run, step_id: UUID):
        engine = self._continue_from(workflow, run)

        (_, active) = engine.find_active_step(engine.steps, step_id)

        details = engine.graph.find_task_by_id(active["sid"])
        element = get_class_from_task_name(details["type"])()
        try:
            rules = (element.post(details))["rules"]
        except TypeError:
            rules = (element.post())["rules"]

        return (engine, active, details, rules)

    def gateway_exclusive_choice(
        self, workflow, run, step_id: UUID, next_step_id: UUID
    ):
        (engine, active, _, rules) = self._prepare_step(workflow, run, step_id)

        if "choice" in rules.keys() and rules["choice"] == "one":
            index, next_step = engine.find_active_step(engine.queue, next_step_id)
            engine.set_step_completed(active)
            engine.add_current_to_queue(next_step["sid"])
            engine.remove_from_bucket(engine.queue, index)
            active = next_step

        return {"pending": active}

    def gateway_parallel_choice(self, workflow, run, step_id: UUID, next_step_id: UUID):
        (engine, active, _, rules) = self._prepare_step(workflow, run, step_id)

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

    def task_exec(
        self,
        workflow,
        run,
        run_id: UUID,
        step_id: UUID,
        data: dict,
    ):
        (_, active, details, rules) = self._prepare_step(workflow, run, step_id)

        if "task" in rules.keys():
            if "metadata" in active.keys():
                return {"pending": active}

            for module_name in details["class"]:
                if module_name.startswith("dataanalytics"):
                    [_, func_name] = module_name.split("/")

                    if not da_client.check_if_function_exists(func_name):
                        return {"error": "Function name does not exist!"}

                    da_input = DataAnalyticsInput(
                        run_id=str(run_id),
                        step_id=step_id,
                        save_loc_bucket=data.get("save_bucket"),
                        save_loc_folder=data.get("save_folder"),
                        function=func_name,
                        metadata={"files": data.get("files")},
                    )

                    response = da_client.post(da_input)

                    if not response.get("is_success"):
                        return response

                    active["metadata"] = response
                elif module_name.startswith("querybuilder"):
                    active["metadata"] = {"url": da_client.redirect()}
                else:
                    return {"error": "Please provide a valid module!"}

        return {"pending": active}

    def task_send(
        self,
        workflow,
        run,
        step_id: UUID,
        data: dict,
    ):
        (engine, active, details, rules) = self._prepare_step(workflow, run, step_id)

        if "metadata" in rules.keys() and rules.get("metadata"):
            for ai_class in details["class"]:
                if not ai_client.router.check_if_route_is_available(ai_class):
                    continue

                for task in engine.queue:
                    if not task.get("sid") in details.get("outputs"):
                        continue

                    step_id_of_receive_task = task.get("id")
                    break

                instructions_response = ai_client.get_instructions_for_(ai_class)

                if not instructions_response.get("is_success"):
                    return instructions_response

                post_data_object = {}
                for key in instructions_response.get("key_name"):
                    if key == "workflow_id":
                        post_data_object[key] = str(engine.workflow_id)
                    elif key == "run_id":
                        post_data_object[key] = str(engine.run_id)
                    elif key == "step_id":
                        post_data_object[key] = step_id_of_receive_task
                    elif key == "data":
                        post_data_object[key] = data.get("data_input")
                    elif key == "user_input":
                        post_data_object[key] = data.get("user_input")
                    elif key == "params":
                        post_data_object[key] = data.get("params")

                response = ai_client.post_(ai_class, post_data_object)

                if not response.get("is_success"):
                    return response

                active["metadata"] = response

                engine.set_step_completed(active)

        return {"pending": active}

    def task_receive(
        self,
        workflow,
        run,
        step_id: UUID,
        data: dict,
    ):
        engine = self._continue_from(workflow, run)
        active = engine.find_task_in_bucket_by_id(engine.queue, str(step_id))
        details = engine.graph.find_task_by_id(active["sid"])
        element = get_class_from_task_name(details["type"])()
        try:
            rules = (element.post(details))["rules"]
        except TypeError:
            rules = (element.post())["rules"]

        if "metadata" in rules.keys() and rules.get("metadata"):
            active["metadata"] = data

        return {"pending": active}

    def task_complete(
        self,
        workflow,
        run,
        step_id: UUID,
        metadata: TaskMetadataBodyParameter | None = None,
    ):
        (engine, active, details, rules) = self._prepare_step(workflow, run, step_id)

        if "complete" in rules.keys():
            # task = engine.find_task_in_bucket_by_id(engine.steps, step_id)

            if details["type"] not in [
                MANUAL_TASK,
                SCRIPT_TASK,
                USER_TASK,
                RECEIVE_TASK,
            ]:
                raise Exception("Action forbidden.")

            task_stores = workflow["tasks"][active["sid"]].get("stores")
            print(active["sid"])
            print(task_stores)
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

                if active.get("metadata"):
                    active["metadata"]["store"] = {
                        "state_data_id": state_id,
                        "state_data_number": len(engine.state["data"]) - 1,
                    }
                else:
                    active["metadata"] = {
                        "store": {
                            "state_data_id": state_id,
                            "state_data_number": len(engine.state["data"]) - 1,
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

    def event_actions(self, workflow, run, step_id: UUID):
        (engine, active, _, rules) = self._prepare_step(workflow, run, step_id)

        if "event" in rules.keys():
            if rules["complete"]:
                engine.set_step_completed(active)
                active = {}

            if rules["finish"]:
                engine.set_workflow_as_finished()

        return {"pending": active}

    def task_revert(self, workflow, run, *, step_id: UUID):
        (engine, active, details, _) = self._prepare_step(workflow, run, step_id)

        if details["type"] not in [
            MANUAL_TASK,
            SCRIPT_TASK,
            USER_TASK,
            SEND_TASK,
            RECEIVE_TASK,
        ]:
            return {"pending": active}

        engine.revert_step(step_id)

        return {"pending": active}

    def ping_step_status(self, workflow, run, step_id: UUID):
        engine = self._continue_from(workflow, run)

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
