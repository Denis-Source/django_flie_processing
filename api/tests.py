from django.test import TestCase, Client
from django.urls import reverse

from api.v1.user_auth.urls import TOKEN_OBTAIN_PAIR
from user.models import User


class BaseAPITestCase(TestCase):
    client = Client()
    url_name = None

    def setUp(self) -> None:
        """Create a user in db with listed the data"""
        self.user_password = "SeccureP4assw0rd"
        self.user_name = "Cool_user"
        self.another_user_name = "Cool_user2"
        self.user_email = f"{self.user_name}@cool.mail"
        self.another_user_email = f"{self.another_user_name}@cool.mail"

        self.user = User.objects.create_user(
            username=self.user_name,
            email=self.user_name,
            password=self.user_password
        )
        self.another_user = User.objects.create_user(
            username=self.another_user_name,
            email=self.another_user_email,
            password=self.user_password
        )
        self.auth_headers = {"Authorization": f"Bearer {self.get_user_token_value()}"}

    def get_url(self, **kwargs):
        """Get api endpoint url based on specified class variable"""
        return reverse(self.url_name, kwargs=kwargs)

    def get_user_token_value(self):
        """Get token from a logged response"""
        response = self.client.post(
            reverse(TOKEN_OBTAIN_PAIR),
            {
                "username": self.user_name,
                "password": self.user_password
            }
        )
        response_json = response.json()

        return response_json.get("access")
