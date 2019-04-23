William Schwartz and Steven McAteer

## TO RUN:
1. Open a terminal
2. Type "python minesweeper.py"
3. The program will output the steps it took to try to solve the game.

## NOTES:
1. There is a default board size specified in the code, so there is no
input files to test with.
2. The first move is randomized and changes on each run
3. The mine locations are also randomized and change each run

## OUR APPROACH:

```
Objects:
    - Board(width, height, num_of_bombs)
    - Cell(x, y, value, visible)
    - CSP:
        - total_mines
        - known_mines = []
        - cells_remaining = []
        - rules = []
```

For each move on the game board, the game expands to the farthest point it can
without uncovering a bomb. Once it reaches this threshold, it creates an edge of cells
with a number in each of them -- this is the number of mines in the surrounding neighbors
 for that cell. To keep track of this, we create a rule for each cell.
Each rule consists of 2 things:
    - The number of known bombs in the cell's neighbors
    - A list of the cell's neighbors

The main functions that we use are:
1. solver: calls all of the following functions and runs the game

```
    Find all possible mines
    possible_mines = trivial_constraint(csp)

    while there are still possible mines, do

        for each mine in possible_mines:
            remove mines from cells_remaining
            add mines to known mines

        for each mines in known_mines:
            set a flag on the cell to mark it

        # simplify rules based off of known mines
        simplify_rules(csp)

        # make ALL possible safe guesses
        make_safe_guess(csp)

        Find all possible mines and try again
        possible_mines = trivial_constraint(csp)

```

2. trivial_constraint: this searches through all of the rules and determines
if any of the constraints are trivial. Basically, if a cell only has one neighbor
and has a mine count of 1, then mark that cell as a mine. Return this mine list
to solver.

3. simplify_rules: this function iterates through all of the rules and
updates the neighbor lists for each mine with the new values. It removes
mine locations, as well as duplicates.

4. make_safe_guess: search through all of the rules and find rules that
have a mine count of 0 and a list of neighbors. Mark all of these cells
 as safe and make each guess.

5. update_rules: takes in a list of newly uncovered cells from a cell expansion
 and creates rules for all of them, as described above.

## CHANGES FROM PART 1:

Because of the nature of how minesweeper is played, we had to change the code from
our Part 1 quite a bit.



## RESULTS:

### Winning the Game

```bash
(venv) Williams-MacBook-Pro:part_2 williamschwartz$ python mine_sweeper.py
    0 1 2 3 4 5 6 7 8 9
0   . . . . . . . . . .
1   . . . . . . . . . .
2   . . . . 1 1 1 . . .
3   . . . . 1 █ 2 1 1 .
4   . . . . 1 2 █ █ 1 .
5   1 1 1 . . 1 █ █ 1 .
6   █ █ 2 . . 1 2 █ 1 .
7   █ █ 2 . . . 1 █ 1 .
8   █ █ 3 2 1 . 1 2 3 2
9   █ █ █ █ 1 . . 1 █ █


identify trivial constraints
known mines [(5, 3), (7, 4), (1, 6), (1, 7), (6, 5), (2, 9), (3, 9), (7, 7), (8, 9), (9, 9)]
remaining [(6, 4), (7, 5), (0, 6), (7, 6), (0, 7), (0, 8), (1, 8), (0, 9), (1, 9)]
simplifying rules
safe_guess [(6, 4), (7, 5), (0, 6), (7, 6), (1, 8), (1, 9)]
(6, 4)
    0 1 2 3 4 5 6 7 8 9
0   . . . . . . . . . .
1   . . . . . . . . . .
2   . . . . 1 1 1 . . .
3   . . . . 1 💣 2 1 1 .
4   . . . . 1 2 3 💣 1 .
5   1 1 1 . . 1 💣 █ 1 .
6   █ 💣 2 . . 1 2 █ 1 .
7   █ 💣 2 . . . 1 💣 1 .
8   █ █ 3 2 1 . 1 2 3 2
9   █ █ 💣 💣 1 . . 1 💣 💣


(7, 5)
    0 1 2 3 4 5 6 7 8 9
0   . . . . . . . . . .
1   . . . . . . . . . .
2   . . . . 1 1 1 . . .
3   . . . . 1 💣 2 1 1 .
4   . . . . 1 2 3 💣 1 .
5   1 1 1 . . 1 💣 2 1 .
6   █ 💣 2 . . 1 2 █ 1 .
7   █ 💣 2 . . . 1 💣 1 .
8   █ █ 3 2 1 . 1 2 3 2
9   █ █ 💣 💣 1 . . 1 💣 💣


(0, 6)
    0 1 2 3 4 5 6 7 8 9
0   . . . . . . . . . .
1   . . . . . . . . . .
2   . . . . 1 1 1 . . .
3   . . . . 1 💣 2 1 1 .
4   . . . . 1 2 3 💣 1 .
5   1 1 1 . . 1 💣 2 1 .
6   2 💣 2 . . 1 2 █ 1 .
7   █ 💣 2 . . . 1 💣 1 .
8   █ █ 3 2 1 . 1 2 3 2
9   █ █ 💣 💣 1 . . 1 💣 💣


(7, 6)
    0 1 2 3 4 5 6 7 8 9
0   . . . . . . . . . .
1   . . . . . . . . . .
2   . . . . 1 1 1 . . .
3   . . . . 1 💣 2 1 1 .
4   . . . . 1 2 3 💣 1 .
5   1 1 1 . . 1 💣 2 1 .
6   2 💣 2 . . 1 2 2 1 .
7   █ 💣 2 . . . 1 💣 1 .
8   █ █ 3 2 1 . 1 2 3 2
9   █ █ 💣 💣 1 . . 1 💣 💣


(1, 8)
    0 1 2 3 4 5 6 7 8 9
0   . . . . . . . . . .
1   . . . . . . . . . .
2   . . . . 1 1 1 . . .
3   . . . . 1 💣 2 1 1 .
4   . . . . 1 2 3 💣 1 .
5   1 1 1 . . 1 💣 2 1 .
6   2 💣 2 . . 1 2 2 1 .
7   █ 💣 2 . . . 1 💣 1 .
8   █ 2 3 2 1 . 1 2 3 2
9   █ █ 💣 💣 1 . . 1 💣 💣


(1, 9)
    0 1 2 3 4 5 6 7 8 9
0   . . . . . . . . . .
1   . . . . . . . . . .
2   . . . . 1 1 1 . . .
3   . . . . 1 💣 2 1 1 .
4   . . . . 1 2 3 💣 1 .
5   1 1 1 . . 1 💣 2 1 .
6   2 💣 2 . . 1 2 2 1 .
7   █ 💣 2 . . . 1 💣 1 .
8   █ 2 3 2 1 . 1 2 3 2
9   █ 1 💣 💣 1 . . 1 💣 💣


simplifying rules
safe_guess [(0, 7), (0, 8), (0, 9)]
(0, 7)
    0 1 2 3 4 5 6 7 8 9
0   . . . . . . . . . .
1   . . . . . . . . . .
2   . . . . 1 1 1 . . .
3   . . . . 1 💣 2 1 1 .
4   . . . . 1 2 3 💣 1 .
5   1 1 1 . . 1 💣 2 1 .
6   2 💣 2 . . 1 2 2 1 .
7   2 💣 2 . . . 1 💣 1 .
8   █ 2 3 2 1 . 1 2 3 2
9   █ 1 💣 💣 1 . . 1 💣 💣


(0, 8)
    0 1 2 3 4 5 6 7 8 9
0   . . . . . . . . . .
1   . . . . . . . . . .
2   . . . . 1 1 1 . . .
3   . . . . 1 💣 2 1 1 .
4   . . . . 1 2 3 💣 1 .
5   1 1 1 . . 1 💣 2 1 .
6   2 💣 2 . . 1 2 2 1 .
7   2 💣 2 . . . 1 💣 1 .
8   1 2 3 2 1 . 1 2 3 2
9   █ 1 💣 💣 1 . . 1 💣 💣


(0, 9)
    0 1 2 3 4 5 6 7 8 9
0   . . . . . . . . . .
1   . . . . . . . . . .
2   . . . . 1 1 1 . . .
3   . . . . 1 💣 2 1 1 .
4   . . . . 1 2 3 💣 1 .
5   1 1 1 . . 1 💣 2 1 .
6   2 💣 2 . . 1 2 2 1 .
7   2 💣 2 . . . 1 💣 1 .
8   1 2 3 2 1 . 1 2 3 2
9   . 1 💣 💣 1 . . 1 💣 💣


you win!
```

### Unsatisfiable


### Strengths:
- Consistently solves all games unless unsatisfiable

### Weaknesses:
- If the game reaches a point where the constraints cannot decipher a safe
move, the game stops (All further moves require probability/random guessing)
