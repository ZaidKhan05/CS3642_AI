


import random
import copy
import heapq
import time

class Node:
    def __init__(self, board, parent, depth, cost, heuristic):
        self.board = board
        self.parent = parent
        self.depth = depth
        self.cost = cost
        self.heuristic = heuristic
        self.children = []
        self.blank = self.findBlank()

    def findBlank(self):
        for j in range(3):
            for k in range(3):
                if self.board[j][k] == 0:
                    return (j, k)

    def move(self, x, y):
        new_x, new_y = self.blank[0] + x, self.blank[1] + y
        if 0 <= new_x < 3 and 0 <= new_y < 3:
            newboard = copy.deepcopy(self.board)
            newboard[self.blank[0]][self.blank[1]], newboard[new_x][new_y] = newboard[new_x][new_y], newboard[self.blank[0]][self.blank[1]]
            return Node(newboard, self, self.depth + 1, self.cost + 1, 0)
        return None

    def generateChildren(self):
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for move in moves:
            child = self.move(*move)
            if child:
                self.children.append(child)

    def printBoard(self):
        for row in self.board:
            print(" ".join(map(str, row)))
        print()

    def printPath(self):
        path = []
        current = self
        while current:
            path.append(current)
            current = current.parent
        for node in reversed(path):
            node.printBoard()

    def __lt__(self, other):
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)

def manhattan_distance(board, goal):
    """ Heuristic function for Manhattan distance """
    distance = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] != 0:
                for x in range(3):
                    for y in range(3):
                        if board[i][j] == goal[x][y]:
                            distance += abs(i - x) + abs(j - y)
    return distance

def tiles_out_of_place(board, goal):
    """ Heuristic function for tiles out of place """
    count = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] != 0 and board[i][j] != goal[i][j]:
                count += 1
    return count

def search_algorithm(start_board, goal_board, search_type):
    root = Node(start_board, None, 0, 0, 0)
    nodes_visited = 0

    if search_type == 'dfs':
        stack = [root]
        visited = set()
        while stack:
            current = stack.pop()
            nodes_visited += 1
            if tuple(map(tuple, current.board)) == tuple(map(tuple, goal_board)):
                current.printPath()
                return True, nodes_visited
            visited.add(tuple(map(tuple, current.board)))
            current.generateChildren()
            for child in reversed(current.children):  # DFS: stack, reversed for correct order
                if tuple(map(tuple, child.board)) not in visited:
                    stack.append(child)
            if nodes_visited % 1000 == 0:
                print(f"Iteration: {nodes_visited}")
                current.printBoard()

    elif search_type == 'ucs':
        queue = [(root.cost, root)]
        visited = set()
        while queue:
            current_cost, current = heapq.heappop(queue)
            nodes_visited += 1
            if tuple(map(tuple, current.board)) == tuple(map(tuple, goal_board)):
                current.printPath()
                return True, nodes_visited
            visited.add(tuple(map(tuple, current.board)))
            current.generateChildren()
            for child in current.children:
                if tuple(map(tuple, child.board)) not in visited:
                    heapq.heappush(queue, (child.cost, child))
            if nodes_visited % 1000 == 0:
                print(f"Iteration: {nodes_visited}")
                current.printBoard()

    elif search_type == 'aStar':
        root.heuristic = tiles_out_of_place(root.board, goal_board)
        queue = [(root.cost + root.heuristic, root)]
        visited = set()
        while queue:
            _, current = heapq.heappop(queue)
            nodes_visited += 1
            if tuple(map(tuple, current.board)) == tuple(map(tuple, goal_board)):
                current.printPath()
                return True, nodes_visited
            visited.add(tuple(map(tuple, current.board)))
            current.generateChildren()
            for child in current.children:
                if tuple(map(tuple, child.board)) not in visited:
                    child.heuristic = tiles_out_of_place(child.board, goal_board)
                    heapq.heappush(queue, (child.cost + child.heuristic, child))
            if nodes_visited % 1000 == 0:
                print(f"Iteration: {nodes_visited}")
                current.printBoard()

    elif search_type == 'bfs':
        root.heuristic = manhattan_distance(root.board, goal_board)
        queue = [(root.cost + root.heuristic, root)]
        visited = set()
        while queue:
            _, current = heapq.heappop(queue)
            nodes_visited += 1
            if tuple(map(tuple, current.board)) == tuple(map(tuple, goal_board)):
                current.printPath()
                return True, nodes_visited
            visited.add(tuple(map(tuple, current.board)))
            current.generateChildren()
            for child in current.children:
                if tuple(map(tuple, child.board)) not in visited:
                    child.heuristic = manhattan_distance(child.board, goal_board)
                    heapq.heappush(queue, (child.cost + child.heuristic, child))
            if nodes_visited % 1000 == 0:
                print(f"Iteration: {nodes_visited}")
                current.printBoard()

    return False, nodes_visited

def createBoard():
    return [[9, 9, 9], [9, 9, 9], [9, 9, 9]]

def fillBoard(board):
    digits = list(range(9))
    random.shuffle(digits)
    idx = 0
    for j in range(3):
        for k in range(3):
            board[j][k] = digits[idx]
            idx += 1
    return board

def printBoard(board):
    for row in board:
        print(" ".join(map(str, row)))
    print()

def main():
    goal = [[1, 2, 3], [8, 0, 4], [7, 6, 5]]
    algorithm = int(input("Which algorithm do you want to use? \n1. Depth-First Search (DFS)\n2. Uniform-Cost Search (UCS)\n3. Best-First Search (BFS)\n4. A* Algorithm\n"))
    algo_map = {1: 'dfs', 2: 'ucs', 3: 'bfs', 4: 'aStar'}
    search_type = algo_map.get(algorithm)
    trials = int(input("How many trials do you want to run? \nthe trials will be run with random starting boards \nthe test will go until the desired amount of trials are successful\n"))
    successfulTrials = 0
    failedTrials = 0
    totalTrials = 0
    if search_type:
        results = []
        successfulResults = []
        
        while successfulTrials < trials:
            totalTrials += 1
            board = createBoard()
            board = fillBoard(board)
            print(f"Starting board: {totalTrials}")
            printBoard(board)
            print("Goal board:")
            printBoard(goal)
            start_time = time.time()
            reached_goal, nodes_visited = search_algorithm(board, goal, search_type)
            end_time = time.time()
            run_time = end_time - start_time
            results.append((nodes_visited, run_time))
            if not reached_goal:
                failedTrials += 1
            else:
                successfulResults.append((nodes_visited, run_time))
                successfulTrials += 1


        #data for all trials
        best_nodes = min(results, key=lambda x: x[0])[0]
        worst_nodes = max(results, key=lambda x: x[0])[0]
        avg_nodes = sum(result[0] for result in results) / trials

        best_time = min(results, key=lambda x: x[1])[1]
        worst_time = max(results, key=lambda x: x[1])[1]
        avg_time = sum(result[1] for result in results) / trials

        print(f"\n{search_type.upper()} Algorithm Results with {totalTrials} trials, {failedTrials} failed trials, {successfulTrials} successful trials:")
        print(f"Best number of nodes visited: {best_nodes}")
        print(f"Worst number of nodes visited: {worst_nodes}")
        print(f"Average number of nodes visited: {avg_nodes:.2f}")
        print(f"Best run time: {best_time:.4f} seconds")
        print(f"Worst run time: {worst_time:.4f} seconds")
        print(f"Average run time: {avg_time:.4f} seconds")

        #data for successful trials
        best_nodes = min(successfulResults, key=lambda x: x[0])[0]
        worst_nodes = max(successfulResults, key=lambda x: x[0])[0]
        avg_nodes = sum(successfulResults[0] for successfulResults in successfulResults) / successfulTrials

        best_time = min(successfulResults, key=lambda x: x[1])[1]
        worst_time = max(successfulResults, key=lambda x: x[1])[1]
        avg_time = sum(successfulResults[1] for successfulResults in successfulResults) / successfulTrials

        print(f"\n{search_type.upper()} Algorithm Results with {successfulTrials} successful trials(trials with boards that were valid):")
        print(f"Best number of nodes visited: {best_nodes}")
        print(f"Worst number of nodes visited: {worst_nodes}")
        print(f"Average number of nodes visited: {avg_nodes:.2f}")
        print(f"Best run time: {best_time:.4f} seconds")
        print(f"Worst run time: {worst_time:.4f} seconds")
        print(f"Average run time: {avg_time:.4f} seconds")
    else:
        print("Invalid input")
        return
main()
