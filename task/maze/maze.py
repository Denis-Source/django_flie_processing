import random

from PIL import Image, ImageDraw

from .cell import Cell
from .depiction import Depiction

BINARY_TREE = "binary_tree"
SIDEWINDER = "sidewinder"
ALDOUS_BRODER = "aldous_broder"
WILSON = "wilson"
HUNT_AND_KILL = "hunt_and_kill"
RECURSIVE_BACKTRACKER = "recursive_backtracker"


class MazeValueError(ValueError):
    pass


class Maze:
    """
    Generate a maze using different algorithms:
    - Binary Tree Algorithm.
    - Sidewinder Algorithm.
    - Aldous-Broder Algorithm.
    - Wilson Algorithm.
    - Hunt And Kill Algorithm.
    - Recursive Backtracker Algorithm.
    """

    def __init__(self, rows, columns, width, height, line_width=5, line_color="black", background_color="white"):
        if width % columns != 0:
            raise MazeValueError(f"Width: {width} not divisible by number of columns: {columns}.")
        if height % rows != 0:
            raise MazeValueError(f"Height: {height} not divisible by number of {rows}.")
        self.rows = rows
        self.columns = columns
        self.width = width
        self.height = height
        self.line_width = line_width
        self.line_color = line_color
        self.background_color = background_color
        self.cell_width = width // columns
        self.cell_height = height // rows
        self.drawing_constant = line_width // 2

        self.algorithms = {
            BINARY_TREE: self._binary_tree_generation,
            SIDEWINDER: self._side_winder_generation,
            ALDOUS_BRODER: self._aldous_broder_generation,
            WILSON: self._wilson_generation,
            HUNT_AND_KILL: self._hunt_and_kill_generation,
            RECURSIVE_BACKTRACKER: self._recursive_back_tracker_generation
        }

    def _create_maze_cells(self):
        """Return maze cells."""
        return [[Cell(row, column, self.rows, self.columns) for column in range(self.columns)]
                for row in range(self.rows)]

    def _get_dead_ends(self, maze):
        """Make a 2D list containing finished maze
        Return dead end cells in the current maze
        """
        return {cell for row in maze for cell in row if len(cell.linked_cells) == 1 and
                str(cell) != str(maze[-1][-1])}

    def _binary_tree_generation(self):
        """Generate a maze using binary tree"""
        maze_cells = self._create_maze_cells()
        for row in range(self.rows):
            for column in range(self.columns):
                current_cell = maze_cells[row][column]
                north, south, east, west = current_cell.get_neighbors(maze_cells)
                to_link = random.choice("nw")
                if not north and not west:
                    continue
                if to_link == "n" and north:
                    current_cell.link(north, maze_cells)
                    yield current_cell, north
                if to_link == "w" and west:
                    current_cell.link(west, maze_cells)
                    yield current_cell, west
                if to_link == "n" and not north:
                    current_cell.link(west, maze_cells)
                    yield current_cell, west
                if to_link == "w" and not west:
                    current_cell.link(north, maze_cells)
                    yield current_cell, north

    def _side_winder_generation(self):
        """Generate a maze using sidewinder algorithm"""
        maze_cells = self._create_maze_cells()
        checked_cells = []
        for row in range(self.rows):
            for column in range(self.columns):
                current_cell = maze_cells[row][column]
                north, south, east, west = current_cell.get_neighbors(maze_cells)
                if row == 0 and east:
                    east_cell = maze_cells[row][column + 1]
                    current_cell.link(east_cell, maze_cells)
                    yield current_cell, east_cell
                if row != 0:
                    checked_cells.append(current_cell)
                    to_link = random.choice("ne")
                    if to_link == "e" and east:
                        east_cell = maze_cells[row][column + 1]
                        current_cell.link(east_cell, maze_cells)
                        yield current_cell, east_cell
                    if to_link == "n" or (to_link == "e" and not east):
                        random_cell = random.choice(checked_cells)
                        checked_cells.clear()
                        random_cell_coordinates = random_cell.coordinates()
                        random_cell_north_neighbor = maze_cells[random_cell_coordinates[0] - 1][
                            random_cell_coordinates[1]]
                        random_cell.link(random_cell_north_neighbor, maze_cells)
                        modified_cells.append((random_cell, random_cell_north_neighbor))
                        yield modified_cells

    def _aldous_broder_generation(self):
        """Generate a maze using Aldous Broder algorithm"""
        maze_cells = self._create_maze_cells()
        modified_cells = []
        starting_cell = maze_cells[random.choice(range(self.rows))][random.choice(range(self.columns))]
        visited = set()
        run = [starting_cell]
        while len(visited) < self.rows * self.columns:
            current_cell = run[-1]
            visited.add(current_cell)
            random_neighbor = random.choice([
                neighbor for neighbor in current_cell.get_neighbors(maze_cells) if neighbor])
            if random_neighbor not in visited:
                visited.add(random_neighbor)
                run.append(random_neighbor)
                current_cell.link(random_neighbor, maze_cells)
                modified_cells.append((current_cell, random_neighbor))
            if random_neighbor in visited:
                run.clear()
                run.append(random_neighbor)

            yield modified_cells

    def _wilson_generation(self):
        """Generate a maze using Wilson algorithm"""
        maze_cells = self._create_maze_cells()
        unvisited = {cell for row in maze_cells for cell in row}
        starting_cell = random.choice(list(unvisited))
        unvisited.remove(starting_cell)
        visited = {starting_cell}
        path = [random.choice(list(unvisited))]
        unvisited.remove(path[-1])
        modified_cells = []
        while unvisited:
            current_cell = path[-1]
            new_cell = random.choice([neighbor for neighbor in current_cell.get_neighbors(maze_cells) if neighbor])
            if new_cell in path and new_cell not in visited:
                to_erase_from = path.index(new_cell)
                del path[to_erase_from + 1:]
            if new_cell in visited:
                for cell in path:
                    visited.add(cell)
                    if cell in unvisited:
                        unvisited.remove(cell)
                path.append(new_cell)
                for index in range(len(path) - 1):
                    path[index].link(path[index + 1], maze_cells)
                    modified_cells.append((path[index], path[index + 1]))
                path.clear()
                if unvisited:
                    path.append(random.choice(list(unvisited)))
            if new_cell not in path and new_cell not in visited:
                path.append(new_cell)

            yield modified_cells

    def _hunt_and_kill_generation(self):
        """Generate a maze using hunt and kill algorithm"""
        maze_cells = self._create_maze_cells()
        unvisited = [cell for row in maze_cells for cell in row]
        starting_cell = random.choice(list(unvisited))
        visited = [starting_cell]
        unvisited.remove(starting_cell)
        run = [starting_cell]
        modified_cells = []
        while unvisited:
            current_cell = run[-1]
            valid_neighbors = [neighbor for neighbor in current_cell.get_neighbors(maze_cells) if neighbor in unvisited]
            if valid_neighbors:
                next_cell = random.choice(valid_neighbors)
                current_cell.link(next_cell, maze_cells)
                modified_cells.append((current_cell, next_cell))
                yield modified_cells
                visited.append(next_cell)
                unvisited.remove(next_cell)
                run.append(next_cell)
            if not valid_neighbors:
                for cell in unvisited:
                    valid_neighbors = [neighbor for neighbor in cell.get_neighbors(maze_cells) if neighbor in visited]
                    if valid_neighbors:
                        choice = random.choice(valid_neighbors)
                        cell.link(choice, maze_cells)
                        modified_cells.append((cell, choice))
                        yield modified_cells
                        unvisited.remove(cell)
                        visited.append(cell)
                        run.append(cell)
                        break

    def _recursive_back_tracker_generation(self):
        """Generate a maze using a recursive backtracker"""
        maze_cells = self._create_maze_cells()
        unvisited = [cell for row in maze_cells for cell in row]
        starting_cell = random.choice(unvisited)
        unvisited.remove(starting_cell)
        run = [starting_cell]
        modified = []
        while run:
            current_cell = run[-1]
            valid_neighbors = [neighbor for neighbor in current_cell.get_neighbors(maze_cells) if neighbor in unvisited]
            if valid_neighbors:
                next_cell = random.choice(valid_neighbors)
                current_cell.link(next_cell, maze_cells)
                modified.append((current_cell, next_cell))
                unvisited.remove(next_cell)
                run.append(next_cell)
            if not valid_neighbors:
                run.pop()
        dead_ends = self._get_dead_ends(maze_cells)
        return modified, dead_ends

    def generate_maze(self, algorithm):
        """Generate a maze continuously
        yields an image every specified step
        """
        if algorithm not in self.algorithms:
            raise MazeValueError(f"Invalid configuration {algorithm}")

        depiction = Depiction(
            self.columns,
            self.rows
        )
        for cells in self.algorithms[algorithm]():
            yield depiction.generate_image(cells)

        yield depiction.put_dots()