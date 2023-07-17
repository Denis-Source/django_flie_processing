from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    MAX_TASKS = 3
    class Roles(models.TextChoices):
        USER = "user", "User"
        STAFF = "staff", "Staff"
        ADMIN = "admin", "Admin"

    email = models.EmailField(unique=True, verbose_name="Email", help_text="Email of the user")
    username = models.CharField(max_length=64, unique=True, verbose_name="Username", help_text="The main distinguishing field")
    role = models.CharField(max_length=8, choices=Roles.choices, verbose_name="User role", default=Roles.USER, help_text="User assigned role, regular 'user' is by default")

    registered = models.DateTimeField(auto_now_add=True, verbose_name="Registered date", help_text="Automatically generated date and time of user registration")
    image = models.ImageField(verbose_name="Profile image", upload_to="user_images", null=True, blank=True, help_text="User profile picture")

    def __str__(self):
        return f"{self.role} {self.username}"
