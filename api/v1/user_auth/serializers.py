from rest_framework.serializers import ModelSerializer, CharField, Serializer, SerializerMethodField

from user.models import User


class UserDetailSerializer(ModelSerializer):
    max_tasks = SerializerMethodField("get_max_tasks", label="Maximum of opened task user can have at one moment")

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "role",
            "registered",
            "image",
            "is_superuser",
            "max_tasks"
        ]

    def get_max_tasks(self, obj):
        return User.MAX_TASKS


class UserCreateSerializer(ModelSerializer):
    password = CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password"
        ]

    def create(self, validated_data):
        return User.objects.create_user(
            validated_data["username"],
            validated_data["email"],
            validated_data["password"]
        )


class UserLoginSerializer(Serializer):
    username = CharField()
    password = CharField()
