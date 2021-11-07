from sudoku import Sudoku
from copy import deepcopy
from time import time
from typing import List, Tuple


def solveSudoku(board: List[List[int]], find_all=False) -> Tuple[List[List[List[int]]], bool, dict]:
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


# This function takes a string of values and converts it to a sudoku board:
def string_to_array(string: str) -> List[int]:
    arr = []
    for num in string:
        if num == '.':
            arr.append(0)
        else:
            arr.append(int(num))
    return arr


# This function takes an array of numbers that represent a soduko board and builds the grid.
def array_to_board(arr: List[int]) -> List[List[int]]:
    board = []
    for i in range(0, len(arr), 9):
        board.append(arr[i:i+9])    # Every 9 numbers, board is appended the row with those nine numbers (as a list)
    return board


# Reverse of array_to_baord. Accpets a 9x9 board and returns a single array with the elements of the board.
def board_to_array(board: List[List[int]]) -> List[int]:
    new_arr = []
    for row in board:
        for item in row:
            new_arr.append(item)
    return new_arr


# Reverse of string_to_array: Accepts an array representing the sudoku board and returns a string representing the board
def array_to_string(arr: List[int]) -> str:
    new_string = ''
    for num in arr:
        new_string += str(num)
    return new_string

# Combination of board_to_array and array_to_string. Takes a 9x9 sudoku board and returns a string containing a representation of the same board
def board_to_string(board: List[List[int]]) -> str:
    arr = board_to_array(board)
    return array_to_string(arr)


# Combination of string_to_array and array_to_board. Takes a string and converts it to a 9x9 board
def string_to_board(string: str) -> List[List[int]]:
    arr = string_to_array(string)
    return array_to_board(arr)


# Function to print the results of a given sudoku solution
def print_results(solutions: List[List[List[int]]], solved: bool, stats: dict) -> None:
    print("\n\n===============================RESULTS===============================")
    if solved:
        print("\nYour puzzle was solved!\n")
        print("---------------------------------------------------------------------")
        print("\nStatistics:\n\tCalls:", stats.get("calls"), "\n\tMax Depth:", \
            stats.get("max depth"), "\n\tFound solutions:", stats.get("unique solutions"), \
             "\n\tRuntime:", float(stats.get("runtime")) * 1000, "milliseconds.")
        print("\n")
        for count, board in enumerate(solutions):
            print("---------------------------------------------------------------------")
            puzzle = Sudoku(board)
            print("\nSolution", str(count+1) +":\n")
            print(repr(puzzle))
    else:
        print("\nSorry, your puzzle could not be solved. Here are the results:\n")
        print("\nStatistics:\n\tCalls:", stats.get("calls"), "\n\tMax Depth:", \
            stats.get("max depth"), "\n\tFound solutions:", stats.get("unique solutions"), \
             "\n\tRuntime:", float(stats.get("runtime")) * 1000, "milliseconds.")
        print("")
    print("===============================RESULTS===============================")
            

