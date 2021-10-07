import sys

"""
Implementation of maze solving.
"""


class Node():
    """
    Class that is keeping track of the state, the parent and the action.
    We are not keeping track of the path cost because we can calculate the cost of the path
    at the end after we found our way from the initial state to the goal.
    """
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


class StackFrontier():
    """
    Implemets the idea of a frontier. A way to add and remove a node to/from a frontier. (remove as a stack)
    Implementing this frontier as a stack - a last in first out data structure.
    Why we chose object? an object to store all of my Frontier data.
    """
    def __init__(self):
        """
        Function that initially creates a frontier that is represented by an empty list.
        """
        self.frontier = list()  # ne stekam zdj ce nismo dal parametra frontier v init

    def add(self, node):
        """
        Adds a node to the frontier, by appending it to the end of the list.
        :param node:
        :return:
        """
        self.frontier.append(node)

    def empty(self):
        """
        Checks if frontier is emtpy.
        :return: True if it is empty. False otherwise.
        """
        return len(self.frontier) == 0

    def remove(self):
        """
        Remove a node from the frontier. Includes a safety net for the case of empty frontier.
        :return: node that we have removed
        """
        if self.empty():
            raise Exception("Empty frontier.")
        else:
            node = self.frontier[-1]  # stack frontier
            self.frontier = self.frontier[:-1]  # update the frontier
            return node

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)


class QueueFrontier(StackFrontier):
    """
    Inherits from a stack frontier - meaning it is going to do all the same things that
    the stack frontier did, except the way we remove a node from the frontier is going to be different.
    Removes from the beginning of the list, like a queue, first in first out.
    """

    def remove(self):
        """
        Removes a node from the beginning of the list.
        :return: The removed node
        """
        if self.empty():
            raise Exception("empty frontier.")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:] #updates the frontier
            return node


class Maze:
    """
    This is going to handle the process od taking a sequence, a maze like text file,
    and figuring out how to solve it.
    # - represents a wall
    A - starting positiom
    B - ending position
    """
    # code for parsing the text file
    def __init__(self, filename):

        # read file and set height and width of maze
        with open(filename) as f:
            contents = f.read()

        # validate start and goal
        if contents.count("A") != 1:
            raise Exception("Maze must have exactly one start point.")
        if contents.count("B") != 1:
            raise Exception("Maze must have exactly one goal.")

        # determine the height and width of the maze
        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        # keep track of the walls
        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == 'A':
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == 'B':
                        self.goal = (i, j)
                        row.append(False)
                    elif contents[i][j] == ' ':
                        row.append(False)
                    else:
                        # we have hit a wall
                        row.append(True)
                except IndexError:  # think about why would this happen
                    row.append(False)
            self.walls.append(row)
        self.solution = None

    def neighbors(self, state):
        row, col = state
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]
        result = []
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r, c)))
            return result

    def solve(self):
        """
        Finds a solution to maze, if one exists.
        :param self:
        :return:
        """

        # keep track of number of states explored
        self.num_explored = 0  # why is this not in __init__ ???

        # initialize frontier to just the starting position
        start = Node(state=self.start, parent=None, action=None)
        frontier = StackFrontier()  # DFS uses a stack as its data structure
        frontier.add(start)  # initially this frontier just contains the start state

        # initialize an empty explored set
        self.explored = set()  # why is this not in __init__ ???

        while True:
            if frontier.empty():
                raise Exception("no solution")

            # choose a node from the frontier
            node = frontier.remove()
            self.num_explored += 1

            if node.state == self.goal:
                # if it is the goal, then we backtrack our way to figure out
                # what actions we took in order to get to this goal
                actions = list()
                cells = list()

                # follow parent nodes to find solution
                while node.parent is not None: # loop until initial state, where there is no parent
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent

                # reverse it to get the sequence of actions from the initial state to the goal
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return

            # if it is not the goal just mark node as explored
            self.explored.add(node.state)

            # add neighbors to frontier
            for action, state in self.neighbors(node.state):
                # for each neighbor check, is the state already in the frontier?
                # is the state already in the explored set?
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)

    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("█", end="")
                elif (i, j) == self.start:
                    print("A", end="")
                elif (i, j) == self.goal:
                    print("B", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()

    def output_image(self, filename, show_solution=True, show_explored=False):
        from PIL import Image, ImageDraw
        cell_size = 50
        cell_border = 2

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.width * cell_size, self.height * cell_size),
            "black"
        )
        draw = ImageDraw.Draw(img)

        solution = self.solution[1] if self.solution is not None else None
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):

                # Walls
                if col:
                    fill = (40, 40, 40)

                # Start
                elif (i, j) == self.start:
                    fill = (255, 0, 0)

                # Goal
                elif (i, j) == self.goal:
                    fill = (0, 171, 28)

                # Solution
                elif solution is not None and show_solution and (i, j) in solution:
                    fill = (220, 235, 113)

                # Explored
                elif solution is not None and show_explored and (i, j) in self.explored:
                    fill = (212, 97, 85)

                # Empty cell
                else:
                    fill = (237, 240, 252)

                # Draw cell
                draw.rectangle(
                    ([(j * cell_size + cell_border, i * cell_size + cell_border),
                      ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                    fill=fill
                )

        img.save(filename)


if len(sys.argv) != 2:
    sys.exit("Usage: python maze.py maze.txt")

m = Maze(sys.argv[1])
print("Maze:")
m.print()
print("Solving...")
m.solve()
print("States Explored:", m.num_explored)
print("Solution:")
m.print()

