from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Roles(models.TextChoices):
        USER = "user", "User"
        STAFF = "staff", "Staff"
        ADMIN = "admin", "Admin"

    email = models.EmailField(unique=True, verbose_name="Email")
    username = models.CharField(max_length=64, unique=True, verbose_name="Username")
    role = models.CharField(max_length=8, choices=Roles.choices, verbose_name="User role", default=Roles.USER)

    registered = models.DateTimeField(auto_now_add=True, verbose_name="Registered date")
    image = models.ImageField(verbose_name="Profile image", upload_to="user_images", null=True, blank=True)

    def __str__(self):
        return f"{self.role} {self.username}"
