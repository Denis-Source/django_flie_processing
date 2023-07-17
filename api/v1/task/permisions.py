from rest_framework.permissions import BasePermission

from task.models import Task
from user.models import User


class IsNotExceededOpenTasks(BasePermission):
    """Is user has not opened too many tasks"""
    def has_permission(self, request, view):
        return User.MAX_TASKS > len(Task.get_opened_tasks().filter(initiator=request.user))
