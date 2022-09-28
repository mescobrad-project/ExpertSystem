from uuid import UUID
from importlib.util import spec_from_file_location, module_from_spec
from src.engine.config import (
    SCRIPT_DIR,
    MANUAL_TASK,
    SCRIPT_TASK,
)
from src.engine.main import WorkflowEngine
from src.engine.classes.ElementClass import get_class_from_task_name
from src.engine.utils.TemplateUtils import pending_and_waiting_template


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

        return pending_and_waiting_template(active, queue)

    def _set_waiting_task_as_active(self, engine, active, step_id):
        index, next_step = engine.find_active_step(engine.queue, step_id)
        engine.set_task_as_active_step(next_step, False)
        engine.remove_from_bucket(
            engine.queue[index]["and"],
            engine.get_step_position_index(engine.queue[index]["and"], next_step["id"]),
        )
        steps_waiting = engine.count_waiting_steps_in_bucket(engine.queue[index]["and"])

        if steps_waiting == 0:
            engine.set_step_completed(active)
            engine.update_step_number(active, True)
            engine.remove_from_bucket(engine.queue, index)
            engine.add_to_queue(next_step["sid"])

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
            engine.add_to_queue(next_step["sid"])
            engine.set_task_as_active_step(next_step)
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
                self._set_waiting_task_as_active(engine, active, next_step_id)
            elif rules["choice"] == "wait_all":
                # check for previous steps completion
                waiting = engine.get_not_completed_converging_tasks()

                if len(waiting) > 0:
                    return {
                        "display": "Please complete the following tasks first",
                        "waiting": waiting,
                    }

                self._set_waiting_task_as_active(engine, active, next_step_id)

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

    def task_complete(self, tasks, state, steps, queue, step_id: UUID):
        (engine, active, details, rules) = self._prepare_step(
            tasks, state, steps, queue, step_id
        )

        if "complete" in rules.keys():
            # task = engine.find_task_in_bucket_by_id(engine.steps, step_id)

            if details["type"] not in [MANUAL_TASK, SCRIPT_TASK]:
                raise Exception("Action forbidden.")

            engine.set_step_completed(active)

            if "task" in rules.keys():
                (_, next_step) = engine.find_active_step(engine.queue)
                engine.set_task_as_active_step(next_step)
                engine.remove_from_bucket(
                    engine.queue,
                    engine.get_step_position_index(engine.queue, next_step["id"]),
                )

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


WorkflowEngineController = BaseEngineController()
