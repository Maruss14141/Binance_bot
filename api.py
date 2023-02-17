from binance.um_futures import UMFutures


def connection (api_key, secret_key):
    return UMFutures(api_key,secret_key)

