import base64
from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile
from django.test import TestCase

from task.maze.maze import BINARY_TREE, SIDEWINDER, ALDOUS_BRODER, WILSON, HUNT_AND_KILL, RECURSIVE_BACKTRACKER
from task.maze.maze import Maze
from task.maze.utils import convert_to_64, base64_file


class MazeTestCase(TestCase):
    def setUp(self) -> None:
        self.maze_params = {
            "rows": 100,
            "columns": 100,
            "width": 1000,
            "height": 1000,
        }
        self.step = 20

    def test_binary_tree(self):
        """Should generate mezes with binary tree algorithm"""
        mazes = [maze for maze in
                 Maze(**self.maze_params).
                 generate_maze(BINARY_TREE, self.step)]

        self.assertGreater(len(mazes), 0)
        self.assertTrue(
            all(isinstance(image, Image.Image) for image in mazes))

    def test_sidewinder(self):
        """Should generate mezes with Sidewinder algorithm"""
        mazes = [maze for maze in
                 Maze(**self.maze_params).
                 generate_maze(SIDEWINDER, self.step)]

        self.assertGreater(len(mazes), 0)
        self.assertTrue(
            all(isinstance(image, Image.Image) for image in mazes))

    def test_aldous_broder(self):
        """Should generate mezes with Aldous Broder algorithm"""
        mazes = [maze for maze in
                 Maze(**self.maze_params).
                 generate_maze(ALDOUS_BRODER, self.step)]

        self.assertGreater(len(mazes), 0)
        self.assertTrue(
            all(isinstance(image, Image.Image) for image in mazes))

    def test_wilson(self):
        """Should generate mezes with Wilson algorithm"""
        mazes = [maze for maze in
                 Maze(**self.maze_params).
                 generate_maze(WILSON, self.step)]

        self.assertGreater(len(mazes), 0)
        self.assertTrue(
            all(isinstance(image, Image.Image) for image in mazes))


    def test_hunt_and_kill(self):
        """Should generate mezes with Hunt and Kill algorithm"""
        mazes = [maze for maze in
                 Maze(**self.maze_params).
                 generate_maze(HUNT_AND_KILL, self.step)]

        self.assertGreater(len(mazes), 0)
        self.assertTrue(
            all(isinstance(image, Image.Image) for image in mazes))

    def test_recursive_backtracker(self):
        """Should generate mezes with a recursive backtracker"""
        mazes = [maze for maze in
                 Maze(**self.maze_params).
                 generate_maze(RECURSIVE_BACKTRACKER, self.step)]

        self.assertGreater(len(mazes), 0)
        self.assertTrue(
            all(isinstance(image, Image.Image) for image in mazes))

    def test_to_64(self):
        """Should convert an image into a base64 string"""
        maze = [maze for maze in
                Maze(**self.maze_params).
                generate_maze(WILSON, self.step)][0]
        base64maze = convert_to_64(maze)

        image = base64.b64decode(base64maze)
        image = Image.open(BytesIO(image))
        self.assertTrue(isinstance(image, Image.Image))

    def test_from_64(self):
        """Should convert a base64 string into a Django suitable file format"""
        maze = [maze for maze in
                Maze(**self.maze_params).
                generate_maze(WILSON, self.step)][0]

        buffer = BytesIO()
        maze.save(buffer, format="png", quality=100)
        base64str = base64.b64encode(buffer.getvalue()).decode()

        image = base64_file(base64str)
        self.assertTrue(isinstance(image, ContentFile))
