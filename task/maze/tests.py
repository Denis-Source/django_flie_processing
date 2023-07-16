import base64
from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile
from django.test import TestCase

from task.maze.maze import BINARY_TREE, SIDEWINDER, ALDOUS_BRODER, WILSON
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
        mazes = [maze for maze in
                 Maze(**self.maze_params).
                 generate_maze(BINARY_TREE, self.step)]

        self.assertGreater(len(mazes), 0)
        self.assertTrue(
            all(isinstance(image, Image.Image) for image in mazes))

    def test_sidewinder(self):
        mazes = [maze for maze in
                 Maze(**self.maze_params).
                 generate_maze(SIDEWINDER, self.step)]

        self.assertGreater(len(mazes), 0)
        self.assertTrue(
            all(isinstance(image, Image.Image) for image in mazes))

    def test_aldous_broder(self):
        mazes = [maze for maze in
                 Maze(**self.maze_params).
                 generate_maze(ALDOUS_BRODER, self.step)]

        self.assertGreater(len(mazes), 0)
        self.assertTrue(
            all(isinstance(image, Image.Image) for image in mazes))

    def test_binary_tree(self):
        mazes = [maze for maze in
                 Maze(**self.maze_params).
                 generate_maze(BINARY_TREE, self.step)]

        self.assertGreater(len(mazes), 0)
        self.assertTrue(
            all(isinstance(image, Image.Image) for image in mazes))

    def test_wilson(self):
        mazes = [maze for maze in
                 Maze(**self.maze_params).
                 generate_maze(WILSON, self.step)]

        self.assertGreater(len(mazes), 0)
        self.assertTrue(
            all(isinstance(image, Image.Image) for image in mazes))

    def test_to_64(self):
        maze = [maze for maze in
                Maze(**self.maze_params).
                generate_maze(WILSON, self.step)][0]
        base64maze = convert_to_64(maze)

        image = base64.b64decode(base64maze)
        image = Image.open(BytesIO(image))
        self.assertTrue(isinstance(image, Image.Image))

    def test_from_64(self):
        maze = [maze for maze in
                Maze(**self.maze_params).
                generate_maze(WILSON, self.step)][0]

        buffer = BytesIO()
        maze.save(buffer, format="png", quality=100)
        base64str = base64.b64encode(buffer.getvalue()).decode()

        image = base64_file(base64str)
        self.assertTrue(isinstance(image, ContentFile))
