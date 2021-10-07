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
        self.frontier = list() # ne štekam zdj če nismo dal parametra frontier v init

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
            self.frontier = self.frontier[:-1]  #update the frontier
            return node


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
            raise Exception("Msze must have exactly one goal.")

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
                except IndexError: #zhink about why would this happen
                    row.append(False)
            self.walls.append(row)
        self.solution = None

        def solve(self):
            """
            Finds a solution to maze, if one exists.
            :param self:
            :return:
            """

            # keep track of number of states explored
            self.num_explored = 0

            # initialize frontier to just the starting position
            start = Node(state=self.start, parent=None, action=None)
            frontier = StackFrontier()  # DFS uses a stack as its data structure
            frontier.add(start)

            # initialize an empty explored set
            self.explored = set()

            while True:
                if frontier.empty():
                    raise Exception("no solution")

                # choose a node from the frontier
                node = frontier.remove()
                self.num_explored += 1

                if node.state == self.goal:
                    actions = list()
                    cells = list()
                    while node.parent is not None:
                        actions.append(node.action)
                        cells.append(node.state)
                        node = node.parent
                    actions.reverse()
                    cells.reverse()
                    self.solution = (actions, cells)
                    return

                #mark node as explored
                self.explored.add(node.state)

                # add neighbors to frontier
                for action, state in self.neigbors(node.state):
                    if not frontier.contains_state(state) and state not in self.explored:
                        child = Node(state=state, parent=node, action=action)
                        frontier.add(child)




