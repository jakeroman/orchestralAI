import asyncio

from . import networking
from ..websocket_client import WebSocketClient


class OrchestralClient:
    api_key: str

    # Initialization
    def __init__(self, api_key: str):
        self.api_key = api_key


    # API Methods
    def serve(self):
        """Starts a blocking connection and serves tools."""
        asyncio.run(self._serve_async())


    # Async API Methods
    async def _serve_async(self):
        """Async method to start a blocking connection and serves tools."""
        wsc: WebSocketClient = await networking.get_connection(self.api_key)

        result = await networking.run_action(wsc, "ping", message="Hello World!")
        print(result)

        await wsc.disconnect()