from pprint import pprint
from time import sleep

from environs import Env

from helpers import FirefoxDriver
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


# base class to post video on tiktok using selenium
class _TikTok:
    def __init__(self, env: Env):
        self.env = env
        self.base_url = "https://www.tiktok.com"
        self._drv = FirefoxDriver()
        self._login()

    # try to login to tiktok
    def _login(self):
        login_url = self.base_url + "/login/phone-or-email/email"
        self._drv.get(login_url)
        pprint(self._drv.get_cookies())
        # self._drv.find_element(By.NAME, "username").send_keys(self.env("TIKTOK_USERNAME"))
        # self._drv.find_element(
        #     By.XPATH,
        #     "/html/body/div[2]/div/div[2]/div[1]/form/div[2]/div/input"
        # ).send_keys(self.env("TIKTOK_PASSWORD"))
        # self._drv.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        # sleep(self._drv.timeout)
        # page = self._drv.find_element(By.XPATH, '/html')
        # page.screenshot("templates/image/tiktok_login.png")

    def upload(self, video_path):
        pass
