import re, random, string, pickle, sqlite3, time
from typing import Union
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
from .user import Identity

#409 gagal registrasi 
#180 checkpoint 
#1 berhasil
#500 kesalahan validasi

class Register:
    def __init__(self, driver: Chrome, database: str) -> None:
        self.database = database
        self.driver = driver
        self.domain = '.facebook.com'

    def new(self, email: str, gender: Union[str, int] = None, password: str = None) -> int:
        setattr(self, 'user', Identity(gender=gender))
        setattr(self, 'password', password or ''.join(random.sample(string.ascii_letters + string.digits, random.randrange(8, 10))))
        setattr(self, 'email', email)
        setattr(self, 'gender', gender)

        self.driver.get('https://www.facebook.com/r.php')
        try:
            self._fill_registration_form()
            time.sleep(20)

            if email in self.driver.page_source and 'reg_error' not in self.driver.page_source:
                return 1

            if 'reg_error' in self.driver.page_source:
                self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
                time.sleep(20)

                if email in self.driver.page_source:
                    return 1

            if '180' in self.driver.page_source:
                return 180
        except NoSuchElementException:
            pass

        return 408

    def confirm(self, code: Union[str, int]) -> int:
        self.driver.get('https://www.facebook.com/me')
        time.sleep(2)

        try:
            try:self.driver.find_element(By.NAME, 'code').send_keys(code)
            except: self.driver.find_element(By.NAME, 'n').send_keys(code)
        except NoSuchElementException:
            return 103

        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(10)
        return self._validate()

    def _fill_registration_form(self) -> None:
        self.driver.find_element(By.NAME, 'firstname').send_keys(self.user.firstname)
        self.driver.find_element(By.NAME, 'lastname').send_keys(self.user.lastname)
        self.driver.find_element(By.NAME, 'birthday_day').send_keys(self.user.birthday.day)
        self.driver.find_element(By.NAME, 'birthday_month').send_keys(self.user.birthday.month)
        self.driver.find_element(By.NAME, 'birthday_year').send_keys(self.user.birthday.year)
        self.driver.find_element(By.CSS_SELECTOR, f'input[name="sex"][value="{self.user.gender}"]').click()
        self.driver.find_element(By.NAME, 'reg_email__').send_keys(self.email)
        self.driver.find_element(By.NAME, 'reg_passwd__').send_keys(self.password)
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()

    def _validate(self) -> int:
        self.driver.get('https://www.facebook.com/me')

        if 'profile' in self.driver.page_source:
            with sqlite3.connect(self.database) as db:
                db.cursor().execute('INSERT INTO accounts VALUES (?,?,?,?,?,?,?,?)', (re.search(r'c_user=(.*?);', self.cookie()).group(1),f'{self.user.firstname} {self.user.lastname}',self.email,self.password,f'{self.user.birthday.day}/{self.user.birthday.month}/{self.user.birthday.year}','female' if str(self.gender) == '1' else 'male',datetime.now().strftime('%d/%m/%Y'),self.user.useragent))
                db.commit()
            return 1
        
        return 500

    def cookie(self) -> str:
        return '; '.join([f'{cookie["name"]}={cookie["value"]}' for cookie in self.driver.get_cookies()])
