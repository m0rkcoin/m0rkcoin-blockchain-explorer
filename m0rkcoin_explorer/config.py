import os

import yaml
import jinja2
from munch import Munch
from walrus import Walrus


config_file_path = os.path.join(
    os.path.dirname(__file__), os.path.pardir, 'config.yml')
config_override_file_path = os.path.join(
    os.path.dirname(__file__), os.path.pardir, 'config-override.yml')

config: Munch = None

env = jinja2.Environment(loader=jinja2.PackageLoader('m0rkcoin_explorer'))


def load_config():
    with open(config_file_path) as config_file:
        _config = yaml.load(config_file)
        globals()['config'] = Munch.fromDict(_config)
    try:
        with open(config_override_file_path) as config_override_file:
            _config_override = yaml.load(config_override_file)
            globals()['config'].update(_config_override)
    except Exception:
        pass


load_config()

cache_client = Walrus(host=config.redis.host, port=config.redis.port)
cache = cache_client.cache()

CACHE_HOUR = 60 * 60
CACHE_DAY = CACHE_HOUR * 24
CACHE_WEEK = CACHE_DAY * 7
CACHE_MONTH = CACHE_DAY * 30

M0RKCOIN_PREV_HEIGHT = 'm0rkcoin:prev_height'
M0RKCOIN_EMISSION_KEY = 'm0rkcoin:emission'
