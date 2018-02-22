import os

import yaml
import jinja2
from munch import Munch
from walrus import Walrus


config_file_path = os.path.join(
    os.path.dirname(__file__), os.path.pardir, 'config.yml')

config = None

env = jinja2.Environment(loader=jinja2.PackageLoader('m0rkcoin_explorer'))


def load_config():
    with open(config_file_path) as config_file:
        _config = yaml.load(config_file)
        globals()['config'] = Munch.fromDict(_config)


load_config()

cache_client = Walrus(host=config.redis.host, port=config.redis.port)
cache = cache_client.cache()

CACHE_HOUR = 60 * 60
CACHE_DAY = CACHE_HOUR * 24
CACHE_WEEK = CACHE_DAY * 7
CACHE_MONTH = CACHE_DAY * 30
