from django.contrib import auth
from rest_framework import status

from api.tests import BaseAPITestCase
from api.v1.user_auth import urls
from api.v1.user_auth.serializers import UserDetailSerializer


class RegisterAPITestCase(BaseAPITestCase):
    url_name = urls.REGISTER

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
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ProfileDetailAPITestCase(BaseAPITestCase):
    url_name = urls.PROFILE

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
            headers={"Authorization": f"Bearer {token_value}"}
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


    def test_other_auth_method_provided(self):
        """If bearer token provided, should return 401
        and no user data"""
        token_value = self.get_user_token_value()
        response = self.client.get(
            self.get_url(),
            headers={"Authorization": f"Token {token_value}"}
        )

        self.assertNotIn("username", response.json())
