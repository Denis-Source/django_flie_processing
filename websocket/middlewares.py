from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.db import close_old_connections


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
