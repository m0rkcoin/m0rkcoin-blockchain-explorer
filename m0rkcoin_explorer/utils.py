from typing import Union, Dict, List

import arrow


def get_human_readable_hash_rate(hash_rate: float) -> str:
    index = 0
    units = ['H', 'KH', 'MH', 'GH', 'TH', 'PH']
    while hash_rate > 1024:
        hash_rate = hash_rate / 1024
        index += 1
    return f'{hash_rate:.2f} {units[index]}'


def format_m0rk_value(amount: int) -> str:
    return f"{amount / 1000000000000:,.12f}"


def format_block_values(blocks: Union[Dict, List[Dict]]):
    if not isinstance(blocks, list):
        blocks = [blocks]

    for block in blocks:
        block['reward'] = format_m0rk_value(block['reward'])
        block['timestamp'] = arrow.get(
            block['timestamp']).format("YYYY-MM-DD HH:mm:ss")
