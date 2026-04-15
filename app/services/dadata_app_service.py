from dadata import Dadata
from config.config import APP_CONFIG

class DadataAppService:
    def __init__(self):
        token = APP_CONFIG['SERVICE_TOKEN']
        secret = APP_CONFIG['SERVICE_KEY']
        service = Dadata(token, secret)
        self.service = service

    def get_clean(self, address):
        if not address:
            raise ValueError(f"field address empty!")

        return self.service.clean("address", address)

    def get_by_id(self, address_id):
        if not address_id:
            raise ValueError(f"field get_by_id empty!")

        return self.service.find_by_id("address", address_id)
