import asyncio
import websockets
import logging
import ssl

connected_clients = []

async def websocket_handler(websocket, path):
    logging.debug(f'New WebSocket connection: {websocket.remote_address}')
    connected_clients.append(websocket)
    try:
        while True:
            try:
                message = await websocket.recv()
                if message:
                    # Process the received message as needed
                    pass
            except websockets.exceptions.ConnectionClosed as e:
                logging.debug(f"WebSocket connection closed: {websocket.remote_address} - {e}")
                break
            except Exception as e:
                logging.debug(f'WebSocket connection error: {e}')
                print(f"Error in websocket_handler: {e}")
                break
    finally:
        connected_clients.remove(websocket)
        logging.debug(f'WebSocket connection removed: {websocket.remote_address}')


async def start_websocket_server():
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(certfile='/etc/letsencrypt/live/dydx-bot.afao.fr/fullchain.pem', keyfile='/etc/letsencrypt/live/dydx-bot.afao.fr/privkey.pem')

    async with websockets.serve(websocket_handler, "0.0.0.0", 8765, ssl=ssl_context):
        logging.debug("WebSocket server started on wss://localhost:8765")
        await asyncio.Future()  # Run the WebSocket server indefinitely

async def send_message_to_clients(message):
    for client in connected_clients:
        await client.send(message)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(start_websocket_server())
