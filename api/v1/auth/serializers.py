from rest_framework.serializers import ModelSerializer

from user.models import User


class UserDetailSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "role",
            "registered",
            "image",
            "is_superuser"
        ]
