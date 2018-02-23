

def get_human_readable_hash_rate(hash_rate: float) -> str:
    index = 0
    units = ['H', 'KH', 'MH', 'GH', 'TH', 'PH']
    while hash_rate > 1024:
        hash_rate = hash_rate / 1024
        index += 1
    return f'{hash_rate:.2f} {units[index]}'
