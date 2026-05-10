import re
import json
from fastapi import UploadFile, File

class ParseDataService:
    def __init__(self, file: UploadFile = File(...)):
        self.file = file

    async def extract_json_by_patern(self, patern=r'local\.ERROR:.*?({.*?"address"\s*:\s*".+?".*?})'): 
        content = await self.file.read()
        logs_text = content.decode("utf-8")

        addresses = set()
        regxp_patern = re.compile(patern)

        matches = regxp_patern.findall(logs_text)

        for json_str in matches:
            try:
                data = json.loads(json_str)
                address = data.get("address")
                if address and address.strip():
                    addresses.add(address.strip())
            except json.JSONDecodeError:
                continue

        return list(addresses)