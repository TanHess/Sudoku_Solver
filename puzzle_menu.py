from sudoku_helpers import *

class PuzzleMenu():
    def __init__(self, infile: str) -> None:

        beg = []
        int = []
        exp = []
        sel = -1
        with open(infile, 'r') as file:
            for line in file:
                stripped_line = line.rstrip()
                if stripped_line == '':
                    continue
                if stripped_line == 'EASY':
                    sel = 1
                elif stripped_line == 'INTERMEDIATE':
                    sel = 2
                elif stripped_line == 'EXPERT':
                    sel = 3
                else:
                    if sel == 1:
                        beg.append(str(stripped_line))
                    elif sel == 2:
                        int.append(str(stripped_line))
                    elif sel == 3:
                        exp.append(str(stripped_line))
                    else:
                        continue  # Does not follow the naming conventions, skip line
        self.easy_puzzles = beg
        self.intermediate_puzzles = int
        self.expert_puzzles = exp



    def display_category(self, category: List[str]) -> int:
        counter = 0
        for puzzle in category:
            board = string_to_board(puzzle)
            temp_sudoku =  Sudoku(board)
            counter += 1
            print("\n===============BOARD " + str(counter) + "===============\n")
            print(repr(temp_sudoku))
        return counter


    def show_menu(self) -> List[List[int]]:
        print("Hello user, Welcome to the Sudoku solver.")
        print("Please pick a category to choose a puzzle from!")
        print("1) EASY")
        print("2) MEDIUM")
        print("3) EXPERT")
        choice = input("Enter your choice: ")
        while choice not in ['1', '2', '3']:
            choice = input("Error! Invalid choice!\n Please enter a valid choice now: ")

        if int(choice) == 1:
            num_options = self.display_category(self.easy_puzzles)
            new_choice = input("Which board would you like to solve? (1-"+str(num_options)+")")
            index = int(new_choice) - 1
            return string_to_board(self.easy_puzzles[index])
        elif int(choice) == 2:
            num_options = self.display_category(self.intermediate_puzzles)
            new_choice = input("Which board would you like to solve? (1-"+str(num_options)+")")
            index = int(new_choice) - 1
            return string_to_board(self.intermediate_puzzles[index])
        elif int(choice) == 3:
            num_options = self.display_category(self.expert_puzzles)
            new_choice = input("Which board would you like to solve? (1-"+str(num_options)+")")
            index = int(new_choice) - 1
            return string_to_board(self.expert_puzzles[index])
        else:
            print("ERROR! Some unexpected and unhandled error occured")
            return