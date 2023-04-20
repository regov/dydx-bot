import asyncio
import websockets
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
                break
            except Exception as e:
                print(f"Error in websocket_handler: {e}")
                break
    finally:
        connected_clients.remove(websocket)


async def start_websocket_server():
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(certfile='/etc/letsencrypt/live/dydx-bot.afao.fr/fullchain.pem', keyfile='/etc/letsencrypt/live/dydx-bot.afao.fr/privkey.pem')

    async with websockets.serve(websocket_handler, "0.0.0.0", 8765, ssl=ssl_context):
        await asyncio.Future()  # Run the WebSocket server indefinitely

async def send_message_to_clients(message):
    message =  {"message": str(message)}
    for client in connected_clients:
        await client.send(json.dumps(message))

if __name__ == "__main__":
    asyncio.run(start_websocket_server())