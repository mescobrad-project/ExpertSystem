from collections import defaultdict
from json import loads


class Graph:
    def __init__(self, keys: list):
        self.keys = keys
        self.V = len(self.keys)
        self.graph = defaultdict(list)
        self.key_to_index = {key: idx for idx, key in enumerate(self.keys)}

    def addEdge(self, u, v):
        self.graph[u].append(v)

    def BFS(self, s, max_depth=1):
        visited = [False] * self.V
        queue = [(s, 0)]
        visited[self.key_to_index[s]] = True

        next_queue = []

        while queue:
            (s, level) = queue.pop(0)
            if level >= max_depth:
                break

            for i in self.graph[s]:
                if not visited[self.key_to_index[i]]:
                    queue.append((i, level + 1))
                    next_queue.append(i)
                    visited[self.key_to_index[i]] = True

        return next_queue

    def DFSUtil(self, u, color):
        color[u] = "GRAY"
        for v in self.graph[u]:
            if color[v] == "GRAY":
                return True
            if color[v] == "WHITE" and self.DFSUtil(v, color):
                return True
        color[u] = "BLACK"
        return False

    def isCyclic(self):
        color = {key: "WHITE" for key in self.keys}
        for k in self.keys:
            if color[k] == "WHITE" and self.DFSUtil(k, color):
                return True
        return False
