from .GraphClass import Graph


class WorkflowRun(Graph):
    def __init__(self, tasks: dict):
        super().__init__(list(tasks.keys()))
        self.tasks = tasks
        self._setup()

    def _setup(self):
        for key, task in self.tasks.items():
            outputs = task.get("outputs", [])
            for sid in outputs:
                self.addEdge(key, sid)

    def find_task_by_type(self, task_type: str):
        for key, value in self.tasks.items():
            if value["type"] == task_type:
                return {"sid": key, "name": value.get("name"), "value": value}
        raise Exception("There are no starting points in workflow.")

    def find_task_by_id(self, sid: str) -> dict:
        return self.tasks.get(sid, None)

    def find_converging_tasks(self, sid: str) -> list:
        converging_tasks = []
        for key, task in self.tasks.items():
            outputs = task.get("outputs", [])
            if sid in outputs:
                converging_tasks.append(key)
        return converging_tasks
