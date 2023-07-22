class CellValueError(ValueError):
    pass


class Cell:
    """Grid cell"""

    def __init__(self, row_index, column_index, rows, columns):
        """
        row_index: cell row index.
        column_index: cell column index.
        rows: number of rows in grid.
        columns: number of columns in grid.
        """
        if row_index >= rows or row_index < 0:
            raise CellValueError(f"Expected a row index in range(0, {rows}) exclusive, got {row_index}")
        if column_index >= columns or column_index < 0:
            raise CellValueError(f"Expected a column index in range(0, {columns} exclusive, got {column_index}")

        self.row = row_index
        self.column = column_index
        self.rows = rows
        self.columns = columns
        self.linked_cells = set()

    def get_neighbors(self, grid):
        """Return North, South, East, West neighboring cells"""
        neighbors = []
        row, column = self.row, self.column

        # North
        if row > 0:
            neighbors.append(grid[row - 1][column])
        else:
            neighbors.append(0)

        # South
        if row < self.rows - 1:
            neighbors.append(grid[row + 1][column])
        else:
            neighbors.append(0)

        # East
        if column < self.columns - 1:
            neighbors.append(grid[row][column + 1])
        else:
            neighbors.append(0)

        # West
        if column > 0:
            neighbors.append(grid[row][column - 1])  # West
        else:
            neighbors.append(0)

        return neighbors

    def link(self, other, grid):
        """Link 2 unconnected cells."""
        # if self in other.linked_cells or other in self.linked_cells:
        #     raise CellValueError(f"{self} and {other} are already connected.")
        # if self.columns != other.columns or self.rows != other.columns:
        #     raise CellValueError("Cannot connect cells in different grids.")
        # if self not in other.get_neighbors(grid) or other not in self.get_neighbors(grid):
        #     raise CellValueError(f"{self} and {other} are not neighbors and cannot be connected.")
        # if not isinstance(other, Cell):
        #     raise CellValueError(f"Cannot link Cell to {type(other)}.")
        self.linked_cells.add(other)
        other.linked_cells.add(self)

    def unlink(self, other):
        """Unlink 2 connected cells."""
        if self not in other.linked_cells or other not in self.linked_cells:
            raise CellValueError(f"{self} and {other} are not connected.")
        self.linked_cells.remove(other)
        other.linked_cells.remove(self)

    def coordinates(self):
        """Return cell (row, column)."""
        return self.row, self.column

    def is_linked(self, other):
        """Return True if 2 cells are linked."""
        return other in self.linked_cells

    def __str__(self):
        """Cell display."""
        return f"Cell{self.coordinates()}"

    def __repr__(self):
        """Cell representation."""
        return f"Cell{self.coordinates()}"
