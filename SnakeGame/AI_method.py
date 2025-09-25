from collections import deque
import heapq

# BFS
def bfs(snake_head, food_coords, obstacles_list, snake, width, height):
    queue = deque([(snake_head, [])])
    visited = set()

    while queue:
        current, path = queue.popleft()

        if current == food_coords:
            return path

        if (
            current in visited
            or current[0] < 4
            or current[0] >= width
            or current[1] < 4
            or current[1] >= height
            or current in snake[1:]
            or current in obstacles_list
        ):
            continue

        visited.add(current)

        directions = [(0, -1), (0, 1), (1, 0), (-1, 0)]

        for direction in directions:
            neighbor = (current[0] + direction[0], current[1] + direction[1])
            queue.append((neighbor, path + [direction]))

    return None

# DFS
def dfs(snake_head, food_coords, obstacles_list, snake, width, height):

    stack = [(snake_head, [])]
    visited = set()

    while stack:
        current, path = stack.pop()



        if current == food_coords:
            return path

        if (
            current in visited
            or current[0] < 4
            or current[0] >= width
            or current[1] < 4
            or current[1] >= height
            or current in snake[1:]
            or current in obstacles_list
        ):
            continue

        visited.add(current)

        directions = [(0, -1), (0, 1), (1, 0), (-1, 0)]
        for direction in directions:
            neighbor = (current[0] + direction[0], current[1] + direction[1])
            stack.append((neighbor, path + [direction]))
    return None


def ID(snake_head, food_coords, obstacles_list, snake, width, height, max_depth):
    def depth_limited_search(initial_state, goal_state, depth_limit):
        stack = deque([(initial_state, [])])
        visited = set()

        while stack:
            current, path = stack.pop()

            if current == food_coords:
                return path

            if (
            current in visited
            or current[0] < 4
            or current[0] >= width
            or current[1] < 4
            or current[1] >= height
            or current in snake[1:]
            or current in obstacles_list
            ):
                continue

            visited.add(current)

            directions = [(0, -1), (0, 1), (1, 0), (-1, 0)]
            if len(path) < depth_limit:
                for direction in directions:
                    neighbor = (current[0] + direction[0], current[1] + direction[1])
                    stack.append((neighbor, path + [direction]))
        return None

    for depth_limit in range(max_depth):
        result = depth_limited_search(snake_head, food_coords, depth_limit)
        if result:
            return result

# UCS
def ucs(snake_head, food_coords, obstacles_list, snake, width, height):
    priority_queue = [(0, snake_head, [])]
    visited = set()

    while priority_queue:
        cost, current, path = heapq.heappop(priority_queue)

        if current == food_coords:
            return path

        if (
            current in visited
            or current[0] < 4
            or current[0] >= width
            or current[1] < 4
            or current[1] >= height
            or current in snake[1:]
            or current in obstacles_list
        ):
            continue

        visited.add(current)

        directions = [(0, -1), (0, 1), (1, 0), (-1, 0)]
        for direction in directions:
            neighbor = (current[0] + direction[0], current[1] + direction[1])
            new_cost = cost + 1  # Assuming each step has a cost of 1
            heapq.heappush(priority_queue, (new_cost, neighbor, path + [direction]))

    return None

# GREEDY
def greedy(snake_head, food_coords, obstacles_list, snake, width, height):
    heap = [(heuristic(snake_head, food_coords), snake_head, [])]
    visited = set()

    while heap:
        _, current, path = heapq.heappop(heap)

        if current == food_coords:
            return path

        if (
            current in visited
            or current[0] < 4
            or current[0] >= width
            or current[1] < 4
            or current[1] >= height
            or current in snake[1:]
            or current in obstacles_list
        ):
            continue

        visited.add(current)

        directions = [(0, -1), (0, 1), (1, 0), (-1, 0)]
        for direction in directions:
            neighbor = (current[0] + direction[0], current[1] + direction[1])
            heapq.heappush(heap, (heuristic(neighbor, food_coords), neighbor, path + [direction]))

    return None

def heuristic(point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

