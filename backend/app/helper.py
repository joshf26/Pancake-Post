import logging

from datetime import datetime

from conf import *

logging.basicConfig(level=logging.DEBUG, format='[All Forum %(asctime)s] - %(message)s')


class Post:
    def __init__(self, owner, title, content=None):
        self.owner = owner
        self.title = title
        self.content = content

        self.time = datetime.now()
        self.responses = []
        self.votes = [owner]


def log(message):
    if DEBUG_MESSAGES:
        logging.debug('[DEBUG] {}'.format(message))
