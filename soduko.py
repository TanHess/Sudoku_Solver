


# Initialize the soduko board with a 9x9 list of values passed in 
# during the Class instantiation
class Soduko():
    def __init__(self, board: list[list[int]]) -> None:
        self._BOX_SIZE = 3
        self._BOARD_SIZE = 9
        self.board = board
        self.n = len(board)
        candidates = []
        for i in range(self.n):
            row = []
            for j in range(self.n):
                pass

    
    # Function that finds the box specified by the location on the board specified by board[i][j]
    # Operates by determining whether the box starting row is 1, 4, or 7 and same for the column.
    # Returns a set of the values within the 3X3 box based on the starting row/column 
    def find_box_vals(self, r: int, c: int) -> list[list[int]]:
        box = []
        row_start = (r // 3) * self._BOX_SIZE
        column_start = (c // 3) * self._BOX_SIZE
        for i in range(row_start, row_start + self._BOX_SIZE):
            box_row = []
            for j in range(column_start, column_start + self._BOX_SIZE):
                box_row.append(self.board[i][j])
            box.append(box_row)
        return box

    # Simply returns the row specified by the index r; accessed through self.board[r]. 
    def find_row_values(self, r: int) -> list[int]:
        return self.board[r]


    # Iterates over the rows of the board and appends the element at index c (the column to add)
    # to a list. Returns this list (now populated with all the elements in column "c")
    def find_column_values(self, c: int) -> list[int]:
        column = []
        for row in self.board:
            column.append(row[c])
        return column


    # This function finds the possible solutions for a particular location on the board.
    # (Based on which numbers 1-9 are not in the square, in the row, or in the column of board[i][j])
    def find_candidates(self, r: int, c: int) -> set(int):
        options = set(range(1, self._BOARD_SIZE + 1)) # Set to hold possible soduko values (1-9)
        column_vals = set(self.find_column_values(c))
        row_vals = set(self.find_row_values(r))
        box_vals = set(self.find_box_vals(r, c))
        used_vals = set(column_vals, row_vals, box_vals)
        available_vals = options.difference(used_vals)
        return available_vals

