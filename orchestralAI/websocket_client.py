import asyncio
import websockets

class WebSocketClient:
    server_ip: str
    server_port: int

    def __init__(self, server_ip: str = "127.0.0.1", server_port: int = 8000):
        self.ws = None
        self.server_ip = server_ip
        self.server_port = server_port
        self.keep_alive_task = None

    async def connect(self, api_key: str) -> None:
        try:
            self.ws = await websockets.connect(f"ws://{self.server_ip}:{self.server_port}/websockets/{api_key}")
            return True
        except Exception as e:
            return e

    async def send_message(self, message: str) -> None:
        if not self.ws:
            raise ValueError("WebSocket connection is not established")
        try:
            await self.ws.send(message)
        except Exception as e:
            print(f"[websocket_client] Error sending message over WebSocket: {e}")

    async def receive_message(self) -> str:
        if not self.ws:
            raise ValueError("WebSocket connection is not established")
        try:
            return await self.ws.recv()
        except Exception as e:
            print(f"[websocket_client] Error receiving message over WebSocket: {e}")

    async def keep_alive(self):
        try:
            while True:
                print("[keep_alive] ping")
                await self.send_message("ping")
                await asyncio.sleep(30)  # Ping every 30 seconds
        except websockets.ConnectionClosed:
            print("[websocket_client] Connection closed")
    
    async def disconnect(self):
        if self.keep_alive_task:
            self.keep_alive_task.cancel()
            try:
                await self.keep_alive_task
            except asyncio.CancelledError:
                pass
        if self.ws:
            await self.ws.close()
            self.ws = None
            print("[websocket_client] WebSocket connection closed")