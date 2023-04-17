import asyncio
import websockets
from websocket_handler import start_websocket_server

async def main():
    await start_websocket_server()

if __name__ == "__main__":
    asyncio.run(main())
