import sys
import numpy as np
import copy
from board import Board
import json

class CSP:
    def __init__(self):
        self.total_mines = 0
        self.known_mines = []
        self.total_cells = 0
        self.cells_remaining = []
        self.rules = []


def simplify_rules(csp):
    to_delete = []
    for j, rule in enumerate(csp.rules):
        for i, cell in enumerate(rule["cells"]):
            if cell in csp.known_mines:
                rule["count"] = rule["count"] - 1
                del rule["cells"][i]
        if rule["cells"] == []:
            to_delete.append(j)

    to_delete = to_delete[::-1]
    for delete in to_delete:
        del csp.rules[delete]


def solver(csp, b):
    # list of easy bombs that have to be bombs
    possible_mines = mrv(csp)
    while possible_mines != []:

        should_kill = True
        for mine in possible_mines:
            if mine not in csp.known_mines:
                should_kill = False
        if (should_kill):
            break
        
        for mine in possible_mines:
            # remove mines from remaining
            # add mines to known mines
            if mine not in csp.known_mines:
                csp.known_mines.append(mine)
            if mine in csp.cells_remaining:
                del csp.cells_remaining[csp.cells_remaining.index(mine)]

        print("known mines", csp.known_mines)
        #print("remaining", csp.cells_remaining)

        # simplify rules based off of known mines
        simplify_rules(csp)

        safe_guess = []
        for rule in csp.rules:
            if rule["count"] == 0:
                for cell in rule["cells"]:
                    if cell not in safe_guess:
                        safe_guess.append(cell)
        
        print(safe_guess, "safe_guess")

        for guess in safe_guess:
            print(guess)
            b.guess_cell(guess[0], guess[1])
            del csp.cells_remaining[csp.cells_remaining.index(guess)]
            for rule in csp.rules:
                if guess in rule["cells"]:
                    del rule["cells"][rule["cells"].index(guess)]

        safe_guess = []
        simplify_rules(csp)

        update_rules(b, csp)
        possible_mines = mrv(csp)
        print("possible mines", possible_mines)

    if(len(csp.known_mines) == csp.total_mines):
        for not_mine in csp.cells_remaining:
            print(not_mine, "this is not a mine!")
            b.guess_cell(not_mine[0], not_mine[1])

#find the min remaining value
def mrv(csp):
    mines = []
    for rule in csp.rules:
        if rule["count"] == len(rule["cells"]):
            for cell in rule["cells"]:
                if (cell not in mines):
                    mines.append(cell)
    
    return mines


def read_input(board):
    csp = CSP()
    b = board
    is_done = b.print_board()
    if (is_done):
        print("We did it!!")
        exit()
    csp.total_cells = len(b.grid) * len(b.grid[0])
    csp.total_mines = b.num_mines

    update_rules(b, csp)
    return csp



def update_rules(board, csp):
    b = board
    for y, row in enumerate(b.grid):
        for x, cell in enumerate(row):
            if(cell.visible == True and cell.count > 0):
                rule = {
                    "count": cell.count,
                    "cells": []
                }
                adj_x = [x-1, x, x+1]
                adj_y = [y-1, y, y+1]
                for y_ in adj_y:
                    for x_ in adj_x:
                        if (y_ < b.board_size[1] and x_ < b.board_size[0] and y_ >= 0 and x_ >= 0):
                            if(b.grid[y_][x_].visible == False):
                                rule["cells"].append((x_, y_))
                if rule not in csp.rules:
                    csp.rules.append(rule)

            if(cell.visible == False):
                if (x,y) not in csp.cells_remaining and (x,y) not in csp.known_mines:
                    csp.cells_remaining.append((x,y))

if __name__ == "__main__":
    b = Board(10, 10, 10)
    csp = read_input(b)
    solver(csp, b)