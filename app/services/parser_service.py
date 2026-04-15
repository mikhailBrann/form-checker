import re
import json
import time
import os
from fastapi import UploadFile, File
from selenium.webdriver.remote.webelement import WebElement

from services.selenium_service import SeleniumService

class ParserService:
    def __init__(self):
        self.selenium = SeleniumService()

    def parse_page_screenshot(
        self, 
        url: str, 
        filename: str
    ): 
        try:
            self.selenium.driver.get(url)
            time.sleep(2)

            self.make_shot(
                url,
                f"{filename}_before.png"
            )

            form = self.send_form(
                ".resume-form form",
                {
                    "name": {
                        "value": "test test",
                        "type": "input"
                    },
                    "phone": {
                        "value": "9999999998",
                        "type": "user_input"
                    },
                    "birthdate": {
                        "value": "01101988",
                        "type": "user_input"
                    },
                    "select-vol2": {
                        "value": "Магазины",
                        "value_elem": ".complete__dropdown-option",
                        "type": "click_select_by_selector"
                    },
                    "privacy": {
                        "value": "",
                        "type": "checkbox"
                    }
                }
            )

            self.make_shot(
                url,
                f"{filename}_after.png"
            )

            return form
        except Exception as e:
            return e
        finally:
            self.selenium.driver.close()
            self.selenium.driver.quit()

    def make_shot(
        self, 
        url: str, 
        filename: str,
        tag="body", 
        file_path="public/storage/screenshots"
    ):
        try:
            ele = self.selenium.driver.find_element(
                self.selenium.by.TAG_NAME, 
                tag
            )
            height = self.selenium.driver.execute_script(
                "return document.body.scrollHeight"
            )

            self.selenium.driver.set_window_size(
                1920, 
                height
            )

            if not os.path.exists(file_path):
                os.mkdir(file_path)

            path_to_file = f"{file_path}/{filename}"

            self.selenium.driver.save_screenshot(path_to_file)

            return path_to_file
        except Exception as e:
            return e

    def send_form(self, parent_selector: str, fields: dict):
        form = self.selenium.driver.find_element(
            self.selenium.by.CSS_SELECTOR,
            parent_selector
        )

        for field in fields:
            field_value = fields[field].get("value")
            field_type = fields[field].get("type")
            value_elem_selector = fields[field].get("value_elem")
            
            self._complete_field_form(
                field_value,
                field_type,
                value_elem_selector
            )

        time.sleep(0.1)
        result = self._submit_form(form)

        return result
    
    def _submit_form(self, form):
        requests = []
        
        self.selenium.driver.execute_cdp_cmd("Network.enable", {})
        self.selenium.driver.execute_cdp_cmd(
            "Network.setRequestInterception",
            {
                "patterns": [{"urlPattern": "*", "resourceType": "XHR", "interceptionStage": "HeadersReceived"}]
            }
        )
        
        form.submit()

        time.sleep(5)
        
        logs = self.selenium.driver.get_log("performance")

        import json

        for entry in logs:
            message = json.loads(entry["message"])["message"]
            if (
                "Network.requestWillBeSent" == message.get("method")
                or "Network.responseReceived" == message.get("method")
            ):
                requests.append(message)

        # Отключаем Network мониторинг
        self.selenium.driver.execute_cdp_cmd("Network.disable", {})
        
        return requests



        

    def _complete_field_form(
        self, 
        form, 
        field_value="",
        field_type="",
        value_elem_selector=""
    ):
        if field_type == "click_select_by_selector":
            field_elem = form.find_element(
                self.selenium.by.CSS_SELECTOR,
                f".{field}"
            )
            value_elem_selector = fields[field]['value_elem']
            elems = form.find_elements(
                self.selenium.by.CSS_SELECTOR,
                f"{value_elem_selector}"
            )

            field_elem.click()
            time.sleep(0.1)

            field_click_elem = next((el for el in elems if el.text.strip() == field_value), None)
            
            if field_click_elem != None:
                field_click_elem.click()

        
        if field_type == "input":
            field_elem = form.find_element(
                self.selenium.by.CSS_SELECTOR,
                f"[name={field}]"
            )

            field_elem.clear()
            field_elem.send_keys(field_value)

        if field_type == "user_input":
            field_elem = form.find_element(
                self.selenium.by.CSS_SELECTOR,
                f"[name={field}]"
            )
            
            time.sleep(0.1)

            self.selenium.driver.execute_script("arguments[0].scrollIntoView(true);", field_elem)
            self.selenium.driver.execute_script("arguments[0].focus();", field_elem)
            self.selenium.driver.execute_script("arguments[0].value = '';", field_elem)

            for char in str(field_value):
                field_elem.send_keys(char)
                time.sleep(0.1)

            field_elem.send_keys(self.selenium.keys.TAB)

        if field_type == "checkbox":
            field_elem = form.find_element(
                self.selenium.by.CSS_SELECTOR,
                f"[name={field}]"
            )
            self.selenium.driver.execute_script("arguments[0].click();", field_elem)