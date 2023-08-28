"""
ASGI config for live project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import live.routing

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': URLRouter(
        live.routing.websocket_urlpatterns
    ),
})
