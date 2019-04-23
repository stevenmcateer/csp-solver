import random

class Cell:
    def __init__(self, value_, is_visible=False):
        self.value = value_
        self.count = 0
        self.visible = False
        self.flag = False

    def show(self):
        self.visible = True

    def set_flag(self):
        self.flag = True

    def __repr__(self):
        if self.visible == True:
            if self.count > 0 and self.value == ".":
                return str(self.count)
            return self.value
        if self.flag == True:
            return "💣"
        else:
            return "█"

class Board:
    #TODO: maybe make resizeable board
    def __init__(self, x, y, num_mines):
        self.board_size = (x,y) #(x,y)
        self.num_mines = num_mines

        start = self.random_start()

        self.mines = self.generate_mines(self.num_mines, start)
        
        self.grid = [['0']*x for y_ in range(y)]

        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if ((x,y) in self.mines):
                    c = Cell("M")
                else:
                    c = Cell(".")

                    adj_x = [x-1, x, x+1]
                    adj_y = [y-1, y, y+1]

                    for y_ in adj_y:
                        for x_ in adj_x:
                            if (x_ >= 0 and x_ < self.board_size[0] and y_ >= 0 and y_ < self.board_size[1]):
                                if ((x_,y_) in self.mines):
                                    c.count += 1


                self.grid[y][x] = c

        self.grid[start[1]][start[0]].visible = True
        self.expand_selection(start[0], start[1])

    def print_board(self):
        top = "    "
        for i, cell in enumerate(self.grid[0]):
            top += "{} ".format(i%10)
        print(top)
        for i, row in enumerate(self.grid):
            if ( len(str(i)) == 2):
                print_row = "{}  ".format(i)
            else:
                print_row = "{}   ".format(i)
            for cell in row:
                print_row += "{} ".format(cell)
            print(print_row)
        print("\n")
        
        return self.did_win()

    def guess_cell(self, x,y):
        if((x,y) not in self.mines):
            self.grid[y][x].visible = True
            new_cells = self.expand_selection(x, y)
            self.print_board()

            return (new_cells)
        elif (x,y) in self.mines:
            for mine in self.mines:
                self.grid[mine[1]][mine[0]].visible = True
            self.print_board()
            print("you're loose, go kill yourself")

    def generate_mines(self, num_mines, start):
        mines = []
        for _ in range(self.num_mines):

            x = random.randrange(0, self.board_size[0], step=1)
            y = random.randrange(0, self.board_size[1], step=1)
            
            while (x,y) in mines or (x,y) == start:
                x = random.randrange(0, self.board_size[0], step=1)
                y = random.randrange(0, self.board_size[1], step=1)
            
            mines.append((x,y))

        return mines
    
    def random_start(self):
        x = random.randrange(0,  self.board_size[0], step=1)
        y = random.randrange(0,  self.board_size[1], step=1)
        return x, y

    def expand_selection(self,x,y):
        uncovered_cells = [(x,y),]
        if (self.grid[y][x].count == 0 and self.grid[y][x].value == "."):
            adj_x = [x-1, x, x+1]
            adj_y = [y-1, y, y+1]
            for y_ in adj_y:
                for x_ in adj_x:
                    if (x_ >= 0 and x_ < self.board_size[0] and y_ >= 0 and y_ < self.board_size[1] and self.grid[y_][x_].visible != True):
                        self.grid[y_][x_].visible = True
                        new_cells = self.expand_selection(x_,y_)
                        uncovered_cells += new_cells
        return uncovered_cells

    def did_win(self):
        for row in self.grid:
            for cell in row:
                if (cell.visible == False and cell.value != 'M'):
                    return False
        print("you win!")
        
        exit()
        return True

