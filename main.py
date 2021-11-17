from sudoku_gui import sudokuUI, WIDTH, HEIGHT
from sudoku_helpers import *
from sudoku import Sudoku
from puzzle_menu import PuzzleMenu
import tkinter as tk

def main():
    run = 'y'
    file = input("Hello user! Enter a file to read puzzles from: ")
    menu = PuzzleMenu(file)
    while run.lower() == 'y' or run.lower() == 'yes':
        play_or_solve = input("Would you like to \n 1) Play game \n 2) Solve the puzzle \n Please enter your answer: ")
        if play_or_solve == '1':
            sudoku_board = menu.show_menu()
            game = Sudoku(sudoku_board)
            game.start_game()
            root = tk.Tk()
            sudokuUI(root, game)
            root.geometry("%dx%d" % (WIDTH, HEIGHT+40))
            root.mainloop
        elif play_or_solve == '2':
            sudoku_board = menu.show_menu()
            find_all = input("Would you like to find all the unique sudoku answers?")
            if find_all.lower() == 'y' or find_all.lower() == 'yes':
                solutions, solved, stats = solveSudoku(sudoku_board, find_all=True)
            else:
                solutions, solved, stats = solveSudoku(sudoku_board, find_all=False)
            print_results(solutions, solved, stats)
            run = input("\nWould you like to run the program on another puzzle?")
            before_solved_board = Sudoku(sudoku_board)
        else:
            print("***Error, please select a valid option*** \n")


if __name__ == '__main__':
    main()