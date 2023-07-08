from django.contrib import auth
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token

from core import settings
from user.models import User


class AuthTestCase(TestCase):
    client = Client()

    def setUp(self) -> None:
        self.user_password = "SeccureP4assw0rd"
        self.user_name = "Cool_user"
        self.user_email = f"{self.user_name}@cool.mail"

        self.user = User.objects.create_user(
            username=self.user_name,
            email=self.user_name,
            password=self.user_password
        )

    def login_user(self):
        url = reverse("v1-login")

        return self.client.post(
            url,
            {
                "username": self.user_name,
                "password": self.user_password
            }
        )

    def test_registration_already_exists(self):
        url = reverse("v1-register")
        response = self.client.post(
            url,
            {
                "username": self.user_name,
                "email": self.user_email,
                "password": self.user_password
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_success(self):
        url = reverse("v1-register")
        response = self.client.post(
            url,
            {
                "username": "Another_Cool_user",
                "email": "SupaCool@cool.mail",
                "password": self.user_password
            }
        )
        user = auth.get_user(self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(user.is_authenticated, True)

    def test_login_success(self):
        url = reverse("v1-login")

        response = self.client.post(
            url,
            {
                "username": self.user_name,
                "password": self.user_password
            }
        )

        user = auth.get_user(self.client)
        token = Token.objects.get(key=response.json()["token"])

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user.is_authenticated, True)
        self.assertEqual(token.user, user)

    def test_login_wrong_password(self):
        url = reverse("v1-login")

        response = self.client.post(
            url,
            {
                "username": self.user_name,
                "password": "wrongpassword"  # Incorrect password
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_user_not_exist(self):
        url = reverse("v1-login")

        response = self.client.post(
            url,
            {
                "username": "nonexistentuser",  # User does not exist
                "password": "testpassword"
            }
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)