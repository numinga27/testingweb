from channels.routing import ProtocolTypeRouter
from live.liveflash.routing import websockets

application = ProtocolTypeRouter({
    "websocket": websockets,
})