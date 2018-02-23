import asyncio
import logging

from sanic import Sanic

from m0rkcoin_explorer import daemon
from m0rkcoin_explorer.config import (
    M0RKCOIN_EMISSION_KEY, M0RKCOIN_PREV_HEIGHT, cache_client, config)
from m0rkcoin_explorer.site.routes import _site_bp


logger = logging.getLogger('sanic')


app = Sanic()

app.static('/static', './static')

app.blueprint(_site_bp)


async def calculate_emission():
    while True:
        await asyncio.sleep(30)

        logger.info('Refreshing emission...')

        block_count = daemon.get_block_count()
        prev_block_count = int(cache_client.get(M0RKCOIN_PREV_HEIGHT) or 1)
        total_reward = int(cache_client.get(M0RKCOIN_EMISSION_KEY) or 0)

        for height in range(prev_block_count, block_count + 1):
            block = daemon.get_block_by_height(height)
            total_reward += block['reward']

        logger.info(f'New Emission: {total_reward} at '
                    f'Height {block_count + 1}')
        cache_client.set(M0RKCOIN_EMISSION_KEY, total_reward)
        cache_client.set(M0RKCOIN_PREV_HEIGHT, block_count + 1)


app.add_task(calculate_emission())

if __name__ == '__main__':
    app.run(host=config.host, port=config.port, debug=config.debug)
