import asyncio
import websockets
import logging
import ssl
import json

from func_connections import connect_dydx

connected_clients = []

async def get_user_data():
    # Remplacez cette fonction par la logique nécessaire pour obtenir les données de l'utilisateur
    client = connect_dydx()
    account = client.private.get_account()
    return account.data["account"]["equity"]

async def websocket_handler(websocket, path):
    logging.debug(f'New WebSocket connection: {websocket.remote_address}')
    connected_clients.append(websocket)

    try:
        while True:
            try:
                message = await websocket.recv()
                if message:
                    # Traiter les messages reçus et envoyer les données de l'utilisateur en réponse à une demande spécifique
                    message_data = json.loads(message)
                    if message_data.get('action') == 'get_user_data':
                        user_data = await get_user_data()

                        balance = {"balance": user_data}
                        await websocket.send(json.dumps(balance))
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
        logging.debug("WebSocket server started on port 8765")
        await asyncio.Future()  # Run the WebSocket server indefinitely

async def send_message_to_clients(message):
    for client in connected_clients:
        await client.send(message)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(start_websocket_server())