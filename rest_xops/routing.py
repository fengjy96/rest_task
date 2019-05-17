from websocket.jwt_auth import TokenAuthMiddleware
from channels.routing import URLRouter, ProtocolTypeRouter
from django.urls import path
from websocket.consumers.console import ConsoleMsgConsumer

application = ProtocolTypeRouter({
    "websocket": TokenAuthMiddleware(
        URLRouter([
            path(r"websocket/console", ConsoleMsgConsumer),
        ])
    )
})
