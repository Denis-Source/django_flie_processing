from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.db import close_old_connections
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.settings import api_settings


class TokenAuthMiddleware(BaseMiddleware):
    """Middleware responsible for token based authentication for channels"""

    def __init__(self, app):
        self.app = app

    @database_sync_to_async
    def get_user(self, token_value):
        """Get user with a provided token"""
        from rest_framework.authtoken.models import Token

        token = Token.objects.filter(key=token_value).first()
        if token:
            return token.user

    async def __call__(self, scope, receive, send):
        """If authentication token is provided, add user to scope"""
        await database_sync_to_async(close_old_connections)()
        params = parse_qs(scope.get('query_string').decode())
        params = params.get("token")
        if params:
            user = await self.get_user(params[0])
            scope["user"] = user
        return await self.app(scope, receive, send)


class JWTAuthMiddleware(BaseMiddleware):
    def __init__(self, app, *args, **kwargs):
        self.app = app
        self.user_model = None

    @database_sync_to_async
    def get_user(self, validated_token):
        """
        Attempts to find and return a user using the given validated token.
        """
        try:
            user_id = validated_token[api_settings.USER_ID_CLAIM]
        except KeyError:
            return

        try:
            user = self.user_model.objects.get(**{api_settings.USER_ID_FIELD: user_id})
        except self.user_model.DoesNotExist:
            return

        return user

    async def __call__(self, scope, receive, send):
        """If authentication token is provided, add user to scope"""

        from user.models import User
        self.user_model = User
        await database_sync_to_async(close_old_connections)()
        params = parse_qs(scope.get('query_string').decode())
        params = params.get("token")
        if params:
            raw_token = params[0]
            try:
                validated_token = self.get_validated_token(raw_token)
                user = await self.get_user(validated_token)
                scope["user"] = user
            except InvalidToken:
                scope["user"] = None
        return await self.app(scope, receive, send)


    def get_validated_token(self, raw_token: bytes):
        messages = []
        for AuthToken in api_settings.AUTH_TOKEN_CLASSES:
            try:
                return AuthToken(raw_token)
            except TokenError as e:
                messages.append(
                    {
                        "token_class": AuthToken.__name__,
                        "token_type": AuthToken.token_type,
                        "message": e.args[0],
                    }
                )

        raise InvalidToken(
            {
                "detail": "Given token not valid for any token type",
                "messages": messages,
            }
        )
