import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_NAME')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    API_BASE_URL = os.getenv('API_BASE_URL')
    API_KEY = os.getenv('API_KEY')
    REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT'))
    MAX_RETRIES = int(os.getenv('MAX_RETRIES'))
    RETRY_DELAY = int(os.getenv('RETRY_DELAY'))

