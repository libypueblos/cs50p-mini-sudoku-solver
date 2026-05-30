import pytest
import sys
from project import import_grid, validate_grid, transform_grid, Puzzle


def test_import_grid(monkeypatch):
    # Test the behavior when less than 2 arguments are provided
    monkeypatch.setattr(sys, "argv", ["project.py"])
    with pytest.raises(Exception, match = "Too few command-line arguments"):
        import_grid()

    # Test the behavior when more than 2 arguments are provided
    monkeypatch.setattr(sys, "argv", ["project.py", "puzzle.txt", "hello"])
    with pytest.raises(Exception, match = "Too many command-line arguments"):
        import_grid()

    # Test the behavior when 2nd argument is not a valid txt file
    monkeypatch.setattr(sys, "argv", ["project.py", ".txt"])
    with pytest.raises(Exception, match = "Invalid command-line argument"):
        import_grid()

    # Test the behavior when 2nd argument is not a txt file
    monkeypatch.setattr(sys, "argv", ["project.py", "puzzle.py"])
    with pytest.raises(Exception, match = "Not a text file"):
        import_grid()

    # Test the behavior when puzzle file is empty
    monkeypatch.setattr(sys, "argv", ["project.py", "puzzle_empty.txt"])
    with pytest.raises(Exception, match = "Puzzle file is empty"):
        import_grid()

    # Test the behavior when puzzle file does not exist
    monkeypatch.setattr(sys, "argv", ["project.py", "puzzle_not_exist.txt"])
    with pytest.raises(Exception, match = "Puzzle file does not exist"):
        import_grid()


def test_validate_grid(monkeypatch):
    # Test the behavior when puzzle_grid has more rows than expected
    monkeypatch.setattr(sys, "argv", ["project.py", "puzzle_extra_rows.txt"])
    puzzle_grid = import_grid()
    with pytest.raises(Exception, match = "Puzzle has fewer or more than 6 rows"):
        validate_grid(puzzle_grid)

    # Test the behavior when puzzle_grid has more columns than expected
    monkeypatch.setattr(sys, "argv", ["project.py", "puzzle_extra_cols.txt"])
    puzzle_grid = import_grid()
    with pytest.raises(Exception, match = "Puzzle has fewer or more than 6 columns"):
        validate_grid(puzzle_grid)

    # Test the behavior when puzzle_grid has invalid value
    monkeypatch.setattr(sys, "argv", ["project.py", "puzzle_with_invalid_value.txt"])
    puzzle_grid = import_grid()
    with pytest.raises(Exception, match = "Puzzle has invalid value/s"):
        validate_grid(puzzle_grid)


def test_transform_grid(monkeypatch):
    # Puzzle 1
    monkeypatch.setattr(sys, "argv", ["project.py", "puzzle1.txt"])
    puzzle_grid = import_grid()
    puzzle_grid = validate_grid(puzzle_grid)
    puzzle_grid = transform_grid(puzzle_grid)
    assert puzzle_grid == [[0,0,0,0,0,0],[0,0,0,1,2,3],[0,0,2,0,1,0],[0,1,0,5,0,0],[4,2,3,0,0,0],[0,0,0,0,0,0]]

    # Puzzle 2
    monkeypatch.setattr(sys, "argv", ["project.py", "puzzle2.txt"])
    puzzle_grid = import_grid()
    puzzle_grid = validate_grid(puzzle_grid)
    puzzle_grid = transform_grid(puzzle_grid)
    assert puzzle_grid == [[0,0,0,5,0,0],[0,0,4,0,3,0],[0,0,5,0,2,0],[0,2,0,0,0,1],[0,1,2,3,4,5],[0,0,0,0,0,0]]

    # Puzzle 3
    monkeypatch.setattr(sys, "argv", ["project.py", "puzzle3.txt"])
    puzzle_grid = import_grid()
    puzzle_grid = validate_grid(puzzle_grid)
    puzzle_grid = transform_grid(puzzle_grid)
    assert puzzle_grid == [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]


def test_puzzle(monkeypatch):
    # Puzzle 1
    monkeypatch.setattr(sys, "argv", ["project.py", "puzzle1.txt"])
    puzzle_grid = import_grid()
    puzzle_grid = validate_grid(puzzle_grid)
    puzzle_grid = transform_grid(puzzle_grid)
    puzzle = Puzzle(puzzle_grid)
    solved = puzzle.solve()
    assert solved == True

    # Puzzle 2
    monkeypatch.setattr(sys, "argv", ["project.py", "puzzle2.txt"])
    puzzle_grid = import_grid()
    puzzle_grid = validate_grid(puzzle_grid)
    puzzle_grid = transform_grid(puzzle_grid)
    puzzle = Puzzle(puzzle_grid)
    solved = puzzle.solve()
    assert solved == True

    # Puzzle 3
    monkeypatch.setattr(sys, "argv", ["project.py", "puzzle3.txt"])
    puzzle_grid = import_grid()
    puzzle_grid = validate_grid(puzzle_grid)
    puzzle_grid = transform_grid(puzzle_grid)
    puzzle = Puzzle(puzzle_grid)
    solved = puzzle.solve()
    assert solved == False
