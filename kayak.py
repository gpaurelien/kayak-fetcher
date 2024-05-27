import json
import logging
import random
from time import sleep
from urllib.parse import urlencode

logger = logging.getLogger(__name__)

def default_evade():
    sleep(random.randint(2, 5))  # sleep a random duration to try and evade suspentio

class Kayak:
    def __init__(self):
        pass

    def _fetch(self, uri, evade=default_evade):
        evade()

        url = f"{self.client.API_BASE_URL if not base_request else self.client.LINKEDIN_BASE_URL}{uri}"
        return self.client.session.get(url, **kwargs)