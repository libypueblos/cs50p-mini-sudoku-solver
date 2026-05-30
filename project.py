import sys


GRID_SIZE = 6
BOX_HEIGHT = 2
BOX_WIDTH = 3


class Puzzle:
    def __init__(self, grid):
        self.solved = False
        self.puzzle_grid = grid
        self.initialize_solution_candidates()

    def initialize_solution_candidates(self):
        self.solution_candidates = {}
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if self.puzzle_grid[row][col] == 0:
                    self.solution_candidates[f"{row}{col}"] = list(range(1, GRID_SIZE+1))

    def solve(self):
        while self.solved == False:
            # Break loop when puzzle reaches a solution
            if self.is_solved() == True:
                self.solved = True
                break

            # For every digit in a solved cell, remove the digit from the solution_candidates of its related row, column, and box
            for row in range(GRID_SIZE):
                for col in range(GRID_SIZE):
                    if self.puzzle_grid[row][col] != 0:
                        self.update_solution_candidates(row, col, self.puzzle_grid[row][col])

            if self.new_cell_solution_found() == False:
                self.solved = False
                break

        return self.solved

    def new_cell_solution_found(self):
        # Check if new cell solution found and update solution_candidates accordingly
        resolve_puzzle = False
        solved_cells = []
        for key in self.solution_candidates:
            if len(self.solution_candidates[key]) == 1:  # New cell solution found!
                resolve_puzzle = True
                solved_cells.append(key)
                row = int(key[0])
                col = int(key[1])
                self.puzzle_grid[row][col] = self.solution_candidates[key][0]
                self.update_solution_candidates(row, col, self.solution_candidates[key][0])
        for key in solved_cells:
            del self.solution_candidates[key]

        # Return True if solution to a cell is found, else return False
        return resolve_puzzle

    def is_solved(self):
        if len(self.solution_candidates) == 0:
            return True
        return False

    def update_solution_candidates(self, row, col, num):
        # Update its related row and column
        for n in range(GRID_SIZE):
            self.remove_candidate(row, n, num)
            self.remove_candidate(n, col, num)

        # Update its related box
        row_start = (row // BOX_HEIGHT) * BOX_HEIGHT
        col_start = (col // BOX_WIDTH) * BOX_WIDTH
        for i in range(row_start, row_start + BOX_HEIGHT):
            for j in range(col_start, col_start + BOX_WIDTH):
                self.remove_candidate(i, j, num)

    def remove_candidate(self, r, c, num):
        # Remove a candidate number from a specific cell's list if it exists
        cell_key = f"{r}{c}"
        # Check if cell_key is in solution_candidates
        candidates = self.solution_candidates.get(cell_key, [])
        if num in candidates:
            candidates.remove(num)

    def print_results(self, status, grid):
        if status:
            print("Puzzle solved!")
        else:
            print("Puzzle has not reached a solution.")

        for row in grid:
            print(f"{row}")

    @property
    def puzzle_grid(self):
        return self._puzzle_grid

    @puzzle_grid.setter
    def puzzle_grid(self, grid):
        self._puzzle_grid = grid

    @property
    def solution_candidates(self):
        return self._solution_candidates

    @solution_candidates.setter
    def solution_candidates(self, dict):
        self._solution_candidates = dict

    @property
    def solved(self):
        return self._solved

    @solved.setter
    def solved(self, solved):
        self._solved = solved


def import_grid():
    puzzle_grid = []

    # User must input exactly one command-line argument
    if len(sys.argv) < 2:
        raise Exception("Too few command-line arguments")
    elif len(sys.argv) > 2:
        raise Exception("Too many command-line arguments")

    # Verify filename and exit program if invalid
    puzzle_file = sys.argv[1].strip().lower()
    if len(puzzle_file) <= 4:    # Filename cannot be spaces [len=0] and must be more than the minimum ".txt" [len=4]
        raise Exception("Invalid command-line argument")
    elif puzzle_file.endswith(".txt") == False:   # User input non-python file
        raise Exception("Not a text file")

    # Read puzzle file and store lines into a list
    try:
        with open(puzzle_file) as file:
            puzzle_grid = [line.strip() for line in file]
            if not puzzle_grid:
                raise Exception("Puzzle file is empty")
    except FileNotFoundError:
        raise FileNotFoundError("Puzzle file does not exist")

    # Output the grid
    return puzzle_grid


def validate_grid(puzzle_grid):
    # Number of rows must be six
    if len(puzzle_grid) < GRID_SIZE or len(puzzle_grid) > GRID_SIZE:
        raise Exception("Puzzle has fewer or more than 6 rows")

    for row in range(GRID_SIZE):
        # Number of columns must be six
        if len(puzzle_grid[row]) < GRID_SIZE or len(puzzle_grid[row]) > GRID_SIZE:
            raise Exception("Puzzle has fewer or more than 6 columns")
        # Each number in grid must be from 0 to 6 only
        for col in range(GRID_SIZE):
            if int(puzzle_grid[row][col]) not in range(GRID_SIZE+1):
                raise Exception("Puzzle has invalid value/s")

    # Output the grid
    return puzzle_grid


def transform_grid(puzzle_grid):
    # Transform grid into list of integers
    for i in range(GRID_SIZE):
        line = puzzle_grid[i]
        puzzle_grid[i] = []
        for j in range(GRID_SIZE):
            puzzle_grid[i].append(int(line[j]))

    # Output the grid
    return puzzle_grid


def main():
    # Import the puzzle grid from a file
    puzzle_grid = import_grid()
    validate_grid(puzzle_grid)
    transform_grid(puzzle_grid)

    # Instantiate a puzzle with the puzzle grid, and solve
    puzzle = Puzzle(puzzle_grid)
    status = puzzle.solve()

    # Print puzzle solution status and resulting puzzle grid
    puzzle.print_results(status, puzzle.puzzle_grid)

if __name__ == "__main__":
    main()
