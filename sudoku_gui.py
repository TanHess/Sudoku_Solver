from tkinter import Tk, Frame, Canvas, BOTH, Button, TOP, BOTTOM, messagebox, Label

from puzzle_menu import PuzzleMenu

MARGIN = 20
SIDE = 50
WIDTH = HEIGHT = MARGIN * 2 + SIDE * 9
class sudokuUI(Frame):
    def __init__(self, parent, game):
        self.game = game
        self.parent = parent
        Frame.__init__(self, parent)
        self.row, self.col = 0, 0
        self.attempts = 3
        self.__initUI()


    def __initUI(self):
        self.parent.title("Sudoku")
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self, width=WIDTH, height=HEIGHT)
        self.canvas.pack(fill=BOTH, side=TOP)



    def __show_menu(self):
        self.menu = PuzzleMenu("puzzles.txt")
        menu_label = Label()
        easy = Button(self, text="Easy")
        medium =  Button(self, text="Medium")
        hard = Button(self, text="Hard")

    
    def __play_game(self, game):
        self.game=game
        clear_button = Button(self, text="Clear answers", command=self.__clear_answers())
        clear_button.pack(fill=BOTH,side=BOTTOM)
        self.__draw_grid()
        self.__draw_puzzle()
        self.canvas.bind("<Button-1>", self.__cell_clicked())
        self.canvas.bind("<Key>", self.__key_pressed())



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


    
