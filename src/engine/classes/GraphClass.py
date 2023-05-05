from collections import defaultdict


class Graph:
    def __init__(self, keys: list):
        self.keys = keys
        self.V = len(self.keys)
        self.graph = defaultdict(list)

    def addEdge(self, u, v):
        self.graph[u].append(v)  # Function to print a BFS of graph

    def BFS(self, s, max_depth=1):
        # Mark all the vertices as not visited
        visited = [False] * self.V

        # Create a queue for BFS
        queue = []

        # Mark the source node as
        # visited and enqueue it
        queue.append((s, 0))
        visited[self.keys.index(s)] = True

        next_queue = []

        while queue:
            # Dequeue a vertex from
            # queue and print it
            (s, level) = queue.pop(0)

            if level >= max_depth:
                break

            # Get all adjacent vertices of the
            # dequeued vertex s. If a adjacent
            # has not been visited, then mark it
            # visited and enqueue it
            for i in self.graph[s]:
                if visited[self.keys.index(i)] == False:
                    queue.append((i, level + 1))
                    next_queue.append(i)
                    visited[self.keys.index(i)] = True

        return next_queue

    def DFSUtil(self, u, color):
        # GRAY :  This vertex is being processed (DFS
        #         for this vertex has started, but not
        #         ended (or this vertex is in function
        #         call stack)
        color[self.keys.index(u)] = "GRAY"

        for v in self.graph[u]:
            if color[self.keys.index(v)] == "GRAY":
                return True

            if color[self.keys.index(v)] == "WHITE" and self.DFSUtil(v, color):
                return True

        color[self.keys.index(u)] = "BLACK"
        return False

    def isCyclic(self):
        color = ["WHITE"] * self.V

        for k in self.keys:
            if color[self.keys.index(k)] == "WHITE":
                if self.DFSUtil(k, color):
                    return True
        return False


# This code is contributed by Neelam Yadav
# This program is contributed by Divyanshu Mehta
