from sanic import Blueprint
from sanic.request import Request
from sanic.response import html

from m0rkcoin_explorer.config import env, config
from m0rkcoin_explorer import daemon, utils


_site_bp = Blueprint('site_bp', '')

@_site_bp.route('/', methods=['GET'])
async def home_page(request: Request):

    block_count = daemon.get_block_count()

    start_block = int(request.args.get('start_block', block_count))

    last_block = daemon.get_last_block_header()

    difficulty = last_block['difficulty']
    hash_rate = utils.get_human_readable_hash_rate(
        difficulty / config.coin_diff_target)

    recent_blocks = []
    min_block = start_block - config.page_size

    for height in range(max(min_block, 0) + 1, start_block + 1):
        recent_blocks.append(daemon.get_block_by_height(height))

    recent_blocks.reverse()

    ctx = {
        'block_count': f'{block_count:,}',
        'difficulty': f'{difficulty:,}',
        'hash_rate': hash_rate,
        'emission': f'{int(last_block["reward"] / 1000000000000)}',
        'recent_blocks': recent_blocks,
        'min_block': min_block
    }

    template = env.get_template('index.html')
    return html(template.render(**ctx))
