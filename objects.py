from random import randint
import customtkinter as ctk


class Tile:
    def __init__(self, col, row, value):
        self.col = col
        self.row = row
        self.is_flaged = False
        self.is_opened = False
        self.value = value


class Board:
    def __init__(self, rows, cols, mines):
        self.board = []
        self.rows = rows
        self.cols = cols
        self.tiles = self.rows * self.cols
        self.mines = mines
        self.mines_placed = 0
        self.mines_revealed = 0
        self.flags = 0

    def get_cell_by_axis(self, x, y):
        for cell in self.board:
            if cell.col == x and cell.row == y:
                return cell
        return None

    def surrounded_cells(self, tile):
        cells = [
            self.get_cell_by_axis(x=tile.col - 1, y=tile.row - 1),
            self.get_cell_by_axis(x=tile.col - 1, y=tile.row),
            self.get_cell_by_axis(x=tile.col - 1, y=tile.row + 1),
            self.get_cell_by_axis(x=tile.col, y=tile.row - 1),
            self.get_cell_by_axis(x=tile.col + 1, y=tile.row - 1),
            self.get_cell_by_axis(x=tile.col + 1, y=tile.row),
            self.get_cell_by_axis(x=tile.col + 1, y=tile.row + 1),
            self.get_cell_by_axis(x=tile.col, y=tile.row + 1)
        ]

        cells = [cell for cell in cells if cell is not None]
        return cells

    def check_value(self, tile):
        counter = 0
        for cell in self.surrounded_cells(tile):
            if cell.value == -1:
                counter += 1

        return counter

    def generate_board(self):
        for row in range(0, self.rows - 1):
            for col in range(0, self.cols - 1):
                tile = Tile(col=col, row=row, value=0)
                self.board.append(tile)

        while self.mines_placed != self.mines:
            random_row = randint(0, self.rows - 1)
            random_col = randint(0, self.cols - 1)

            for cell in self.board:
                if cell.col == random_col and cell.row == random_row and cell.value != -1:
                    cell.value = -1
                    self.mines_placed += 1
                    break
