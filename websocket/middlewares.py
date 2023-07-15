from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.db import close_old_connections


class TokenAuthMiddleware(BaseMiddleware):
    def __init__(self, app):
        self.app = app

    @database_sync_to_async
    def get_user(self, token_value):
        from rest_framework.authtoken.models import Token

        token = Token.objects.filter(key=token_value).first()
        if token:
            return token.user

    async def __call__(self, scope, receive, send):
        await database_sync_to_async(close_old_connections)()
        headers = scope.get("headers")

        token_header = self.get_auth_header(headers)
        if token_header:
            user = await self.get_user(token_header.split(" ")[1])
            scope["user"] = user
        return await self.app(scope, receive, send)

    def get_auth_header(self, headers):
        for header in headers:
            if header[0].decode().lower() == "authorization":
                return header[1].decode().lower()

        return None
