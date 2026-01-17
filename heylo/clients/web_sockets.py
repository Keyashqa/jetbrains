import websockets
import json

class GridWebSocketClient:
    def __init__(self, ws_url: str, api_key: str):
        self.ws_url = ws_url
        self.api_key = api_key

    async def listen(self, on_message):
        async with websockets.connect(
            self.ws_url,
            extra_headers={"Authorization": f"Bearer {self.api_key}"}
        ) as ws:
            async for msg in ws:
                await on_message(json.loads(msg))
