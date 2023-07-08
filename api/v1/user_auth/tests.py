from django.contrib import auth
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token

from api.v1.user_auth.serializers import UserDetailSerializer
from user.models import User


class BaseAuthTestCase(TestCase):
    client = Client()
    url_name = None

    def setUp(self) -> None:
        """Creates a user in db with listed the data"""
        self.user_password = "SeccureP4assw0rd"
        self.user_name = "Cool_user"
        self.user_email = f"{self.user_name}@cool.mail"

        self.user = User.objects.create_user(
            username=self.user_name,
            email=self.user_name,
            password=self.user_password
        )

    def get_url(self):
        """Gets api endpoint url based on specified class variable"""
        return reverse(self.url_name)

    def logged_user_response(self):
        """Logins user, gets authorized response which includes a token"""
        return self.client.post(
            reverse("v1-login"),
            {
                "username": self.user_name,
                "password": self.user_password
            }
        )

    def get_user_token_value(self):
        """Gets token from a logged response"""
        response = self.logged_user_response()
        response_json = response.json()
        self.client.logout()

        return response_json.get("token")


class RegisterAuthTestCase(BaseAuthTestCase):
    url_name = "v1-register"

    def test_registration_already_exists(self):
        """If the user is already registered, should return 400 status"""
        response = self.client.post(
            self.get_url(),
            {
                "username": self.user_name,
                "email": self.user_email,
                "password": self.user_password
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_success(self):
        """If the user data is correct, should create a new user,
        return 201 status, and provide a valid token"""
        response = self.client.post(
            self.get_url(),
            {
                "username": "Another_Cool_user",
                "email": "SupaCool@cool.mail",
                "password": self.user_password
            }
        )
        user = auth.get_user(self.client)
        token = Token.objects.get(key=response.json()["token"])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(token.user, user)


class LoginAuthTestCase(BaseAuthTestCase):
    url_name = "v1-login"

    def test_login_success(self):
        """If provided data is correct, should return 200 status
        and provide a valid token"""
        response = self.client.post(
            self.get_url(),
            {
                "username": self.user_name,
                "password": self.user_password
            }
        )

        user = auth.get_user(self.client)
        token = Token.objects.get(key=response.json()["token"])

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(token.user, user)

    def test_login_wrong_password(self):
        """If the password is not correct, should return 400 status"""
        response = self.client.post(
            self.get_url(),
            {
                "username": self.user_name,
                "password": "wrongpassword"
            }
        )

        user = auth.get_user(self.client)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_user_not_exist(self):
        """If the username is not correct, should return 404 status"""
        response = self.client.post(
            self.get_url(),
            {
                "username": "nonexistentuser",
                "password": self.user_password
            }
        )

        user = auth.get_user(self.client)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ProfileDetailAuthTestCase(BaseAuthTestCase):
    url_name = "v1-profile"

    def test_not_authenticated(self):
        """If user is not authorized, should return 401 status"""
        response = self.client.get(
            self.get_url()
        )

        user = auth.get_user(self.client)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_authenticated(self):
        """If user is authorized, should return 200 and user profile info"""
        token_value = self.get_user_token_value()
        response = self.client.get(
            self.get_url(),
            headers={"Authorization": f"Token {token_value}"}
        )

        expected_data = UserDetailSerializer(self.user).data
        self.assertEqual(response.json(), expected_data)

    def test_token_not_provided(self):
        """If the token is not provided, should return status 401
         and no userdata"""
        response = self.client.get(
            self.get_url(),
        )
        user = auth.get_user(self.client)
        self.assertNotIn("username", response.json())

    def test_token_not_exist(self):
        """If the token is provided but not correct, should return 401
        and no userdata"""
        token_value = "b4d7b3c7ebe1f91a53ee2357a2ae8a8e6be43b1e"  # Not correct

        response = self.client.get(
            self.get_url(),
            headers={"Authorization": f"Token {token_value}"}
        )
        user = auth.get_user(self.client)
        self.assertNotIn("username", response.json())

    def test_other_auth_method_provided(self):
        """If bearer token provided, should return 401
        and no user data"""
        token_value = self.get_user_token_value()
        response = self.client.get(
            self.get_url(),
            headers={"Authorization": f"Bearer {token_value}"}
        )

        self.assertNotIn("username", response.json())
