from sudoku_helpers import *

def main():
    run = 'y'
    while run.lower() == 'y' or run.lower() == 'yes':
        sudoku_string = input("Enter a string representing a sudoku board:\n")
        sudoku_board = string_to_board(sudoku_string)
        find_all = input("Would you like to find all the unique sudoku answers?")
        if find_all.lower() == 'y' or find_all.lower() == 'yes':
            solutions, solved, stats = solveSudoku(sudoku_board, find_all=True)
        else:
            solutions, solved, stats = solveSudoku(sudoku_board, find_all=False)
        print_results(solutions, solved, stats)
        run = input("\nWould you like to run the program on another puzzle?")

main()