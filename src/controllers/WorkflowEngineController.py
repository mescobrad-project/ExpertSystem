from uuid import UUID
from importlib.util import spec_from_file_location, module_from_spec
from src.engine.config import (
    SCRIPT_DIR,
    MANUAL_TASK,
    SCRIPT_TASK,
)
from src.engine.main import WorkflowEngine
from src.engine.classes.ElementClass import get_class_from_task_name
from src.engine.utils.TemplateUtils import pending_and_waiting_template, stepTemplate


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

        details = engine.graph.find_task_by_name(active["name"])
        element = get_class_from_task_name(details["type"])()
        actions = element.pre()

        if actions["complete"]:
            engine.set_step_completed(active)

        if actions["next_steps"]:
            engine.add_to_queue(active["name"])
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
            engine.add_to_queue(engine.graph.find_task_by_name(next_step["name"]))

        return next_step

    def execute_step_actions(self, tasks, state, steps, queue, actions, step_id: UUID):
        engine = self._continue_from(tasks, state, steps, queue)

        (_, active) = engine.find_active_step(engine.steps, step_id)

        details = engine.graph.find_task_by_name(active["name"])
        element = get_class_from_task_name(details["type"])()
        rules = element.post()

        # next_step = active
        if "choice" in rules.keys():
            if rules["choice"] == "one":
                index, next_step = engine.find_active_step(
                    engine.queue, actions["action"]
                )
                engine.set_step_completed(active)
                engine.add_to_queue(engine.graph.find_task_by_name(next_step["name"]))
                engine.set_task_as_active_step(next_step)
                engine.remove_from_bucket(engine.queue, index)
                active = next_step
            elif rules["choice"] == "all":
                self._set_waiting_task_as_active(engine, active, step_id)
            elif rules["choice"] == "wait_all":
                # check for previous steps completion
                waiting = self.get_not_completed_converging_tasks()

                if len(waiting) > 0:
                    return {
                        "display": "Please complete the following tasks first",
                        "waiting": waiting,
                    }

                self._set_waiting_task_as_active(engine, active, step_id)

        if "task" in rules.keys():
            if actions["choice"] == "exec":
                spec = spec_from_file_location(
                    "main", f"{SCRIPT_DIR}/{details['class']}.py"
                )
                script = module_from_spec(spec)
                spec.loader.exec_module(script)

                script.main()
            elif actions["choice"] == "complete":
                task = engine.find_task_in_bucket_by_id(engine.steps, step_id)

                if details["type"] not in [MANUAL_TASK, SCRIPT_TASK]:
                    raise Exception("Action forbidden.")

                engine.set_step_completed(task)
                (_, next_step) = engine.find_active_step(engine.queue)
                engine.set_task_as_active_step(next_step)
                engine.remove_from_bucket(
                    engine.queue,
                    engine.get_step_position_index(engine.queue, next_step["id"]),
                )

                active = next_step

        if "event" in rules.keys():
            if rules["complete"]:
                engine.set_step_completed(task)

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
