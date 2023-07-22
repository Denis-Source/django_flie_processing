import base64
from io import BytesIO
from random import randint

from PIL import Image
from django.core.files.base import ContentFile
from django.test import TestCase

from task.maze.maze import BINARY_TREE, SIDEWINDER, ALDOUS_BRODER, WILSON, HUNT_AND_KILL, RECURSIVE_BACKTRACKER
from task.maze.maze import Maze
from task.maze.maze_depiction import MazeDepiction
from task.maze.utils import convert_to_64, base64_file, image_to_file


class MazeTestCase(TestCase):
    def setUp(self) -> None:
        self.maze_params = {
            "rows": 100,
            "columns": 100,
        }

    def test_binary_tree(self):
        """Should generate mezes with binary tree algorithm"""
        generated_maze = [cells for cells in
                          Maze(**self.maze_params).
                          generate_maze(BINARY_TREE)]

        self.assertGreater(len(generated_maze), 0)
        self.assertTrue(
            all(isinstance(cells, tuple) for cells in generated_maze))

    def test_sidewinder(self):
        """Should generate mezes with Sidewinder algorithm"""
        generated_maze = [cells for cells in
                          Maze(**self.maze_params).
                          generate_maze(SIDEWINDER)]

        self.assertGreater(len(generated_maze), 0)
        self.assertTrue(
            all(isinstance(cells, tuple) for cells in generated_maze))

    def test_aldous_broder(self):
        """Should generate mezes with Aldous Broder algorithm"""
        generated_maze = [cells for cells in
                          Maze(**self.maze_params).
                          generate_maze(ALDOUS_BRODER)]

        self.assertGreater(len(generated_maze), 0)
        self.assertTrue(
            all(isinstance(cells, tuple) for cells in generated_maze))

    def test_wilson(self):
        """Should generate mezes with Wilson algorithm"""
        generated_maze = [cells for cells in
                          Maze(**self.maze_params).
                          generate_maze(WILSON)]

        self.assertGreater(len(generated_maze), 0)
        self.assertTrue(
            all(isinstance(cells, tuple) for cells in generated_maze))

    def test_hunt_and_kill(self):
        """Should generate mezes with Hunt and Kill algorithm"""
        generated_maze = [cells for cells in
                          Maze(**self.maze_params).
                          generate_maze(HUNT_AND_KILL)]

        self.assertGreater(len(generated_maze), 0)
        self.assertTrue(
            all(isinstance(cells, tuple) for cells in generated_maze))

    def test_recursive_backtracker(self):
        """Should generate mezes with a recursive backtracker"""
        generated_maze = [cells for cells in
                          Maze(**self.maze_params).
                          generate_maze(RECURSIVE_BACKTRACKER)]

        self.assertGreater(len(generated_maze), 0)
        self.assertTrue(
            all(isinstance(cells, tuple) for cells in generated_maze))


class MazeDepictionTestCase(TestCase):
    def setUp(self):
        self.maze_params = {
            "rows": 100,
            "columns": 100,
        }
        self.maze = Maze(**self.maze_params)

    def test_image_generator(self):
        """Should generate a stream of images"""
        depiction = MazeDepiction(
            self.maze.columns,
            self.maze.rows,
        )
        images = [depiction.generate_image(cells) for cells in self.maze.generate_maze(BINARY_TREE)]
        self.assertTrue(all([isinstance(image, Image.Image) for image in images]))


class UtilsTestCase(TestCase):
    @staticmethod
    def _generate_noisy_image(image, noise_intensity=30):
        width, height = image.size
        for y in range(height):
            for x in range(width):
                r, g, b = image.getpixel((x, y))
                noise_r = randint(-noise_intensity, noise_intensity)
                noise_g = randint(-noise_intensity, noise_intensity)
                noise_b = randint(-noise_intensity, noise_intensity)

                r = max(0, min(255, r + noise_r))
                g = max(0, min(255, g + noise_g))
                b = max(0, min(255, b + noise_b))
                image.putpixel((x, y), (r, g, b))
        return image

    def setUp(self):
        self.image = self._generate_noisy_image(
            Image.new("RGB", (100, 100), "white")
        )

    def test_to_64(self):
        """Should convert an image into a base64 string"""
        base64image = convert_to_64(self.image)

        result_image = base64.b64decode(base64image)
        result_image = Image.open(BytesIO(result_image))
        self.assertIsInstance(result_image, Image.Image)
        width, height = self.image.size
        self.assertEqual(
        [self.image.getpixel((x, y)) for x in range(width) for y in range(height)],
        [result_image.getpixel((x, y)) for x in range(width) for y in range(height)],)

    def test_from_64(self):
        """Should convert a base64 string into a Django suitable file format"""
        buffer = BytesIO()
        self.image.save(buffer, format="png", quality=100)
        base64str = base64.b64encode(buffer.getvalue()).decode()

        file = base64_file(base64str)
        self.assertIsInstance(file, ContentFile)

    def test_image_to_file(self):
        """Should convert a pillow image to Django suitable file format"""
        file  = image_to_file(self.image)
        self.assertIsInstance(file, ContentFile)
