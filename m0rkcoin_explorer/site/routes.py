from sanic import Blueprint
from sanic.request import Request
from sanic.response import html

from m0rkcoin_explorer.config import (
    env, config, cache_client,
    M0RKCOIN_EMISSION_KEY)
from m0rkcoin_explorer import daemon, utils
from m0rkcoin_explorer.utils import format_block_values


_site_bp = Blueprint('site_bp', '')

@_site_bp.route('/', methods=['GET'])
async def home_page(request: Request):

    block_count = daemon.get_block_count()

    if request.args.get('start_block'):
        start_block = int(request.args.get('start_block')) + 1
    else:
        start_block = block_count

    last_block = daemon.get_last_block_header()

    difficulty = last_block['difficulty']
    hash_rate = utils.get_human_readable_hash_rate(
        difficulty / config.coin_diff_target)

    recent_blocks = []
    min_block = start_block - config.page_size

    for height in range(max(min_block, 0), start_block + 1):
        recent_blocks.append(daemon.get_block_by_height(height))

    recent_blocks.reverse()

    emission = int(cache_client.get(M0RKCOIN_EMISSION_KEY) or 0)

    format_block_values(recent_blocks)

    ctx = {
        'block_count': f'{block_count:,}',
        'difficulty': f'{difficulty:,}',
        'hash_rate': hash_rate,
        'emission': f'{int(emission / 1000000000000):,}',
        'recent_blocks': recent_blocks,
        'min_block': min_block
    }

    template = env.get_template('index.html')
    return html(template.render(**ctx))


@_site_bp.route('/blocks/<block_hash:[\w\d]{64}>', methods=['GET'])
async def block_details_by_hash(request: Request, block_hash: str):
    block_count = daemon.get_block_count()
    block = daemon.get_block_by_hash(block_hash)

    format_block_values(block)

    ctx = {
        'block': block,
        'block_count': block_count
    }

    template = env.get_template('block.html')
    return html(template.render(**ctx))


@_site_bp.route('/blocks/<block_height:\d+>', methods=['GET'])
async def block_details_by_height(request: Request, block_height: int):
    block_count = daemon.get_block_count()
    block = daemon.get_block_by_height(int(block_height) + 1)

    format_block_values(block)

    ctx = {
        'block': block,
        'block_count': block_count
    }

    template = env.get_template('block.html')
    return html(template.render(**ctx))
