import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from config.config import APP_CONFIG
from services.shared.browser_mob_proxy_service import BrowserMobProxyService

class SeleniumService:
    def __init__(self):
        browsermob_path = APP_CONFIG['BMP_PROXY_URL']
        chrome_options = Options()

        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-webrtc")
        chrome_options.add_argument("--hide-scrollbars")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--start-maximized")

        # Настраиваем прокси для Chrome через BrowserMob Proxy
        chrome_options.add_argument(f'--proxy-server={browsermob_path}')

        self.driver = webdriver.Remote(
            command_executor=APP_CONFIG['SELENIUM_REMOTE_URL'],
            options=chrome_options
        )
        self.by = By
        self.ec = EC
        self.driver_wait = WebDriverWait
        self.web_element = WebElement
        self.keys = Keys
        self.select = Select
        self.bmp_service = BrowserMobProxyService