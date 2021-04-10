# -*- coding: utf-8 -*-

from tkinter import *
import tkinter.messagebox as mb
from random import randint

class Othelo():
    WIDTH, HEIGHT = 640, 640

    def __init__(self):
        self.win = Tk()
        self.cv = Canvas(self.win, width=Othelo.WIDTH, height=Othelo.HEIGHT)
        self.cv.pack()

        Board(self.cv, self.win)

class Koma():
    WHITE, BLACK = 1, 2
    CW = 80

    def __init__(self, color):
        self.__color = color

    def get_color(self):
        return self.__color

    def set_color(self, color):
        self.__color = color

class Board():
    COLS, ROWS = 8, 8

    def __init__(self, cv, win):
        self.cv = cv
        self.win = win
        self.board = []
        self.is_player_turn = True

        for y in range(0, Board.ROWS):
            self.board.append([0 for x in range(0, Board.COLS)])
        self.board[3][3] = Koma(Koma.WHITE)
        self.board[4][3] = Koma(Koma.BLACK)
        self.board[3][4] = Koma(Koma.BLACK)
        self.board[4][4] = Koma(Koma.WHITE)

        self.cv.bind("<1>", self.player_turn)
        self.game_loop()
        self.win.mainloop()

    def restart_game(self):
        self.board = []
        self.is_player_turn = True

        for y in range(0, Board.ROWS):
            self.board.append([0 for x in range(0, Board.COLS)])
        self.board[3][3] = Koma(Koma.WHITE)
        self.board[4][3] = Koma(Koma.BLACK)
        self.board[3][4] = Koma(Koma.BLACK)
        self.board[4][4] = Koma(Koma.WHITE)
        self.draw_board()

    def hantei(self, x, y, t, c):
        if x < 0 or x >= Board.COLS  or y < 0 or y >= Board.ROWS: return False
        if self.board[y][x] == 0: return False
        if self.is_player_turn:
            if c == 0 and self.board[y][x].get_color() != Koma.BLACK: return False
            if c > 0 and self.board[y][x].get_color() == Koma.WHITE: return (x, y)
            return self.hantei(x + t[0], y + t[1], t, c + 1)
        else:
            if c == 0 and self.board[y][x].get_color() != Koma.WHITE: return False
            if c > 0 and self.board[y][x].get_color() == Koma.BLACK: return (x, y)
            return self.hantei(x + t[0], y + t[1], t, c + 1)

    def reverse_koma(self, x, y, d):
        for t in d:
            x1, y1 = x, y
            xx, yy = d[t][0], d[t][1]
            while True:
                if xx == x1 and yy == y1: break
                x1, y1 = x1 + t[0], y1 + t[1]
                if self.is_player_turn:
                    self.board[y1][x1].set_color(Koma.WHITE)
                else:
                    self.board[y1][x1].set_color(Koma.BLACK)

    def all_hantei(self, x, y):
        d = {}
        result = False
        tbl = [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]
        for t in tbl:
            xx, yy = x + t[0], y + t[1]
            h = self.hantei(xx, yy, t, 0)
            if h:
                d[t] = h
                result = True
        if result: self.reverse_koma(x, y, d)
        return result

    def is_not_allput(self):
        result = True
        tbl = [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]
        for y in range(0, Board.ROWS):
            for x in range(0, Board.COLS):
                if self.board[y][x] == 0:
                    for t in tbl:
                        xx, yy = x + t[0], y + t[1]
                        if self.hantei(xx, yy, t, 0):
                            result = False
        return result

    def judge_resule(self):
        w, b = 0, 0
        for y in range(0, Board.ROWS):
            for x in range(0, Board.COLS):
                if self.board[y][x] == 0: return False
                if self.board[y][x].get_color() == Koma.WHITE:
                    w += 1
                else:
                    b += 1
        if w == 0: mb.showinfo("結果", "白コマ'{0}'' : 黒コマ'{1}'\nYOU LOSE".format(w, b))
        if b == 0: mb.showinfo("結果", "白コマ'{0}'' : 黒コマ'{1}'\nYOU WIN!".format(w, b))
        if w > b: mb.showinfo("結果", "白コマ'{0}'' : 黒コマ'{1}'\nYOU WIN!".format(w, b))
        if w < b: mb.showinfo("結果", "白コマ'{0}'' : 黒コマ'{1}'\nYOU LOSE".format(w, b))
        if w == b: mb.showinfo("結果", "白コマ'{0}'' : 黒コマ'{1}'\n!DRAW!".format(w, b))
        return True

    def player_turn(self, e):
        if not self.is_player_turn: return
        #print("player_turn")
        x, y = int(e.x / Koma.CW), int(e.y / Koma.CW)
        if self.board[y][x] != 0: return
        if self.is_not_allput():
            self.is_player_turn = False
            print("置ける場所がありません")
            return
        if not self.all_hantei(x, y): return
        self.board[y][x] = Koma(Koma.WHITE)
        self.draw_board()
        self.is_player_turn = False

    def make_strategy(self):
        for y in range(0, Board.ROWS):
            for x in range(0, Board.COLS):
                if self.board[y][x] == 0:
                    if self.all_hantei(x, y):
                        self.board[y][x] = Koma(Koma.BLACK)
                        return
        print("置ける場所がありません")

    def opponent_turn(self):
        if self.is_player_turn: return
        #print("opponent_turn")
        self.make_strategy()
        self.is_player_turn = True

    def game_loop(self):
        self.draw_board()
        if self.judge_resule(): self.restart_game()
        if not self.is_player_turn:
            self.opponent_turn()
        self.win.after(1000, self.game_loop)

    def draw_board(self):
        self.cv.delete("all")
        self.cv.create_rectangle(0, 0, Othelo.WIDTH, Othelo.HEIGHT, fill="green")
        for y in range(0, Board.ROWS):
            for x in range(0, Board.COLS):
                self.cv.create_line(0, y * Koma.CW, Othelo.WIDTH, y * Koma.CW)
                self.cv.create_line(x * Koma.CW, 0, x * Koma.CW, Othelo.HEIGHT)
        for y in range(0, Board.ROWS):
            for x in range(0, Board.COLS):
                if self.board[y][x] == 0: continue
                x1, y1 = x * Koma.CW, y * Koma.CW
                if self.board[y][x].get_color() == Koma.WHITE:
                    self.cv.create_oval(x1, y1, x1 + Koma.CW, y1 + Koma.CW, fill="white")
                else:
                    self.cv.create_oval(x1, y1, x1 + Koma.CW, y1 + Koma.CW, fill="black")

def main():
    Othelo()

if __name__ == '__main__':
    main()
