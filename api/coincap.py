import sys
import os
import requests
from requests.exceptions import RequestException
from time import sleep
# from ..config import Config
# from ..utils.logger import logger

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.logger import setup_logger
from config import Config

logger = setup_logger()


class CoinCapAPI:
    def __init__(self):
        self.base_url = Config.API_BASE_URL
        self.timeout = Config.REQUEST_TIMEOUT
        self.max_retries = Config.MAX_RETRIES
        self.retry_delay = Config.RETRY_DELAY
        self.base_url = Config.API_BASE_URL
        # self.base_url = 'https://rest.coincap.io/v3'
        # self.timeout = 30
        # self.max_retries = 3
        # self.retry_delay = 5

    def _make_request(self, endpoint, params=None):
        url = f"{self.base_url}/{endpoint}?apiKey={Config.API_KEY}"
        
        # for attempt in range(self.max_retries):
        #     try:
        #         response = requests.get(url, params=params, timeout=self.timeout)
        #         response.raise_for_status()
        #         return response.json()
        #     except RequestException as e:
        #         logger.warning(f"Attempt {attempt + 1} failed for {url}: {str(e)}")
        #         if attempt < self.max_retries - 1:
        #             sleep(self.retry_delay)
        #             continue
        #         logger.error(f"Max retries reached for {url}")
        #         raise
        response = requests.get(url, params=params, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def get_assets(self):
        # return self._make_request(f"assets?limit={limit}")
        return self._make_request(f"assets")

    def get_asset_history(self, asset_id, interval="d1", start=None, end=None):
        params = {"interval": interval}
        if start:
            params["start"] = start
        if end:
            params["end"] = end
        return self._make_request(f"assets/{asset_id}/history", params=params)

    def get_markets(self, asset_id=None):
        endpoint = "markets"
        if asset_id:
            endpoint += f"?baseId={asset_id}"
        return self._make_request(endpoint)
    

# coin_cap = CoinCapAPI()
# assets = coin_cap.get_assets()
# print(assets)