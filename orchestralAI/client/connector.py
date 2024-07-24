import asyncio
from ..websocket_client import WebSocketClient


async def connect_client(api_key: str) -> WebSocketClient:
    # Connect to OrchestralAI Server
    print("[client_connector] Connecting client")
    wsc = WebSocketClient()

    connection_result = await wsc.connect(api_key)
    if connection_result is not True:
        raise Exception(f"WS Connection Error: {connection_result}")
    print("[client_connector] Websocket connected")

    # Start keep-alive task
    # keep_alive_task = asyncio.create_task(wsc.keep_alive())
    # wsc.keep_alive_task = keep_alive_task
    # print("[client_connector] Started keep alive task")

    return wsc