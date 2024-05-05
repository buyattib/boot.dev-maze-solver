from tkinter import Tk, BOTH, Canvas


class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Point({self.x}, {self.y})"


class Line:
    def __init__(self, point1: Point, point2: Point):
        self.point1 = point1
        self.point2 = point2

    def draw(self, canvas: Canvas, fill_color: str):
        canvas.create_line(
            self.point1.x,
            self.point1.y,
            self.point2.x,
            self.point2.y,
            fill=fill_color,
            width=2,
        )

    def __str__(self):
        return f"Line({str(self.point1)}, {str(self.point2)})"


class Window:
    def __init__(self, width: int, height: int):
        self.__root = Tk()
        self.__root.title("Maze solver")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

        self.__canvas = Canvas(self.__root, bg="white", height=height, width=width)
        self.__canvas.pack(fill=BOTH, expand=1)

        self.__is_running = False

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__is_running = True
        while self.__is_running:
            self.redraw()

        print("Closing")

    def close(self):
        self.__is_running = False

    def draw_line(self, line: Line, fill_color: str = "black"):
        line.draw(self.__canvas, fill_color)
