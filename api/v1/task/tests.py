from rest_framework import status

from api.tests import BaseAuthTestCase
from task.maze.maze import BINARY_TREE
from task.models import MazeGenerationTask


class StartGenerationCreationTest(BaseAuthTestCase):
    url_name = "v1-maze-generate"

    def test_create_task_success(self):
        """Should create a task if authenticated and provided data is correct"""
        response = self.client.post(
            self.get_url(),
            {
                "name": "maze1",
                "width": 50,
                "height": 50,
                "algorithm": BINARY_TREE
            },
            headers={"Authorization": f"Token {self.get_user_token_value()}"}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MazeGenerationTask.objects.count(), 1)

    def test_create_task_invalid_data(self):
        """Should return bad request if invalid value is provided"""
        response = self.client.post(
            self.get_url(),
            {
                "name": "maze1",
                "width": 5,  # Invalid width value
                "height": 50,
                "algorithm": BINARY_TREE
            },
            headers={"Authorization": f"Token {self.get_user_token_value()}"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(MazeGenerationTask.objects.count(), 0)

    def test_create_task_unauthorized(self):
        """Should return unauthorized if token is not provided"""
        response = self.client.post(
            self.get_url(),
            {
                "name": "maze1",
                "width": 50,
                "height": 50,
                "algorithm": BINARY_TREE
            })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(MazeGenerationTask.objects.count(), 0)


class AlgorithmChoicesTestCase(BaseAuthTestCase):
    url_name = "v1-maze-algorithms"

    def test_get_choices_success(self):
        """Should return a list containing all algorithms"""
        response = self.client.get(self.get_url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data, list))
