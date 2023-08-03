import math
from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from core import settings
from task.models import Task
from user.models import User


class TaskTestCase(TestCase):
    def setUp(self):
        self.closing_statuses = [
            Task.Statuses.ERRORED,
            Task.Statuses.FINISHED,
            Task.Statuses.CANCELED
        ]

        self.not_closing_statuses = [
            Task.Statuses.CREATED,
            Task.Statuses.RUNNING
        ]

        self.user = User(
            email="test@mail.com",
            username="cool_test",
        )
        self.user.save()

    def test_update_status_closing(self):
        """Update status in a case of a task completion
        should set closing date"""
        for status in self.closing_statuses:
            task = Task(name="test_task", initiator=self.user)
            task.save()

            self.assertEqual(task.status, Task.Statuses.CREATED)
            task.update_status(status)
            self.assertEqual(task.status, status)
            self.assertTrue(task.closed_at)

    def test_update_status_not_closing(self):
        """Update status in other case should not set closing date"""
        for status in self.not_closing_statuses:
            task = Task(name="test_task", initiator=self.user)
            task.save()

            self.assertEqual(task.status, Task.Statuses.CREATED)
            task.update_status(status)
            self.assertEqual(task.status, status)
            self.assertFalse(task.closed_at)

    def test_update_status_wrong_value(self):
        """Update with an invalid status should raise an exception"""
        task = Task(name="test_task", initiator=self.user)
        task.save()
        invalid_status = "invalid status"
        self.assertRaises(ValueError, task.update_status, invalid_status)

    def test_get_stale_tasks(self):
        """Should return a list of tasks that are not completed
        and running for too long"""
        n = 100

        for i in range(n):
            task = Task(name="test_task", initiator=self.user)
            if i % 2 == 0:
                task.update_status(Task.Statuses.RUNNING)
            else:
                task.update_status(Task.Statuses.FINISHED)

            if i % 3 == 0:
                task.created_at = timezone.now() - timedelta(seconds=(settings.STALE_TASK_AGE + 10))
            task.save()

        query = Task.get_stale_tasks()
        expected = math.ceil(n / 2 / 3)
        self.assertEqual(len(query), expected)

    def generate_task_sample(self, n=100):
        self.assertTrue(n % len(Task.Statuses.choices) == 0)

        n_map = {
            0: Task.Statuses.CREATED,
            1: Task.Statuses.RUNNING,
            2: Task.Statuses.ERRORED,
            3: Task.Statuses.FINISHED,
            4: Task.Statuses.CREATED,
        }

        for i in range(n):
            task = Task(name="test_task", initiator=self.user)
            task.save()
            status = n_map[i % len(n_map)]
            task.update_status(status)

    def test_get_opened_tasks(self):
        """Should return tasks that are not completed"""
        n = 100
        self.generate_task_sample(n)

        query = Task.get_opened_tasks()

        expected = math.ceil(n / 5 * 3)
        self.assertEqual(len(query), expected)

    def test_get_closed_tasks(self):
        """Should return tasks that are completed"""
        n = 100
        self.generate_task_sample(n)

        query = Task.get_closed_tasks()
        expected = math.ceil(n / 5 * 2)
        self.assertEqual(len(query), expected)
