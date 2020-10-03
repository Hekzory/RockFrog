from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import notifications.routing
import personal_messages.routing

all_websocket_url_patterns = notifications.routing.websocket_urlpatterns + personal_messages.routing.websocket_urlpatterns

application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            all_websocket_url_patterns
        )
    ),
})
