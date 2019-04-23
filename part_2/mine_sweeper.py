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
    print("simplifying rules")
    # can also find subset rules and break apart
    for _ in range(2):
        to_delete = []
        for j, rule in enumerate(csp.rules):
            for i, cell in enumerate(rule["cells"]):
                if cell in csp.known_mines:
                    rule["count"] = rule["count"] - 1
                    del rule["cells"][rule["cells"].index(cell)]
            if rule["cells"] == []:
                to_delete.append(j)

        to_delete = to_delete[::-1]
        for delete in to_delete:
            del csp.rules[delete]

    # remove duplicates
    rules_to_delete = []
    for i, rule in enumerate(csp.rules):
        if i != len(csp.rules):
            for j, all_rules in enumerate(csp.rules):
                if j > i and rule["cells"] == all_rules["cells"]:
                    if (j not in rules_to_delete):
                        rules_to_delete.append(j)
    
    
    rules_to_delete = sorted(rules_to_delete, reverse=True)
    for rule_index in rules_to_delete:
        del csp.rules[rule_index]


def solver(csp, b):
    # list of easy bombs that have to be bombs
    possible_mines = trivial_constraint(csp)
    while possible_mines != []:
        
        for mine in possible_mines:
            # remove mines from remaining
            # add mines to known mines
            if mine not in csp.known_mines:
                csp.known_mines.append(mine)
            if mine in csp.cells_remaining:
                del csp.cells_remaining[csp.cells_remaining.index(mine)]

        for mines in csp.known_mines:
            if b.grid[mines[1]][mines[0]].flag == False:
                b.grid[mines[1]][mines[0]].set_flag()

        print("known mines", csp.known_mines)
        print("remaining", csp.cells_remaining)

        # simplify rules based off of known mines
        simplify_rules(csp)
        # make ALL possible safe guesses
        make_safe_guess(csp)
        
        possible_mines = trivial_constraint(csp)

#find the min remaining value
def trivial_constraint(csp):
    print("identify trivial constraints")
    mines = []
    for rule in csp.rules:
        if rule["count"] == len(rule["cells"]):
            for cell in rule["cells"]:
                if (cell not in mines and cell not in csp.known_mines):
                    mines.append(cell)
    
    return mines

def make_safe_guess(csp):

    safe_guess = find_safe_guesses(csp)

    while safe_guess != []:
        print("safe_guess", safe_guess)
        uncovered_cells = []
        for guess in safe_guess:
            print(guess)
            new_cells = b.guess_cell(guess[0], guess[1])
            uncovered_cells += new_cells
            del csp.cells_remaining[csp.cells_remaining.index(guess)]
            for rule in csp.rules:
                if guess in rule["cells"]:
                    del rule["cells"][rule["cells"].index(guess)]
        
        if uncovered_cells != []:
            update_rules(b, csp, uncovered_cells)
        
        simplify_rules(csp)

        safe_guess = find_safe_guesses(csp)

def find_safe_guesses(csp):
    safe_guess = []
    for rule in csp.rules:
        if rule["count"] == 0:
            for cell in rule["cells"]:
                if cell not in safe_guess:
                    safe_guess.append(cell)
    
    return(safe_guess)
    


def read_input(board):
    csp = CSP()
    b = board
    is_done = b.print_board()
    if (is_done):
        print("We did it!!")
        exit()
    csp.total_cells = len(b.grid) * len(b.grid[0])
    csp.total_mines = b.num_mines

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
    return csp



def update_rules(board, csp, new_cells):
    b = board
    #import ipdb; ipdb.set_trace()
    for cell_ in new_cells:
        # add new rules
        x = cell_[0]
        y = cell_[1]

        cell = b.grid[y][x]

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
                csp.rules.append(rule)
        # remove cells from cells remaining
        
        if cell_ in csp.cells_remaining:
            del csp.cells_remaining[csp.cells_remaining.index(cell_)]

        # remove the cells from rules
        for rule in csp.rules:
            if cell_ in rule["cells"]:
                del rule["cells"][rule["cells"].index(cell_)]


if __name__ == "__main__":
    b = Board(10, 10, 10)
    csp = read_input(b)
    solver(csp, b)
    # need to update rules 
    print("rules! \n", csp.rules, len(csp.rules))
    if(len(csp.known_mines) == csp.total_mines):
        for not_mine in csp.cells_remaining:
            b.guess_cell(not_mine[0], not_mine[1])