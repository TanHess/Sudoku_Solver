from sudoku_helpers import *
from sudoku import Sudoku
from puzzle_menu import PuzzleMenu
import tkinter as tk

def main():
    run = 'y'
    file = input("Hello user! Enter a file to read puzzles from: ")
    menu = PuzzleMenu(file)
    while run.lower() == 'y' or run.lower() == 'yes':
        sudoku_board = menu.show_menu()
        find_all = input("Would you like to find all the unique sudoku answers?")
        if find_all.lower() == 'y' or find_all.lower() == 'yes':
            solutions, solved, stats = solveSudoku(sudoku_board, find_all=True)
        else:
            solutions, solved, stats = solveSudoku(sudoku_board, find_all=False)
        print_results(solutions, solved, stats)
        run = input("\nWould you like to run the program on another puzzle?")
        before_solved_board = Sudoku(sudoku_board)

main()