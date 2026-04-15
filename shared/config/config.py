import os
from dotenv import load_dotenv

load_dotenv()

APP_CONFIG = {
    'APP_PORT': int(os.getenv('APP_PORT', 8000)),
    'SELENIUM_REMOTE_URL': os.getenv('SELENIUM_REMOTE_URL', ''),
}