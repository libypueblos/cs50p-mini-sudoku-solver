# 6x6 MINI-SUDOKU PUZZLE SOLVER
#### Video Demo:  <https://youtu.be/JaJkcMSjBNc>
#### Description: This project is a command-line Python application that solves a beginner-friendly mini-Sudoku puzzle using constraint elimination. The program reads a puzzle grid from a text file, analyzes all unsolved cells, and iteratively narrows down candidate values based on row, column, and sub-box constraints until the puzzle is solved or no further progress can be made. A *pytest test suite* is included to verify correctness, validate error handling, and ensure solver reliability on select puzzle scenarios.

The goal of this project is to demonstrate:
- structured program design
- object-oriented modeling
- defensive input validation
- automated testing practices

Rather than using brute-force guessing or recursive backtracking, the solver uses candidate tracking and constraint propagation to narrow down valid values for each cell.

The puzzle format is fixed at a *6×6 grid*, with sub-boxes sized *2 rows by 3 columns*. Empty cells are represented by 0 in the input text file.


## Core Program Overview

The project is organized around a central *Puzzle* class and a set of helper functions that manage file input, validation, and grid transformation. Responsibilities are deliberately separated so each stage of processing can be tested independently.

#### High-level pipeline:

    file input → validation → grid transformation → candidate initialization → constraint solving → printing solution status with the resulting puzzle grid

## Puzzle Class

The Puzzle class encapsulates the grid state and all solving behavior.

### Key Responsibilities

- tracking unsolved cells
- managing candidate values
- applying constraint rules
- determining solved status

When initialized, the class receives a 2D integer grid and immediately builds a candidate list for every empty cell. Each unsolved coordinate is mapped to all possible values from *1 through 6*.

### Important Methods

- #### `__init__(grid)`
  Initializes the puzzle with a provided grid and prepares candidate lists for all empty cells.

- #### `initialize_solution_candidates()`
  Builds a dictionary where each empty cell is mapped to all possible values (1–6). These candidates are later reduced through constraint checks.

- #### `solve()`
  Main solving loop. Repeatedly:
    - Checks if the puzzle is complete
    - Eliminates invalid candidates based on solved cells
    - Searches for cells that now have exactly one candidate

      The loop stops when the puzzle is solved or when no new cell solutions can be found.

- #### `update_solution_candidates(row, col, num)`
  Removes a confirmed number from candidate lists in the same row, column, and sub-box.

- #### `remove_candidate(r, c, num)`
  Safely removes a number from a specific cell’s candidate list if present.

- #### `new_cell_solution_found()`
  Detects cells with exactly one remaining candidate, writes that value into the grid, and removes the cell from the candidate dictionary.

- #### `is_solved()`
  Returns True when no unsolved cells remain.

- #### `print_results(status)`
  Prints whether the puzzle was successfully solved.

The class also uses property getters and setters for puzzle_grid, solution_candidates, and solved to keep state management explicit and controlled.


## Input and Validation Functions
The following are three additional functions besides the *main* function:

- #### `import_grid()`

  Reads the puzzle file specified via command-line argument and performs strict validation:

    - Requires exactly one argument
    - Filename must be longer than .txt
    - File must end with .txt
    - File must exist
    - File must not be empty

    Clear exceptions are raised for each failure case so both users and automated tests can verify exact failure reasons.

- #### `validate_grid()`

  Checks the structural correctness of the puzzle:

    - Grid must contain exactly 6 rows
    - Grid must contain exactly 6 columns
    - Only valid digits, i.e., `0 to 6`, are allowed

    This validation aims to prevent corrupted puzzle grid input from reaching later solving stages.

- #### `transform_grid()`

  Converts the validated text-based grid into a 2D list of integers used internally by the solver. Separating transformation from validation keeps responsibilities clean and makes each step independently testable.


## Automated Testing with Pytest

A dedicated pytest suite validates both normal and failure behavior. Tests cover:

- command-line handling
- file validation
- grid validation
- transformation correctness
- solver outcomes

Pytest’s monkeypatch fixture is used to override `sys.argv`, allowing command-line scenarios to be tested without invoking the script through a shell.

### Test Coverage

- #### `test_import_grid`
  Verifies argument and file validation logic:
  - Too few arguments
  - Too many arguments
  - Invalid filename length
  - Wrong file extension
  - Empty file
  - Missing file

  Each case confirms the correct exception and message are raised.

- #### `test_validate_grid`
  Checks structural grid validation:
  - Fewer or more than 6 rows
  - Fewer or more than 6 columns
  - Invalid cell values

  Malformed puzzles are rejected early.

- #### `test_transform_grid`
  Confirms that sample puzzle files are correctly converted into expected 2D integer arrays using exact equality assertions.

- #### `test_puzzle`
  Integration-style test of the full solving pipeline:
  - Puzzle 1 solves successfully
  - Puzzle 2 solves successfully
  - Puzzle 3 reports unsolved status

  This verifies both positive and negative solver outcomes.


## ▶️ Usage

#### Run from the command line:

```bash
python project.py puzzle.txt
```
Where *puzzle.txt* contains a 6×6 grid with zeros representing empty cells, like so:
```
000500
004030
005020
020001
012345
000000
```

#### Output:

```bash
Puzzle solved!
[2, 3, 1, 5, 6, 4]
[5, 6, 4, 1, 3, 2]
[1, 4, 5, 6, 2, 3]
[3, 2, 6, 4, 5, 1]
[6, 1, 2, 3, 4, 5]
[4, 5, 3, 2, 1, 6]
```

#### Run from the command line:
```bash
pytest test_project.py
```

## Design Notes

One major design decision was to use constraint propagation instead of brute-force search. The solver does not guess values or backtrack. Instead, it keeps a live candidate list for every empty cell and removes invalid numbers whenever a related cell is solved. This makes the algorithm easier to reason about and efficient for appropriately designed puzzles, though it may not solve puzzles that require guessing.

Another deliberate choice was storing candidate lists in a dictionary keyed by `"<row><column>"` strings. This keeps lookup simple and avoids nested structures, making updates fast and readable.

Constants such as `GRID_SIZE`, `BOX_HEIGHT`, and `BOX_WIDTH` are defined at the top of the file so the puzzle dimensions are configurable in one place, improving maintainability.
