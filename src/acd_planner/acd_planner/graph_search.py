import heapq

def astar(start, goal, graph):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            return reconstruct(came_from, current)

        for n in graph[current]:
            came_from[n] = current
            heapq.heappush(open_set, (0, n))

