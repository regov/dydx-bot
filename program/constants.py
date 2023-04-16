from dydx3.constants import API_HOST_GOERLI, API_HOST_MAINNET
from decouple import config

# !!! SELECT MODE !!!
MODE = config('MODE', default='DEVELOPMENT')

# Close all open position and orders
ABORD_ALL_POSITIONS = config('ABORD_ALL_POSITIONS', default=False, cast=bool)

# Find Cointegrated Pairs
FIND_COINTEGRATED_PAIRS = config('FIND_COINTEGRATED_PAIRS', default=True, cast=bool)

# Manage Exits
MANAGE_EXITS = config('MANAGE_EXITS', default=True, cast=bool)

# Place Orders
PLACE_TRADES = config('PLACE_TRADES', default=True, cast=bool)

# Resolution
RESOLUTION = config('RESOLUTION', default='1HOUR', cast=str)

# Stats Window
STATS_WINDOW = config('STATS_WINDOW', default=21, cast=int)

# Threshold - Openning
MAX_HALF_LIFE = config('MAX_HALF_LIFE', default=24, cast=float)
ZSCORE_THRESHOLD = config('ZSCORE_THRESHOLD', default=1.5, cast=float)
USD_PER_TRADE = config('USD_PER_TRADE', default=50, cast=float)
USD_MIN_COLLATERAL = config('USD_MIN_COLLATERAL', default=1880, cast=float)

# Threshold - Closing
CLOSE_AT_ZSCORE_CROSS = config('CLOSE_AT_ZSCORE_CROSS', default=True, cast=bool)

#ETHEREUM ADDRESS
ETHEREUM_ADDRESS = config('ETHEREUM_ADDRESS')

# KEYS - PRODUCTION
# Must to be on Mainnet on DYDX
STARK_PRIVATE_KEY_MAINNET = config('STARK_PRIVATE_KEY_MAINNET')
DYDX_API_KEY_MAINNET = config('DYDX_API_KEY_MAINNET')
DYDX_API_SECRET_MAINNET = config('DYDX_API_SECRET_MAINNET')
DYDX_API_PASSPHRASE_MAINNET = config('DYDX_API_PASSPHRASE_MAINNET')


# KEYS - DEVELOPMENT
# Must to be on Testnet on DYDX
STARK_PRIVATE_KEY_TESTNET = config('STARK_PRIVATE_KEY_TESTNET')
DYDX_API_KEY_TESTNET = config('DYDX_API_KEY_TESTNET')
DYDX_API_SECRET_TESTNET = config('DYDX_API_SECRET_TESTNET')
DYDX_API_PASSPHRASE_TESTNET = config('DYDX_API_PASSPHRASE_TESTNET')

# KEYS - EXPORT
STARK_PRIVATE_KEY = STARK_PRIVATE_KEY_TESTNET if MODE == 'DEVELOPMENT' else STARK_PRIVATE_KEY_MAINNET
DYDX_API_KEY = DYDX_API_KEY_TESTNET if MODE == 'DEVELOPMENT' else DYDX_API_KEY_MAINNET
DYDX_API_SECRET = DYDX_API_SECRET_TESTNET if MODE == 'DEVELOPMENT' else DYDX_API_SECRET_MAINNET
DYDX_API_PASSPHRASE = DYDX_API_PASSPHRASE_TESTNET if MODE == 'DEVELOPMENT' else DYDX_API_PASSPHRASE_MAINNET

# HOST - EXPORT
HOST = API_HOST_GOERLI if MODE == 'DEVELOPMENT' else API_HOST_MAINNET

# HTTP PROVIDER
HTTP_PROVIDER_MAINNET = config('HTTP_PROVIDER_MAINNET')
HTTP_PROVIDER_TESTNET = config('HTTP_PROVIDER_TESTNET')
HTTP_PROVIDER = HTTP_PROVIDER_TESTNET if MODE == 'DEVELOPMENT' else HTTP_PROVIDER_MAINNET