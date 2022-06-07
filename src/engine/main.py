from uuid import UUID

from .config import START_EVENT
from .classes.WorkflowRunClass import WorkflowRun
from .elements import Element

# from .utils.IOClass import IO

# from .dependencies import WorkFlowEngine as WFE


# def test():
#     jsonf = IO.json_read("simple.json")
#     tasks = jsonf["task"]

#     # Driver program to test above functions

#     tasks_list = []
#     for index in tasks:
#         tasks_list.append(index)

#     g = Graph(tasks_list)
#     IO.byte_write("lol", "test.txt", file=g)

#     for index in tasks:
#         if "outputs" in tasks[index].keys():
#             for next_task in tasks[index]["outputs"]:
#                 g.addEdge(index, next_task)

#     print(
#         "Graph contains cycle"
#         if g.isCyclic() == True
#         else "Graph doesn't contain cycle"
#     )

#     print("Following is Breadth First Traversal" " (starting from vertex 2)")

#     print(g.BFS("strike_aborted"))

#     return {"success": True}


class WorkFlowEngine:
    graph: WorkflowRun

    def __init__(self, tasks: dict) -> None:
        self.graph = WorkflowRun(tasks)

    def initialize(self):
        startTask = self.graph.findTaskByType(START_EVENT)

        startEvent = Element(START_EVENT)(startTask["name"])

        state = startEvent["state"]
        step = startEvent["step"]

        print(
            "Graph contains cycle"
            if self.graph.isCyclic() == True
            else "Graph doesn't contain cycle"
        )
        print(startTask)
        print(self.graph.BFS("Start"))
        print(state)
        print(step)

        return startTask["value"]
