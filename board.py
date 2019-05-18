import copy
from random import getrandbits


class Board:
    def __init__(self, width, height, state=None):
        self.width = width
        self.height = height
        self.state = self._random_state(
            width, height) if state is None else state

    def render(self):
        state_string = " " + "=" * self.width + "\n"
        for y in range(0, self.height):
            state_string += "|" 
            for x in range(0, self.width):
                state_string += "@" if self.state[y][x] == 1 else " "
            state_string += "|\n"
        print(state_string)

    def next_board_state(self):
        new_state = copy.deepcopy(self.state)
        for y in range(0, self.height):
            for x in range(0, self.width):
                new_state[y][x] = self._next_cell_state(x, y)
        self.state = new_state

    @classmethod
    def load_state(cls, state):
        return cls(len(state[0]), len(state), state)

    def _next_cell_state(self, x, y):
        cell_state = self.state[y][x]
        if self.state[y][x] == 1:
            if self._living_neighbors(x, y) <= 1:
                cell_state = 0
            if self._living_neighbors(x, y) > 3:
                cell_state = 0
        else:
            if self._living_neighbors(x, y) == 3:
                cell_state = 1
        return cell_state

    def _living_neighbors(self, x, y):
        neighbors = list(filter(lambda n: n == 1, self._get_neighbors(x, y)))
        return len(neighbors)

    def _get_neighbors(self, x, y):
        neighbors = self.state[y][x-1:x] + self.state[y][x+1:x+2]
        try:
            neighbors += self.state[y-1][x-1:x+2]
        except:
            pass
        try:
            neighbors += self.state[y+1][x-1:x+2]
        except:
            pass
        return neighbors

    @staticmethod
    def _random_state(width, height):
        return [[getrandbits(1) for x in range(0, width)] for y in range(0, height)]
