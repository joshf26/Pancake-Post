import logging

from conf import *

logging.basicConfig(level=logging.DEBUG, format='[Pancake Post %(asctime)s] - %(message)s')


def log(message):
    if DEBUG_MESSAGES:
        logging.debug('[DEBUG] {}'.format(message))
