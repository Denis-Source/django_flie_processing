from django.contrib.auth.models import AnonymousUser
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.exceptions import NotAuthenticated
from rest_framework.generics import RetrieveAPIView

from api.v1.auth.serializers import UserDetailSerializer
from user.models import User


class UserDetailAPIView(RetrieveAPIView):
    serializer_class = UserDetailSerializer
    queryset = User.objects.all()

    def get_object(self):
        if type(self.request.user) == AnonymousUser:
            raise NotAuthenticated
        else:
            return self.request.user
