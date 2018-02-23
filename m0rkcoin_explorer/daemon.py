from m0rkcoin_explorer.config import cache, CACHE_HOUR
from m0rkcoin_explorer.rpc_client import call_daemon_method


def get_block_count():
    resp = call_daemon_method('getblockcount')
    return resp['count']


def get_block_hash(height: int):
    resp = call_daemon_method(
        'on_getblockhash', {
            "height": height
        }
    )
    return resp


def get_last_block_header():
    resp = call_daemon_method('getlastblockheader')
    return resp['block_header']


def get_block_by_hash(hash: str):
    resp = call_daemon_method(
        'getblockheaderbyhash', {
            "hash": hash
        }
    )
    return resp['block_header']


@cache.cached(timeout=CACHE_HOUR)
def get_block_by_height(height: int):
    resp = call_daemon_method(
        'getblockheaderbyheight', {
            "height": height
        }
    )
    return resp['block_header']
