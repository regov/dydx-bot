from constants import ABORD_ALL_POSITIONS, FIND_COINTEGRATED_PAIRS
from func_connections import connect_dydx
from func_private import abord_all_positions
from func_public import construct_market_prices

if __name__ == "__main__":
    # Connect to DYDX
    try:
        print("Connecting to DYDX...")
        client = connect_dydx()
    except Exception as e:
        print("Error:", e)
        print (" Error connecting to DYDX. Check your keys and try again.")
        exit(1)
    
    # Abord all open positions and orders 
    if ABORD_ALL_POSITIONS:
        try:
            print("Closing all open positions")
            close_orders = abord_all_positions(client)
        except Exception as e:
            print (" Error closing open positions: ", e)
            exit(1)

    # Find Cointegrated Pairs
    if FIND_COINTEGRATED_PAIRS:

        # Construct Market Prices
        try:
            print("Fetching market prices, please allow 3 mins...")
            df_market_prices = construct_market_prices(client)

        except Exception as e:
            print("Error constructing market prices: ", e)
            exit(1)

       