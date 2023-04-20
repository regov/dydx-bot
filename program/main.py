from constants import ABORD_ALL_POSITIONS, FIND_COINTEGRATED_PAIRS, PLACE_TRADES, MANAGE_EXITS
from func_connections import connect_dydx
from func_private import abord_all_positions
from func_public import construct_market_prices
from func_cointegration import store_cointegration_results
from func_entry_pairs import open_positions
from func_exit_pairs import manage_trade_exits
from func_messaging import send_message
from websocket_handler import start_websocket_server, send_message_to_clients, connected_clients

import asyncio
import threading

# Run bot
async def run_bot():

        # Send message to Telegram
        try:
            send_message("DYDX Bot Started successfully")
            await send_message_to_clients("DYDX Bot Started successfully")

            # Connect to DYDX
            try:
                print("Connecting to DYDX...")
                await send_message_to_clients("DYDX Bot Started successfully")
                client = connect_dydx()
                account = client.private.get_account()
                quote_balance = account.data["account"]["quoteBalance"]
                equity = account.data["account"]["equity"]
            except Exception as e:
                print("Error:", e)
                print (" Error connecting to DYDX. Check your keys and try again.")
                send_message(f"Failed to connect to client {e}")
                await send_message_to_clients(f"Failed to connect to client {e}")
                exit(1)
            
            # Abord all open positions and orders 
            if ABORD_ALL_POSITIONS:
                try:
                    print("Closing all open positions")
                    await send_message_to_clients("Closing all open positions")
                    close_orders = abord_all_positions(client)
                except Exception as e:
                    print (" Error closing open positions: ", e)
                    send_message(f"Error closing all positions {e}")
                    exit(1)

            # Find Cointegrated Pairs
            if FIND_COINTEGRATED_PAIRS:

                # Construct Market Prices
                try:
                    print("Fetching market prices, please allow 3 mins...")
                    await send_message_to_clients("Fetching market prices, please allow 3 mins...")
                    df_market_prices = construct_market_prices(client)

                except Exception as e:
                    print("Error constructing market prices: ", e)
                    send_message(f"Error constructing market prices {e}")
                    await send_message_to_clients(f"Error constructing market prices {e}")
                    exit(1)

                # Store Cointegrated Pairs
                try:
                    print("Storing cointegrated pairs...")
                    await send_message_to_clients("Storing cointegrated pairs...")
                    stores_result = store_cointegration_results(df_market_prices)
                    if stores_result != "saved":
                        print("Error saving cointegrated pairs")
                        await send_message_to_clients("Error saving cointegrated pairs")
                        exit(1)
                except Exception as e:
                    print("Error saving cointegrated pairs: ", e)
                    send_message(f"Error saving cointegrated pairs {e}")
                    await send_message_to_clients(f"Error saving cointegrated pairs {e}")
                    exit(1)

            # Run as always on
            while True:

                # Place trades for opening positions
                if MANAGE_EXITS:
                    try:
                        print("Managing exits...")
                        await send_message_to_clients("Managing exits...")
                        await manage_trade_exits(client)
                    except Exception as e:
                        print("Error managing exiting positions: ", e)
                        send_message(f"Error managing exiting positions {e}")
                        await send_message_to_clients(f"Error managing exiting positions {e}")
                        exit(1)

                    # Place trades for opening positions
                if PLACE_TRADES:
                    try:
                        print(f"Balance: {quote_balance}")
                        print(f"equity: {equity}")
                        print("Finding trading opportunities...")
                        
                        await send_message_to_clients(f"Balance: {quote_balance}")
                        await send_message_to_clients(f"Equity: {equity}")
                        await send_message_to_clients("Finding trading opportunities...")

                        await open_positions(client)
                    except Exception as e:
                        print("Error trading pairs: ", e)
                        send_message(f"Error opening trades {e}")
                        await send_message_to_clients(f"Error opening trades {e}")
                        exit(1)
        except Exception as e:
            print(e)
            send_message("DYDX Bot Failed to start")
            await send_message_to_clients("DYDX Bot Failed to start")
            exit(1)
        finally:
            send_message("DYDX Bot Stopped")
            await send_message_to_clients("DYDX Bot Stopped")

def run_asyncio_coroutine_in_thread(coroutine):
    def run_in_new_event_loop():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(coroutine)
        loop.close()

    thread = threading.Thread(target=run_in_new_event_loop)
    thread.start()

    return thread

if __name__ == "__main__":
    websocket_server_thread = run_asyncio_coroutine_in_thread(start_websocket_server())
    bot_thread = run_asyncio_coroutine_in_thread(run_bot())

    websocket_server_thread.join()
    bot_thread.join()
