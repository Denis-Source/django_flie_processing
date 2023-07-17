from rest_framework import status

from api.tests import BaseAPITestCase
from task.maze.maze import BINARY_TREE
from task.models import MazeGenerationTask, Task


class BaseListTaskTestCase(BaseAPITestCase):
    def setUp(self) -> None:
        super().setUp()
        self.n = 100
        n_map = {
            0: Task.Statuses.CREATED,
            1: Task.Statuses.RUNNING,
            2: Task.Statuses.ERRORED,
            3: Task.Statuses.FINISHED,
            4: Task.Statuses.CREATED,
        }
        for i in range(self.n):
            task = Task(name="test", initiator=self.user)
            task.update_status(n_map[i % len(n_map)])
            task.save()

class ListHistoryTestCase(BaseListTaskTestCase):
    url_name = "v1-task-history"

    def test_history_success(self):
        """Should retrieve a list of task history"""
        response = self.client.get(
            self.get_url(),
            {
                "page_size": self.n
            },
            headers={"Authorization": f"Token {self.get_user_token_value()}"}
        )
        a = Task.get_opened_tasks()
        self.assertTrue(len(Task.get_closed_tasks().filter(initiator=self.user)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], Task.get_closed_tasks().filter(initiator=self.user).count())

    def test_history_unauthorized(self):
        """Should return unauthorized if token is not provided"""
        response = self.client.get(
            self.get_url()
            )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ListOpenedTestCase(BaseListTaskTestCase):
    url_name = "v1-task-opened"

    def test_opened_success(self):
        """Should retrieve a list of opened tasks"""
        response = self.client.get(
            self.get_url(),
            headers={"Authorization": f"Token {self.get_user_token_value()}"}
        )
        self.assertTrue(len(Task.get_closed_tasks().filter(initiator=self.user)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Task.get_opened_tasks().filter(initiator=self.user).count())

    def test_opened_unauthorized(self):
        """Should return unauthorized if token is not provided"""
        response = self.client.get(
            self.get_url(),
            )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class StartGenerationCreationTestCase(BaseAPITestCase):
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


class AlgorithmChoicesTestCase(BaseAPITestCase):
    url_name = "v1-maze-algorithms"

    def test_get_choices_success(self):
        """Should return a list containing all algorithms"""
        response = self.client.get(self.get_url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data, list))
