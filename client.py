import requests
import logging
from bs4 import BeautifulSoup
import json
from requests.exceptions import HTTPError

logger = logging.getLogger(__name__)

class Client:
    """
    Class to act as a client for the Kayak API.
    """

    BASE_URL = "https://www.kayak.fr/flights/PAR-DBV/2024-07-04/2024-07-11"
    # API_BASE_URL = f"{BASE_URL}/"
    HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept-Encoding': 'gzip, deflate',
    }

    def __init__(self, *args, debug=False, proxies={}):
        self.session = requests.session()
        self.session.headers.update(Client.HEADERS)
        self.proxies = proxies
        self.logger = logger
        self.metadata = {}
        self.session.cookies = None
        self.args = args

        if proxies:
            self.session.proxies.update(proxies)

        logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)

    def _request_session_cookies(self):
        logger.debug("Requesting the app for new cookies.")

        r = requests.get(
            Client.BASE_URL,
            headers=Client.HEADERS,
            proxies=self.proxies,
        )

        return r.cookies
    
    def _set_session_cookies(self, cookies):
        self.session.cookies = cookies

    @property
    def cookies(self):
        return self.session.cookies
    
    def fetch_data(self):
        """
        Get the Kayak data and store it in metadata
        """

        try:
            r = requests.get(
            Client.BASE_URL,
            cookies=self.session.cookies,
            proxies=self.proxies
            )
            r.raise_for_status()

            logger.debug("Request completed successfully")
        except HTTPError as e:
            logger.debug('HTTPError occured %s' % (e))
            raise

        return r.text