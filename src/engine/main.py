from copy import deepcopy
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
        state, steps = StartEvent.peri(startTask["sid"], startTask["name"])

        self.state = state
        self.steps = steps

        return startTask["value"]

    def continue_from(self, workflow_id, run_id, state, steps, queue):
        self.workflow_id = workflow_id
        self.run_id = run_id
        self.state = state
        self.steps = steps
        self.queue = queue

    def get_next_steps_of(self, sid: str) -> list[dict]:
        # Create a list of task dictionaries
        listOfTasks = [
            stepTemplate(None, x, self.graph.tasks[x]["name"])
            for x in self.graph.BFS(sid)
        ]

        # Fetch the current task details
        current_task = self.graph.find_task_by_id(sid)

        # Conditions based on task type
        if current_task["type"] == EXCLUSIVE_GATEWAY:
            for task in listOfTasks:
                task["default"] = current_task.get("default_task_spec") == task["sid"]
            return [{"or": listOfTasks}]
        elif current_task["type"] == PARALLEL_GATEWAY:
            return listOfTasks
        else:
            return listOfTasks

    def add_to_queue(self, sid: str):
        queue = self.get_next_steps_of(sid)
        self.queue.extend(queue)

    def add_current_to_queue(self, sid: str):
        if sid not in [q.get("sid", "") for q in self.queue]:
            task = self.graph.find_task_by_id(sid)
            self.queue.extend([stepTemplate(None, sid, task["name"])])

    def set_step_completed(self, step: dict):
        step["completed"] = True
        step["finish"] = getDateTimeNow()

    def unset_step_completed(self, step: dict):
        step["completed"] = False
        step["finish"] = None

    def set_workflow_as_finished(self):
        self.state["completed"] = True
        self.state["success"] = True

    def append_workflow_state_data(self, data):
        self.state["data"].append(data)

    def decrease_step_number(self):
        self.state["step"] -= 1

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

            details = self.graph.find_task_by_id(task["sid"])
            if details["type"] not in [MANUAL_TASK, SCRIPT_TASK]:
                raise Exception("Action forbidden.")

            self.set_step_completed(task)
        else:
            _stepNumber = self.state["step"]
            self.set_step_completed(self.steps[_stepNumber])

            self.add_to_queue(self.steps[_stepNumber]["sid"])

    def revert_step(self, step_id: UUID):
        task = self.find_task_in_bucket_by_id(self.steps, step_id)
        details = self.graph.find_task_by_id(task["sid"])
        self.decrease_step_number()
        self.unset_step_completed(task)
        self.remove_from_bucket(self.steps, task["number"])
        self.remove_output_tasks_from_queue(details["outputs"])
        self.add_current_to_queue(task["sid"])

    def get_waiting_steps(self):
        if self.state["completed"]:
            return {
                "completed": self.state["completed"],
                "success": self.state["success"],
                "last_step": self.steps[self.state["step"]],
            }

        for current_task in self.steps:
            if "completed" not in current_task.keys() or not current_task.get(
                "completed"
            ):
                return pending_and_waiting_template(current_task, self.queue)

        # current_task = self.steps[self.state["step"]]
        if "completed" in current_task.keys() and current_task["completed"]:
            return {"queue": self.queue}

        return pending_and_waiting_template(current_task, self.queue)

    def check_if_current_step_completed(self) -> dict | None:
        current = self.steps[self.state["step"]]
        if "completed" not in current.keys() or not current["completed"]:
            return pending_and_waiting_template(current, self.queue)

        return None

    def remove_from_bucket(self, bucket: list[dict], index):
        del bucket[index]

    def remove_output_tasks_from_queue(self, listOfOutputTasks: list):
        idxs = []
        for index, task in enumerate(self.queue):
            if task["sid"] in listOfOutputTasks:
                idxs.append(index)

        for i in sorted(idxs, reverse=True):
            self.remove_from_bucket(self.queue, i)

    def count_waiting_steps_in_bucket(self, bucket: list[dict]):
        if isinstance(bucket, list):
            return len(bucket)
        return 0

    def get_incomplete_converging_tasks(self, sid):
        converging_tasks = self.graph.find_converging_tasks(sid)
        steps = deepcopy(self.steps)
        queue = deepcopy(self.queue)

        # Store the tasks that are not completed
        incomplete_tasks = []

        # Check if the sid exists in the steps list (indicating a circle)
        try:
            sid_index = next(i for i, task in enumerate(steps) if task["sid"] == sid)
        except StopIteration:
            sid_index = None

        # Check the steps list for incomplete converging tasks
        for task in steps[sid_index + 1 :] if sid_index is not None else steps:
            if task["sid"] in converging_tasks:
                # Check if the task is not completed
                if not task.get("completed", False):
                    incomplete_tasks.append(task["sid"])
                converging_tasks.remove(task["sid"])

        # Check the queue for converging tasks
        for task in queue:
            if task["sid"] in converging_tasks:
                incomplete_tasks.append(task["sid"])
                converging_tasks.remove(task["sid"])

        # If there are still converging tasks not found in either list, append them to the steps list
        for task_sid in converging_tasks:
            steps.append({"sid": task_sid, "completed": False})
            incomplete_tasks.append(task_sid)

        return incomplete_tasks

    def get_workflow_status(self) -> tuple[dict]:
        return self.state, self.steps, self.queue
