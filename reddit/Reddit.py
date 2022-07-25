from time import sleep

import praw
import pyttsx3
from environs import Env
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class Reddit(praw.Reddit):
    def __init__(self, env: Env):
        super().__init__(
            client_id=env("REDDIT_CLIENT_ID"),
            client_secret=env("REDDIT_CLIENT_SECRET"),
            user_agent=env("REDDIT_USER_AGENT")
        )
        self._username = env("REDDIT_USERNAME")
        self._password = env("REDDIT_PASSWORD")
        self._subreddit_name = None
        opts = FirefoxOptions()
        opts.add_argument("--headless")
        opts.set_preference("dom.push.enabled", False)
        self._drv = Firefox(options=opts)
        self._timeout = 10
        self._base_url = "https://www.reddit.com"
        self._current_posts = {"comments": []}
        self._login()
        self._tts = pyttsx3.init()

    @property
    def subreddit_name(self):
        if not self._subreddit_name:
            self._subreddit_name = "AskReddit"
        return self._subreddit_name

    @subreddit_name.setter
    def subreddit_name(self, subreddit):
        self._subreddit_name = subreddit

    def _login(self):
        self._drv.get(self._base_url + "/login")
        user = self._drv.find_element(By.ID, "loginUsername")
        user.send_keys(self._username)
        pwd = self._drv.find_element(By.ID, "loginPassword")
        pwd.send_keys(self._password)
        btn = self._drv.find_element(By.CSS_SELECTOR, "button[type='submit']")
        btn.click()
        sleep(self._timeout)

        # not always here, so in a try except
        try:
            close_btn = self._drv.find_element(
                By.XPATH,
                '/html/body/div[1]/div/div[2]/div[4]/div/div/div/header/div[1]/div[2]/button/i'
            )
            close_btn.click()
            sleep(self._timeout)
        except NoSuchElementException:
            pass

        # kill cookie popup
        cookie = self._drv.find_element(By.XPATH, '//button[text()="Accept all"]')
        cookie.click()
        sleep(self._timeout)

    def get_post(self, subreddit: str = None):
        if subreddit:
            self.subreddit_name = subreddit

        self._current_posts = {"comments": []}

        for submission in self.subreddit(self.subreddit_name).hot(limit=1):
            self._drv.get(self._base_url + submission.permalink)
            if submission.over_18:
                try:
                    self._drv.find_element(By.XPATH, '//button[text()="Yes"]').click()
                    sleep(self._timeout)
                except NoSuchElementException:
                    pass
            try:
                post = WebDriverWait(self._drv, self._timeout).until(
                    lambda x: x.find_element(By.ID, submission.name)
                )
            except TimeoutException:
                continue
            else:
                s_path = f"templates/image/post_{submission.name}.png"
                post.screenshot(s_path)
                self._current_posts["id"] = submission.name
                self._current_posts["title"] = submission.title
                self._current_posts["s_title"] = s_path
                self._current_posts["nsfw"] = submission.over_18

            comment_amount = len(submission.comments) if len(submission.comments) <= 15 else 15

            for comment in submission.comments[:comment_amount]:
                _id = f"t1_{comment.id}"
                try:
                    post = WebDriverWait(self._drv, self._timeout).until(
                        lambda x: x.find_element(By.ID, _id)
                    )
                except TimeoutException:
                    continue
                else:
                    s_path = f"templates/image/comment_{_id}.png"
                    post.screenshot(s_path)
                    self._current_posts["comments"].append(
                        {
                            "id": _id,
                            "comment": comment.body,
                            "s_comment": s_path
                        }
                    )
        return self._current_posts
