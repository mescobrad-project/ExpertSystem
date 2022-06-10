from ..classes.GraphClass import Graph
from ..config import START_EVENT


class TaskUtils:
    @staticmethod
    def findStart(graph: Graph, tasks: dict):
        start = {"name": "", "value": {}}

        for key, value in tasks.items():
            if value["type"] == START_EVENT:
                start["name"] = key
                start["value"] = value
                break
            else:
                raise Exception("There are no starting points in workflow.")

        return start
