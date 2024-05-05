from window import Point, Line, Window


class Cell:
    def __init__(
        self,
        win: Window | None = None,
    ):
        self._win = win
        self.visited = False

        self.has_left_wall: bool = True
        self.has_right_wall: bool = True
        self.has_top_wall: bool = True
        self.has_bottom_wall: bool = True
        self._x1: float | None = None
        self._x2: float | None = None
        self._y1: float | None = None
        self._y2: float | None = None

    def get_cell_width(self):
        if not self._x2 or not self._x1:
            raise Exception("Cell coordinates not defined")
        return self._x2 - self._x1

    def get_cell_height(self):
        if not self._y2 or not self._y1:
            raise Exception("Cell coordinates not defined")
        return self._y2 - self._y1

    def draw(self, x1: float, y1: float, x2: float, y2: float):
        if not self._win:
            return

        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2

        p1 = Point(x1, y1)
        p2 = Point(x1, y2)
        line = Line(p1, p2)
        if self.has_left_wall:
            self._win.draw_line(line)
        else:
            self._win.draw_line(line, fill_color="white")

        p1 = Point(x2, y1)
        p2 = Point(x2, y2)
        line = Line(p1, p2)
        if self.has_right_wall:
            self._win.draw_line(line)
        else:
            self._win.draw_line(line, fill_color="white")

        p1 = Point(x1, y2)
        p2 = Point(x2, y2)
        line = Line(p1, p2)
        if self.has_bottom_wall:
            self._win.draw_line(line)
        else:
            self._win.draw_line(line, fill_color="white")

        p1 = Point(x1, y1)
        p2 = Point(x2, y1)
        line = Line(p1, p2)
        if self.has_top_wall:
            self._win.draw_line(line)
        else:
            self._win.draw_line(line, fill_color="white")

    def draw_move(self, to_cell: "Cell", undo: bool = False):
        self_center = None
        to_center = None

        if not (self._x1 and self._x2 and self._y1 and self._y2):
            raise Exception("Coordinates of cell not defined")
        if not (to_cell._x1 and to_cell._x2 and to_cell._y1 and to_cell._y2):
            raise Exception("Coordinates of cell not defined")

        self_center = Point(
            self._x2 - self.get_cell_width() / 2, self._y2 - self.get_cell_height() / 2
        )
        to_center = Point(
            to_cell._x2 - to_cell.get_cell_width() / 2,
            to_cell._y2 - to_cell.get_cell_height() / 2,
        )

        line = Line(self_center, to_center)
        color = "red" if not undo else "gray"
        self._win.draw_line(line, fill_color=color)
