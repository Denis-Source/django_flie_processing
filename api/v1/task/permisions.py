from rest_framework.permissions import BasePermission

from task.models import Task
from user.models import User


class IsNotExceededOpenTasks(BasePermission):
    def has_permission(self, request, view):
        """If user has opened too many tasks he is not allowed"""
        return User.MAX_TASKS > len(Task.get_opened_tasks().filter(initiator=request.user))
