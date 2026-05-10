import requests

from config.config import APP_CONFIG

browsermob_base_path = APP_CONFIG['BMP_PROXY_URL']
browsermob_path = f"http://{browsermob_base_path}"

class BrowserMobProxyService:
    def __init__(self, base_url=browsermob_path):
        self.base_url = base_url
        self.proxy_port = None

    def create_proxy(self):
        resp = requests.post(f"{self.base_url}/proxy")
        self.proxy_port = resp.json()['port']
        return self.proxy_port

    def start_har(self, har_name="selenium_har"):
        requests.put(f"{self.base_url}/proxy/{self.proxy_port}/har", json={"initialPageRef": har_name})

    def get_har(self):
        resp = requests.get(f"{self.base_url}/proxy/{self.proxy_port}/har")
        return resp.json()

    def close_proxy(self):
        requests.delete(f"{self.base_url}/proxy/{self.proxy_port}")