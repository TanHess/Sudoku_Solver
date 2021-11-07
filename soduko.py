


# Initialize the soduko board with a 9x9 list of values passed in 
# during the Class instantiation
class Soduko():
    def __init__(self, board: list[list[int]]) -> None:
        self._BOX_SIZE = 3
        self._BOARD_SIZE = 9
        self.board = board
        candidates = []
        for i in range(self._BOARD_SIZE):
            row = []
            for j in range(self._BOARD_SIZE):
                candidate_set = self.find_candidates(i, j)
                row.append(candidate_set)
            candidates.append(row)
        self.candidates = candidates


    # Function to help print the board later (returns a string that represents the current board)
    def __repr__(self) -> str:
        visual_board = ''
        for i in range(self._BOARD_SIZE):
            for j in range(self._BOARD_SIZE):
                if j == 3 or j == 6:
                    visual_board = visual_board + '|' + self.board[i][j]
                else:
                    visual_board = visual_board + self.board[i][j]
            if i == 2 or i == 5:
                visual_board = visual_board + '\n' + '------+-------+------' + '\n'
            else:
                visual_board = visual_board + '\n'
        return visual_board


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


    # Basically same function as above, instead, returns a list of the indices of the box items 
    # instead of their values. (used for iterating over their values later)
    def find_box_indices(self, r: int, c: int) -> list[tuple(int, int)]:
        box = []
        row_start = (r // 3) * self._BOX_SIZE
        column_start = (c // 3) * self._BOX_SIZE
        for i in range(row_start, row_start + self._BOX_SIZE):
            for j in range(column_start, column_start + self._BOX_SIZE):
                box.append((i, j))
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


    # Actual function to place a value and update the self.candidates list
    def place_value(self, r: int, c: int, value: int) -> None:
        self.board[r][c] = value
        self.candidates[r][c] = set()
        inds_row = [(r, i) for i in range(self._BOARD_SIZE)]
        inds_col = [(i, c) for i in range(self._BOARD_SIZE)]
        inds_box = self.find_box_indices(r, c)
        erased = [(r, c)]
        erased += self.erase([value], inds_row + inds_col + inds_box, [])
        while erased:
            r, c = erased.pop()
            inds_row = [(r, i) for i in range(self._BOARD_SIZE)]
            inds_col = [(i, c) for i in range(self._BOARD_SIZE)]
            inds_box = self.find_box_indices(r, c)
            for indices in [inds_row, inds_col, inds_box]:
                uniques = self.get_unique(indices)




    # Code that takes a list of items to delete from the various candidates sets at indices values.
    def erase(self, nums: list[int], indices: list[tuple(int,int)], keep: list[tuple(int,int)]) -> list[tuple(int,int)]:
        erased = []
        for r, c in indices:
            edited = False
            if ((r, c) in keep):
                continue
            for value in nums:
                if value in self.candidates[r][c]:
                    self.candidates[r][c].remove(value)
                    edited = True
            if edited == True:
                erased.append((r, c))
        return erased


    # Function to count the potential candidates at a variable list of locations described by the list indices.
    # Will be used in colaboration with get_unique() to discover if any locations have only 1 candidate. 
    def count_candidates(self, indices: list[tuple(int,int)]) -> list[list[tuple(int,int)]]:
        count = [[] for _ in range(self._BOARD_SIZE + 1)]
        for r, c in indices:
            for num in self.candidates[r][c]:
                count[num].append(r,c)
        return count


    def get_unique(self, indices: list[tuple(int,int)]) -> list[tuple(tuple(int,int),int)]:
        counts = self.count_candidates(indices)
        uniques = []
        for i, inds in enumerate(counts):
            if len(inds) == 1:
                uniques.append((inds, [i]))
        return uniques
