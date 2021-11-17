from typing import List, Tuple, Set
from time import time
from copy import deepcopy

# Initialize the soduko board with a 9x9 list of values passed in 
# during the Class instantiation
class Sudoku():
    def __init__(self, board: List[List[int]]) -> None:
        self._BOX_SIZE = 3
        self._BOARD_SIZE = 9
        self.board = board
        candidates = []
        for i in range(self._BOARD_SIZE):
            row = []
            for j in range(self._BOARD_SIZE):
                if board[i][j] == 0:
                    candidate_set = self.find_candidates(i, j)
                    row.append(candidate_set)
                else:
                    row.append(set())
            candidates.append(row)
        self.candidates = candidates


    # Function to help print the board later (returns a string that represents the current board)
    def __repr__(self) -> str:
        visual_board = ''
        for i in range(self._BOARD_SIZE):
            for j in range(self._BOARD_SIZE):
                if j == 3 or j == 6:
                    visual_board = visual_board + ' | ' + str(self.board[i][j])
                else:
                    visual_board = visual_board + " " + str(self.board[i][j])
            if i == 2 or i == 5:
                visual_board = visual_board + '\n' + '-------+-------+------' + '\n'
            else:
                visual_board = visual_board + '\n'
        return visual_board


    # Function that finds the box specified by the location on the board specified by board[i][j]
    # Operates by determining whether the box starting row is 1, 4, or 7 and same for the column.
    # Returns a set of the values within the 3X3 box based on the starting row/column 
    def find_box_vals(self, r: int, c: int) -> List[int]:
        box_vals = []
        row_start = (r // 3) * self._BOX_SIZE
        column_start = (c // 3) * self._BOX_SIZE
        for i in range(row_start, row_start + self._BOX_SIZE):
            for j in range(column_start, column_start + self._BOX_SIZE):
                box_vals.append(self.board[i][j])
        return box_vals


    # Basically same function as above, instead, returns a list of the indices of the box items 
    # instead of their values. (used for iterating over their values later)
    def find_box_indices(self, r: int, c: int) -> List[Tuple[int, int]]:
        box = []
        row_start = (r // 3) * self._BOX_SIZE
        column_start = (c // 3) * self._BOX_SIZE
        for i in range(row_start, row_start + self._BOX_SIZE):
            for j in range(column_start, column_start + self._BOX_SIZE):
                box.append((i, j))
        return box

    # Simply returns the row specified by the index r; accessed through self.board[r]. 
    def find_row_values(self, r: int) -> List[int]:
        return self.board[r]


    # Iterates over the rows of the board and appends the element at index c (the column to add)
    # to a list. Returns this list (now populated with all the elements in column "c")
    def find_column_values(self, c: int) -> List[int]:
        column = []
        for row in self.board:
            column.append(row[c])
        return column


    # This function finds the possible solutions for a particular location on the board.
    # (Based on which numbers 1-9 are not in the square, in the row, or in the column of board[i][j])
    def find_candidates(self, r: int, c: int) -> Set:
        options = set(range(1, self._BOARD_SIZE + 1)) # Set to hold possible soduko values (1-9)
        column_vals = set(self.find_column_values(c))
        row_vals = set(self.find_row_values(r))
        box_vals = set(self.find_box_vals(r, c))
        used_vals = column_vals | row_vals | box_vals
        available_vals = options.difference(used_vals)
        return available_vals


    # Actual function to place a value and update the self.candidates list
    def place_value(self, r: int, c: int, value: int) -> None:
        self.board[r][c] = value        # Actually place the value
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
                for unique_ind, value in uniques:
                    i, j = unique_ind[0]  # Index of the unique value
                    self.candidates[i][j] = set(value)  # (Ensure that the candidates list reflects the unique value)
                    erased += self.erase(value, indices, unique_ind)  # Delete this value from all the corresponding rows/columns/box candidates
                    

    # Code that takes a list of items to delete from the various candidates sets at indices values.
    def erase(self, nums: List[int], indices: List[Tuple[int,int]], keep: List[Tuple[int,int]]) -> List[Tuple[int,int]]:
        erased = []
        for r, c in indices:
            edited = False
            if ((r, c) in keep):
                continue
            for value in nums:
                if (value in self.candidates[r][c]):
                    self.candidates[r][c].remove(value)
                    edited = True
            if edited == True:
                erased.append((r, c))
        return erased


    # Function to count the potential candidates at a variable list of locations described by the list indices.
    # Will be used in colaboration with get_unique() to discover if any locations have only 1 candidate. 
    def count_candidates(self, indices: List[Tuple[int,int]]) -> List[List[Tuple[int,int]]]:
        count = [[] for _ in range(self._BOARD_SIZE + 1)]
        for r, c in indices:
            for num in self.candidates[r][c]:
                count[num].append((r,c))
        return count


    def get_unique(self, indices: List[Tuple[int,int]]) -> List[Tuple[List[Tuple[int,int]], List[int]]]:
        counts = self.count_candidates(indices)
        uniques = []
        for num, inds in enumerate(counts):
            if len(inds) == 1:
                uniques.append((inds, [num])) # Append the only candidate to unique with its index and value
        return uniques



    def start_game(self):
        self.attempt_board = []
        self.game_over = False
        for i in range(9):
            self.attempt_board.append([])
            for j in range(9):
                self.attempt_board[i].append(self.board[i][j])
    

    def check_win(self):
        solutions, solved, stats = self.solveSudoku(self.board, find_all=True)
        if solved == False:
            return False
        for solution in solutions:
            for i in range(9):
                for j in range(9):
                    if solution[i][j] != self.attempt_board[i][j]:
                        return False
        return True


    def check_submission(self, row, col):
        solutions, solved, stats = self.solveSudoku(self.board, find_all=True)
        for solution in solutions:
            if self.attempt_board[row][col] == solution[row][col]:
                return True
        return False


    def solveSudoku(self, board: List[List[int]], find_all=False) -> Tuple[List[List[List[int]]], bool, dict]:
        def solve(puzzle: Sudoku, depth=0):
            nonlocal calls, max_depth, solutions
            calls += 1
            max_depth = max(max_depth, depth)
            solved = False
            while solved == False:
                solved = True   # Either solved or stuck
                edited = False  # Change to true if we use place_value
                for r in range(puzzle._BOARD_SIZE):
                    for c in range(puzzle._BOARD_SIZE):
                        if puzzle.board[r][c] == 0:     # Unsolved part of board
                            solved = False
                            options = puzzle.candidates[r][c]
                            if len(options) == 0:
                                return False
                            elif len(options) == 1:
                                value = options.pop()
                                puzzle.place_value(r, c, value)
                                edited = True
                if not edited:
                    if solved:
                        solutions.append(puzzle.board)
                        return True
                    else:   # Time to start guessing
                        min_guess = (10, -1)  # Initialize this to a value that is always higher than the highest minimum guesses
                        for r in range(puzzle._BOARD_SIZE):
                            for c in range(puzzle._BOARD_SIZE):
                                options = puzzle.candidates[r][c]
                                if len(options) > 1:
                                    min_guess = min(min_guess, (len(options), (r, c)))
                        r, c = min_guess[1]  # The index of the element with the least possible answers
                        options = puzzle.candidates[r][c]
                        for i in options:
                            next_try = deepcopy(puzzle)
                            next_try.place_value(r, c, i)   # Start guessing values for the next location. (based on the candidates list)
                            solved = solve(next_try, depth=depth+1)    # Recursively call this function now with each guessed value
                            if solved and not find_all:
                                break
                        return solved
            return solved
        solutions = []
        calls = max_depth = 0
        puzzle = Sudoku(board)
        time_start = time()
        solved = solve(puzzle, depth=0)
        time_end = time()
        if len(solutions) > 0:  # Code protects against find_all = True with one solution returning solved=False
            solved = True
        runtime = time_end - time_start
        runtime = "{:.5}".format(runtime)
        stats={
            "calls": calls,
            "max depth": max_depth,
            "unique solutions": len(solutions),
            "runtime" : runtime
        }
        return solutions, solved, stats 



