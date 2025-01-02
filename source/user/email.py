import re, time, random, sqlite3, pickle
from selenium.webdriver import Chrome
from selenium.common.exceptions import UnexpectedAlertPresentException, NoAlertPresentException
from typing import Union

class TMail:
    def __init__(self, driver: Chrome) -> None:
        email_service_provider = [('https://tempmailto.org', r'email_id">(.*?@.*?)<', '.tempmailto.org')]
        self.driver = driver
        self.url, self.regex, self.domain = random.choice(email_service_provider)

    def new_email(self) -> Union[str, None]:
        self.driver.get(self.url)

        for _ in range(20):
            match = re.search(self.regex, self.driver.page_source)
            if match: return match.group(1)
            time.sleep(1)

        return None

    def get_code(self) -> Union[str, bool]:
        for _ in range(20):
            self.driver.refresh()
            time.sleep(2)
            open('/sdcard/x.htm', 'w').write(self.driver.page_source)
            match = re.search(r'FB-(.*?) ', self.driver.page_source)
            if match: return match.group(1)

        return None



