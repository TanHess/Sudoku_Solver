from tkinter import *
from tkinter import messagebox
from tkinter.constants import LEFT
from sudoku import Sudoku
from puzzle_menu import PuzzleMenu
from sudoku_helpers import string_to_board

# GLOBALS:
MARGIN = 20
SIDE = 50
WIDTH = HEIGHT = MARGIN * 2 + SIDE * 9

# Main class to display the tkinter GUI. Inherits from the Tk object
class appUI(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.geometry("%dx%d" % (WIDTH, HEIGHT+40))     # Set the main frame size.
        self.main_frame = Frame(self)
        self.main_frame.pack(side=TOP, fill=BOTH, expand = True)
        self.main_frame.grid_rowconfigure(0, weight = 1)
        self.main_frame.grid_columnconfigure(0, weight = 1)
        #self.show_game(Sudoku(string_to_board(".2.3.475......2......6.9.212.....1.......3.4.3...9..7.7..5.1396..........6..2...5")))
        self.show_menu()

    # Function to make a new game board in the app. (go to sudokuUI)
    def show_game(self, game):
        game_window = Toplevel(self)
        frame = sudokuUI(game_window, game_window, game)
        frame.tkraise()
    # Function to show the main menu. 
    def show_menu(self):
        frame = menuUI(self.main_frame, self)
        frame.tkraise()




class sudokuUI(Frame):
    def __init__(self, parent, controller, game):
        self.game = game
        self.game.start_game()
        self.controller = controller
        self.parent = parent
        Frame.__init__(self, parent)
        self.row, self.col = 0, 0
        self.attempts = 3
        self.__initUI()


    def __initUI(self):
        self.controller.title("Sudoku")
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self, width=WIDTH, height=HEIGHT)
        self.canvas.pack(fill=BOTH, side=TOP)
        clear_button = Button(self, text="Clear answers", command=self.__clear_answers)
        clear_button.pack(fill=BOTH,side=BOTTOM)
        self.__draw_grid()
        self.__draw_puzzle()
        self.canvas.bind("<Button-1>", self.__cell_clicked)
        self.canvas.bind("<Key>", self.__key_pressed)


    def __draw_grid(self):
        for i in range(10):
            color = "blue" if i%3 == 0 else "gray"

            x0 = MARGIN + i*SIDE
            y0 = MARGIN
            x1 = MARGIN + i*SIDE
            y1 = HEIGHT - MARGIN
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

            x0 = MARGIN
            y0 = MARGIN + i*SIDE
            x1 = WIDTH - MARGIN
            y1 = MARGIN + i*SIDE
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

    def __draw_puzzle(self):
        self.canvas.delete("numbers")
        for i in range(9):
            for j in range(9):
                answer = self.game.attempt_board[i][j]
                if answer != 0:
                    x = MARGIN + j * SIDE + SIDE / 2
                    y = MARGIN + i * SIDE + SIDE / 2
                    original = self.game.board[i][j]
                    color = "black" if answer == original else "sea green"
                    self.canvas.create_text(x, y, text=answer, tags="numbers", fill=color)

    def __clear_answers(self):
        self.game.start_game()
        self.canvas.delete("victory")
        self.canvas.delete("loser")
        self.canvas.delete("winner")
        self.canvas.delete("loss")
        self.attempts = 3
        self.__draw_puzzle()

    def __cell_clicked(self, event):
        if self.game.game_over:
            return
        
        x, y = event.x, event.y
        if (MARGIN < x < WIDTH - MARGIN and MARGIN < y < HEIGHT - MARGIN):
            self.canvas.focus_set()

            row, col = int((y - MARGIN) / SIDE), int((x - MARGIN) / SIDE)

            if (row, col) == (self.row, self.col):
                self.row, self.col = -1, -1
            elif self.game.attempt_board[row][col] == 0:
                self.row, self.col = row, col
        self.__draw_cursor()


    def __draw_cursor(self):
        self.canvas.delete("cursor")
        if self.row >= 0 and self.col >= 0:
            x0 = MARGIN + self.col * SIDE + 1
            y0 = MARGIN + self.row * SIDE + 1
            x1 = MARGIN + (self.col + 1) * SIDE - 1
            y1 = MARGIN + (self.row + 1) * SIDE - 1
            self.canvas.create_rectangle(x0, y0, x1, y1, outline="red", tags="cursor")
            

    def __key_pressed(self, event):
        if self.game.game_over:
            return
        if self.row >= 0 and self.col >= 0 and event.char in "1234567890":
            self.game.attempt_board[self.row][self.col] = int(event.char)
            if self.game.check_submission(self.row, self.col):
                self.col, self.row = -1, -1
                self.__draw_puzzle()
                self.__draw_cursor()
                if self.game.check_win():
                    self.__draw_victory()
            else:
                self.game.attempt_board[self.row][self.col] = 0
                self.attempts -= 1
                if self.attempts == 0:
                    self.__draw_loss()
                    return
                self.col, self.row = -1, -1
                self.__draw_puzzle()
                self.__draw_cursor()
                messagebox.showinfo("Information", "Sorry, but that is an incorrect move, you have " + str(self.attempts) + " attempts left.")

    

    def __draw_loss(self):
            x0 = y0 = MARGIN + SIDE * 2
            x1 = y1 = MARGIN + SIDE * 7
            self.canvas.create_oval(x0, y0, x1, y1, tags="loss", fill="dark orange", outline="orange")
            x = y = MARGIN + 4*SIDE + SIDE/2
            self.canvas.create_text(x, y, text="You lose!", tags="loser", fill="white", font=("Arial", 32))


    def __draw_victory(self):
        x0 = y0 = MARGIN + SIDE * 2
        x1 = y1 = MARGIN + SIDE * 7
        self.canvas.create_oval(x0, y0, x1, y1, tags="victory", fill="dark orange", outline="orange")
        x = y = MARGIN + 4*SIDE + SIDE/2
        self.canvas.create_text(x, y, text="You win!", tags="winner", fill="white", font=("Arial", 32))







class menuUI(Frame):
    def __init__(self, parent, controller):
        self.parent = parent
        Frame.__init__(self, parent)
        self.menu = PuzzleMenu()
        self.pack(fill=BOTH, expand=1)
        self.puzzles_frame = Frame(self)
        self.puzzles_frame.pack(side=BOTTOM, fill=BOTH)
        self.show_categories(controller=controller)
        

    def show_categories(self, controller):
        easy = Button(self, text='Easy', command= lambda: self.show_puzzles(0, controller=controller))
        easy.pack(side=TOP)
        intermediate = Button(self, text='Intermediate', command= lambda: self.show_puzzles(1, controller=controller))
        intermediate.pack(side=TOP, ipadx=5)
        expert = Button(self, text='Expert', command= lambda: self.show_puzzles(2, controller=controller))
        expert.pack(side=TOP, ipadx=5)


    def show_puzzles(self, category, controller):
        for widget in self.puzzles_frame.winfo_children():
            widget.destroy()
        count = 1
        puzzles = self.menu.get_boards(category)
        for puzzle in puzzles:
            label = Label(self.puzzles_frame, text = str(count))
            game_btn = Button(self.puzzles_frame, text=repr(puzzle), command=lambda puzzle=puzzle: controller.show_game(puzzle)).pack(side=LEFT, ipady=5)
            count +=1

        '''for visual, i in boards.items():
            Radiobutton(self, text=visual, variable=var, value=i, command= lambda: show_button(var.get())).pack(side=LEFT, ipady=5 ,anchor=W)
        def show_button(count):
            print('\n'+str(count)+'\n')
            if category == 0:
                board = Sudoku(string_to_board(self.menu.easy_puzzles[count]))
            elif category == 1:
                board = Sudoku(string_to_board(self.menu.intermediate_puzzles[count]))
            elif category == 2:
                board = Sudoku(string_to_board(self.menu.expert_puzzles[count]))
            play_button = Button(self, text='Play Game', command=lambda: controller.show_game(board)).pack(anchor=S)


'''


if __name__ == '__main__':
    app = appUI()
    app.mainloop()

    
