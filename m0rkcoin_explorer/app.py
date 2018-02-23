import asyncio

from sanic import Sanic

from m0rkcoin_explorer import daemon
from m0rkcoin_explorer.config import (
    cache_client, M0RKCOIN_EMISSION_KEY, config)
from m0rkcoin_explorer.site.routes import _site_bp

app = Sanic()

app.static('/static', './static')

app.blueprint(_site_bp)


async def calculate_emission():
    while True:
        await asyncio.sleep(300)
        block_count = daemon.get_block_count()
        total_reward = 0
        for height in range(1, block_count + 1):
            block = daemon.get_block_by_height(height)
            total_reward += block['reward']
        cache_client.set(M0RKCOIN_EMISSION_KEY, total_reward)


app.add_task(calculate_emission())

if __name__ == '__main__':
    app.run(host=config.host, port=config.port, debug=config.debug)
