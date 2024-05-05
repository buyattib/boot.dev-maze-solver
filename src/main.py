from window import Window
from maze import Maze


def main():
    win_width = 800
    win_height = 600

    win = Window(win_width, win_height)

    margin = 50
    num_rows = 6
    num_cols = 8
    cell_size_x = (win_width - 2 * margin) / num_cols
    cell_size_y = (win_height - 2 * margin) / num_rows
    seed = 0
    maze = Maze(margin, margin, num_rows, num_cols, cell_size_x, cell_size_y, win, seed)
    result = maze.solve()

    if result:
        print("Maze solved!")
    else:
        pritn("Maze cant be solved!")

    win.wait_for_close()


if __name__ == "__main__":
    main()
