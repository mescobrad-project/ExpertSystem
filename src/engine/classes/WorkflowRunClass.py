from .GraphClass import Graph


class WorkflowRun(Graph):
    def __init__(self, tasks):
        super().__init__(list(tasks.keys()))

        self.tasks = tasks
        self._setup()

    def _setup(self):
        for key, task in self.tasks.items():
            if "outputs" in task.keys():
                for next_task in task["outputs"]:
                    self.addEdge(key, next_task)

    def find_task_by_type(self, task_type: str):
        obj = {"name": "", "value": {}}

        for key, value in self.tasks.items():
            if value["type"] == task_type:
                obj["name"] = key
                obj["value"] = value
                break
            else:
                raise Exception("There are no starting points in workflow.")

        return obj

    def find_task_by_name(self, task_name: str) -> dict:
        if task_name in self.tasks.keys():
            return self.tasks[task_name]

        raise Exception("Task not found")
