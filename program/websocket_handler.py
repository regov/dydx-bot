import asyncio
import websockets
import logging


connected_clients = []

async def websocket_handler(websocket, path):
    logging.debug(f'New WebSocket connection: {websocket.remote_address}')
    connected_clients.append(websocket)
    try:
        while True:
            await asyncio.sleep(1)
    finally:
        connected_clients.remove(websocket)
        logging.debug(f'WebSocket connection closed: {websocket.remote_address}')

async def start_websocket_server():
    async with websockets.serve(websocket_handler, "0.0.0.0", 8765):
        logging.debug("WebSocket server started on ws://localhost:8765")
        await asyncio.Future()  # Exécutez le serveur WebSocket indéfiniment

async def send_message_to_clients(message):
    for client in connected_clients:
        await client.send(message)
