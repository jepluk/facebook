import time
from selenium.webdriver import ChromeOptions, Chrome
from .register import Register
from .user.email import TMail

options = ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--headless=new")
options.add_argument("--enable-javascript")
# Database path name
database = 'database.db'

class Browser:
    def __init__(self) -> None:
        self.tmail = TMail(Chrome(options=options))
        self.register = Register(Chrome(options=options), database)

    def quit(self) -> bool:
        self.tmail.driver.quit()
        self.register.driver.quit()

if __name__ == "__main__":
    bro = Browser()
    email = bro.tmail.new_email()
    reg = bro.register.new(email=email)
    print(reg)
    bro.quit()
