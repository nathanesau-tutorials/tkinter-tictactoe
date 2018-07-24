#!/usr/bin/env python
import tkinter as tk
from tkinter.messagebox import showinfo
import time
import random

class Board:
    def __init__(self):
        self.data = [['B' for i in range(3)] for i in range(3)]

    def getWinner(self): # 'B' if no winner
        diag1 = [self.data[0][0], self.data[1][1], self.data[2][2]]
        diag2 = [self.data[0][2], self.data[1][1], self.data[2][0]]
        row1 = [self.data[0][0], self.data[0][1], self.data[0][2]]
        row2 = [self.data[1][0], self.data[1][1], self.data[1][2]]
        row3 = [self.data[2][0], self.data[2][1], self.data[2][2]]
        col1 = [self.data[0][0], self.data[1][0], self.data[2][0]]
        col2 = [self.data[0][1], self.data[1][1], self.data[2][1]]
        col3 = [self.data[0][2], self.data[1][2], self.data[2][2]]
        lines = [diag1, diag2, row1, row2, row3, col1, col2, col3]
        for line in lines:
            if line[0]==line[1] and line[1]==line[2]:
                return line[0]
        return 'B'

    def isFull(self):
        for row in self.data:
            for item in row:
                if item == 'B':
                    return False
        return True

    def update(self, move):
        self.data[move.row][move.col] = move.symbol

class Move:
    def __init__(self, symbol, row, col):
        self.symbol = symbol
        self.row = row
        self.col = col

# todo: improve getMove logic (minimax is optimal)
class AI:
    def __init__(self, symbol):
        self.symbol = symbol
    
    def getMove(self, board): # defensive strategy
        moveOptions = self.getMoveOptions(board)
        whichMove = random.randint(0, len(moveOptions) - 1)
        return Move(self.symbol, moveOptions[whichMove][0], moveOptions[whichMove][1])

    def getMoveOptions(self, board):
        options = []
        for row in range(len(board.data)):
            for col in range(len(board.data[0])):
                if board.data[row][col] == 'B':
                    options.append([row, col])
        return options

class GameController:
    def __init__(self):
        self.board = Board()
        self.ai = AI('O')

class GUI(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.controller = GameController ()
        self.wm_title("Tic Tac Toe")
        self.menubar = tk.Menu(self)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="New Game", command=self.newGame, accelerator="Ctrl+N")
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.config(menu=self.menubar)
        self.c = tk.Canvas(self, width=500, height=500, borderwidth=5, background='white')
        self.c.pack()
        self.c.bind("<Button-1>", self.onClick)
        self.grid = [[None for i in range(3)] for j in range(3)]
        self.bind_all("<Control-n>", self.newGame)

    def newGame(self, event = None):
        for row in range(3):
            for col in range(3):
                if self.grid[row][col] != None:
                    for item in self.grid[row][col]:
                        self.c.delete(item)
                        item = None
        self.controller = GameController () # clear existing game data
        showinfo(None, "Starting new game")

    def show(self):
        self.mainloop()

    def onClick(self, event):
        row_height = self.c.winfo_height()/3
        col_width = self.c.winfo_width()/3
        row = int(event.y/row_height)
        col = int(event.x/col_width)
        
        if self.controller.board.data[row][col] != 'B':
            return # invalid move (ignore)
        else:
            humanMove = Move('X', row, col)
            self.controller.board.update(humanMove)
            self.draw(humanMove)
            time.sleep(0.5)
            if self.controller.board.getWinner() == 'X':
                showinfo(None, "X wins")
            elif self.controller.board.isFull():
                showinfo(None, "Board full")
            else:
                aiMove = self.controller.ai.getMove(self.controller.board)
                self.controller.board.update(aiMove)
                self.draw(aiMove)
                if self.controller.board.getWinner() == 'O':
                    showinfo(None, "O wins")
                elif self.controller.board.isFull():
                    showinfo(None, "Board full")

    def draw(self, move):
        row_height = self.c.winfo_height()/3
        col_width = self.c.winfo_width()/3
        col = move.col
        row = move.row
        symbol = move.symbol
        if(symbol=='O'):
            topLeft = [col*col_width, row*row_height]
            bottomRight = [(col+1)*col_width, (row+1)*row_height]
            self.grid[row][col] = [self.c.create_oval(topLeft,bottomRight,outline='black',fill='white')]
        else:
            topLeft = [col*col_width, row*row_height]
            bottomRight = [(col+1)*col_width, (row+1)*row_height]
            topRight = [(col+1)*col_width, row*row_height]
            bottomLeft = [col*col_width, (row+1)*row_height]
            self.grid[row][col] = [self.c.create_line(topLeft,bottomRight), self.c.create_line(topRight,bottomLeft)]
        self.c.update()
            
gui = GUI()
gui.show()