from uuid import UUID

from .classes.ElementClass import get_class_from_task_name
from .config import (
    START_EVENT,
    EXCLUSIVE_GATEWAY,
    PARALLEL_GATEWAY,
    MANUAL_TASK,
    SCRIPT_TASK,
)
from .classes.WorkflowRunClass import WorkflowRun
from .utils.Generators import getDateTimeNow
from .utils.TemplateUtils import pending_and_waiting_template, stepTemplate


class WorkflowEngine:
    def __init__(self, tasks: dict) -> None:
        self.graph = WorkflowRun(tasks)
        self.state = {}
        self.steps = []
        self.queue = []

    def initialize(self):
        startTask = self.graph.find_task_by_type(START_EVENT)

        StartEvent = get_class_from_task_name(START_EVENT)()
        state, steps = StartEvent.peri(startTask["name"])

        self.state = state
        self.steps = steps

        return startTask["value"]

    def continue_from(self, state, steps, queue):
        self.state = state
        self.steps = steps
        self.queue = queue

    def get_next_steps_of(self, task_name: str) -> list[dict]:
        listOfTasks = list(
            map(lambda x: stepTemplate(None, x), self.graph.BFS(task_name))
        )
        current_task = self.graph.find_task_by_name(task_name)

        if current_task["type"] == EXCLUSIVE_GATEWAY:
            for task in listOfTasks:
                task["default"] = (
                    True if current_task["default_task_spec"] == task["name"] else False
                )
            return [{"or": listOfTasks}]
        elif current_task["type"] == PARALLEL_GATEWAY:
            return [{"and": listOfTasks}]
        else:
            return listOfTasks

    def add_to_queue(self, task_name: str):
        self.queue.extend(self.get_next_steps_of(task_name))

    def set_step_completed(self, step: dict):
        step["completed"] = True
        step["finish"] = getDateTimeNow()

    def set_workflow_as_finished(self):
        self.state["completed"] = True
        self.state["success"] = True

    def update_step_number(self, current: dict, update_state: bool = True):
        steps_len = len(self.steps)

        if update_state:
            self.state["step"] += 1
            if self.state["step"] < steps_len:
                self.state["step"] = steps_len - 1

            if not current["number"]:
                current["number"] = self.state["step"]
        else:
            current["number"] = steps_len

    def loop_through_bucket(
        self, bucket: list[dict], step_id: UUID | None, mode=None, func=None
    ) -> int | dict | None | tuple:
        for index, step in enumerate(bucket):
            if mode == "map":
                found = func(step_id=step_id, step=step)
                if found:
                    return index, found
            else:
                if step["id"] == step_id:
                    if mode == "index":
                        return index
                    else:
                        return step
        return None

    def find_task_in_bucket_by_id(self, bucket: list[dict], step_id: UUID):
        return self.loop_through_bucket(bucket, step_id)

    def find_active_step(self, bucket: list[dict], step_id: UUID = None) -> tuple:
        active = None

        def func(step_id, step, *args, **kwargs) -> dict | None:
            steps = []

            if "or" in step.keys():
                steps.extend(step["or"])
            elif "and" in step.keys():
                steps.extend(step["and"])
            else:
                steps.append(step)

            if step_id:
                for _, new_step in enumerate(steps):
                    if str(step_id) == new_step["id"]:
                        return new_step

            else:
                for _, step in enumerate(steps):
                    return step

            return None

        index, active = self.loop_through_bucket(bucket, step_id, "map", func)

        if not active:
            raise Exception("Step not found")

        return index, active

    def get_step_position_index(self, bucket: list[dict], step_id):
        return self.loop_through_bucket(bucket, step_id, "index")

    def set_task_as_active_step(self, current: dict, update_state: bool = True):
        self.update_step_number(current, update_state)

        self.steps.append(current)

    def complete_step(self, step_id: UUID | None = None):
        if step_id:
            task = self.find_task_in_bucket_by_id(self.steps, step_id)

            details = self.graph.find_task_by_name(task["name"])
            if details["type"] not in [MANUAL_TASK, SCRIPT_TASK]:
                raise Exception("Action forbidden.")

            self.set_step_completed(task)
        else:
            _stepNumber = self.state["step"]
            self.set_step_completed(self.steps[_stepNumber])

            self.add_to_queue(self.steps[_stepNumber]["name"])

    def get_waiting_steps(self):
        if self.state["completed"]:
            return {
                "completed": self.state["completed"],
                "success": self.state["success"],
                "last_step": self.steps[self.state["step"]],
            }

        current_task = self.steps[self.state["step"]]
        if "completed" in current_task.keys() and current_task["completed"]:
            return {"waiting": self.queue}

        return pending_and_waiting_template(current_task, self.queue)

    def check_if_current_step_completed(self) -> dict | None:
        current = self.steps[self.state["step"]]
        if "completed" not in current.keys() or not current["completed"]:
            return pending_and_waiting_template(current, self.queue)

        return None

    def remove_from_bucket(self, bucket: list[dict], index):
        del bucket[index]

    def count_waiting_steps_in_bucket(self, bucket: list[dict]):
        if isinstance(bucket, list):
            return len(bucket)
        return 0

    def get_not_completed_converging_tasks(self):
        response = []
        for step in reversed(self.queue[:-1]):
            details = self.graph.find_task_by_name(step["name"])
            if details["type"] == PARALLEL_GATEWAY:
                break

            if "completed" not in step.keys() or not step["completed"]:
                response.append(step)

        return response

    def get_workflow_status(self) -> tuple[dict]:
        return self.state, self.steps, self.queue
