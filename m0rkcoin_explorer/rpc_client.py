from typing import Dict
from uuid import uuid4

import requests

from m0rkcoin_explorer.config import config


class RPCException(Exception):
    def __init__(self, message):
        super(RPCException, self).__init__(message)


def call_method(method_name: str, payload: Dict = None) -> Dict:
    full_payload = {
        'params': payload or {},
        'jsonrpc': '2.0',
        'id': str(uuid4()),
        'method': f'{method_name}'
    }
    resp = requests.post(
        f'http://{config.daemon.host}:{config.daemon.port}/json_rpc',
        json=full_payload)
    json_resp = resp.json()
    if 'error' in json_resp:
        raise RPCException(json_resp['error'])
    return json_resp.get('result', {})
