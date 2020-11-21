import copy
import json
import os
import random

RULES = {
    # board size
    10: {
        # ship size : amount
        4: 1,
        3: 2,
        2: 3,
        1: 4
    },
    15: {
        6: 1,
        5: 1,
        4: 3,
        3: 3,
        2: 4,
        1: 5
    }
}


class Board:
    def __init__(self, board_size):
        if board_size not in RULES:
            raise AttributeError('Unsupported board size')

        self._board_size = board_size
        self._board = None

    @property
    def board_size(self):
        return self._board_size

    def generate(self):
        self._board = [
            [0 for _ in range(self._board_size)] for _ in range(self._board_size)
        ]
        for ship_size, ships_count in RULES[self._board_size].items():
            self._add_ship(ship_size, ships_count)
        return self

    def _add_ship(self, ship_size, ships_count):
        random.seed(os.urandom(128))

        for _ in range(ships_count):
            row, col, orientation = self._find_free_place(ship_size)
            if orientation == 'v':
                for i in range(ship_size):
                    self._board[row + i][col] = 1
            else:
                for i in range(ship_size):
                    self._board[row][col + i] = 1

    def _find_free_place(self, ship_size):
        orientations = ['v', 'h']
        random.shuffle(orientations)
        for orientation in orientations:
            for tries in range(10):
                if orientation == 'v':
                    start_row = random.randint(0, self._board_size - ship_size)
                    start_col = random.randint(0, self._board_size - 1)
                else:
                    start_row = random.randint(0, self._board_size - 1)
                    start_col = random.randint(0, self._board_size - ship_size)
                if tries == 9:
                    start_row = 0
                    start_col = 0

                for row in range(start_row, self._board_size):
                    for col in range(start_col, self._board_size):
                        if self._is_fit(row, col, ship_size, orientation):
                            return row, col, orientation

    def _is_fit(self, row, col, ship_size, orientation):
        if orientation == 'v':
            for cur_row in range(row - 1, row + ship_size + 1):
                # under
                if self._get_cell(cur_row, col) == 1:
                    return False
                # from left
                if self._get_cell(cur_row, col - 1) == 1:
                    return False
                # from right
                if self._get_cell(cur_row, col + 1) == 1:
                    return False
        else:
            for cur_col in range(col - 1, col + ship_size + 1):
                # under
                if self._get_cell(row, cur_col) == 1:
                    return False
                # from top
                if self._get_cell(row - 1, cur_col) == 1:
                    return False
                # from below
                if self._get_cell(row + 1, cur_col) == 1:
                    return False

        return True

    def _get_cell(self, row, col):
        if (0 <= row <= self._board_size - 1) \
            and (0 <= col <= self._board_size - 1):
            return self._board[row][col]
        return -1

    def to_json(self):
        return json.dumps(self._board)

    def to_list(self):
        return copy.deepcopy(self._board)

    @classmethod
    def load(cls, from_json):
        list_board = json.loads(from_json)
        board = cls(len(list_board))
        board._board = list_board
        return board

    def shot(self, x, y):
        if self._board[x][y] == 1:            
            return True
        return False
