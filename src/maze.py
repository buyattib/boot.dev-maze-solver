import time
import random

from window import Window
from cell import Cell


class Maze:
    def __init__(
        self,
        x1: float,
        y1: float,
        num_rows: int,
        num_cols: int,
        cell_size_x: float,
        cell_size_y: float,
        win: Window | None = None,
        seed: int | None = None,
    ):
        self._win = win

        self._cells: list[list[Cell]] = []
        self._x1 = x1
        self._y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y

        if seed:
            random.seed(seed)

        print("Creating board with cells")
        self._create_cells()
        time.sleep(0.5)

        print("Create entrance and exit")
        self._break_entrance_and_exit()
        time.sleep(0.5)

        print("Create maze")
        self._break_walls_r(0, 0)
        time.sleep(0.5)

        self._reset_cells_visited()

        print("Start solving")
        time.sleep(0.5)

    def _create_cells(self):
        for _ in range(self.num_cols):
            col = [Cell(self._win) for _ in range(self.num_rows)]
            self._cells.append(col)

        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i: int, j: int):
        if self._win is None:
            return

        x1 = self._x1 + i * self.cell_size_x
        y1 = self._y1 + j * self.cell_size_y
        x2 = self._x1 + (i + 1) * self.cell_size_x
        y2 = self._y1 + (j + 1) * self.cell_size_y

        cell = self._cells[i][j]
        cell.draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self):
        entrance_cell = self._cells[0][0]
        exit_cell = self._cells[-1][-1]

        entrance_cell.has_top_wall = False
        self._draw_cell(0, 0)
        exit_cell.has_bottom_wall = False
        self._draw_cell(self.num_cols - 1, self.num_rows - 1)

    def _break_walls_r(self, i: int, j: int):
        current_cell = self._cells[i][j]
        current_cell.visited = True

        while True:
            possible_directions = []

            if (i - 1) >= 0:
                adj_cell = self._cells[i - 1][j]
                if not adj_cell.visited:
                    possible_directions.append((i - 1, j))
            if (i + 1) < self.num_cols:
                adj_cell = self._cells[i + 1][j]
                if not adj_cell.visited:
                    possible_directions.append((i + 1, j))
            if (j - 1) >= 0:
                adj_cell = self._cells[i][j - 1]
                if not adj_cell.visited:
                    possible_directions.append((i, j - 1))
            if (j + 1) < self.num_rows:
                adj_cell = self._cells[i][j + 1]
                if not adj_cell.visited:
                    possible_directions.append((i, j + 1))

            if len(possible_directions) == 0:
                self._draw_cell(i, j)
                return

            direction = random.randrange(0, len(possible_directions))
            n_i, n_j = possible_directions[direction]
            next_cell = self._cells[n_i][n_j]

            if n_i == i and n_j < j:
                current_cell.has_top_wall = False
                next_cell.has_bottom_wall = False
            elif n_i == i and n_j > j:
                current_cell.has_bottom_wall = False
                next_cell.has_top_wall = False
            elif n_j == j and n_i < i:
                current_cell.has_left_wall = False
                next_cell.has_right_wall = False
            elif n_j == j and n_i > i:
                current_cell.has_right_wall = False
                next_cell.has_left_wall = False

            self._draw_cell(i, j)
            self._draw_cell(n_i, n_j)

            self._break_walls_r(n_i, n_j)

    def _reset_cells_visited(self):
        for col in self._cells:
            for cell in col:
                cell.visited = False

    def _solve_r(self, i: int, j: int):
        self._animate()

        current_cell = self._cells[i][j]
        current_cell.visited = True
        if i == self.num_cols - 1 and j == self.num_rows - 1:
            return True

        # left
        if i - 1 >= 0 and not current_cell.has_left_wall:
            next_cell = self._cells[i - 1][j]
            if not next_cell.visited and not next_cell.has_right_wall:
                current_cell.draw_move(next_cell)
                result = self._solve_r(i - 1, j)
                if result:
                    return True
                else:
                    current_cell.draw_move(next_cell, undo=True)

        # right
        if i + 1 < self.num_cols and not current_cell.has_right_wall:
            next_cell = self._cells[i + 1][j]
            if not next_cell.visited and not next_cell.has_left_wall:
                current_cell.draw_move(next_cell)
                result = self._solve_r(i + 1, j)
                if result:
                    return True
                else:
                    current_cell.draw_move(next_cell, undo=True)

        # up
        if j - 1 >= 0 and not current_cell.has_top_wall:
            next_cell = self._cells[i][j - 1]
            if not next_cell.visited and not next_cell.has_bottom_wall:
                current_cell.draw_move(next_cell)
                result = self._solve_r(i, j - 1)
                if result:
                    return True
                else:
                    current_cell.draw_move(next_cell, undo=True)

        # down
        if j + 1 < self.num_rows and not current_cell.has_bottom_wall:
            next_cell = self._cells[i][j + 1]
            if not next_cell.visited and not next_cell.has_top_wall:
                current_cell.draw_move(next_cell)
                result = self._solve_r(i, j + 1)
                if result:
                    return True
                else:
                    current_cell.draw_move(next_cell, undo=True)

        return False

    def solve(self):
        result = self._solve_r(0, 0)
        return result
