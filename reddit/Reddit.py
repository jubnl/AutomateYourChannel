from time import sleep

import praw
from environs import Env
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from helpers import FirefoxDriver


# base class to get all reddit posts data
class Reddit(praw.Reddit):
    def __init__(self, env: Env):
        # initialize praw
        super().__init__(
            client_id=env("REDDIT_CLIENT_ID"),
            client_secret=env("REDDIT_CLIENT_SECRET"),
            user_agent=env("REDDIT_USER_AGENT")
        )
        self.env = env
        self._drv = FirefoxDriver()
        self._base_url = "https://www.reddit.com"
        self._current_posts = {"comments": []}
        self.base_path = "templates\\image\\"
        # login into reddit using selenium
        self._login()

    def _login(self):
        # GET https://www.reddit.com/login/
        self._drv.get(self._base_url + "/login")

        # write username and password in proper fields
        self._drv.find_element(By.ID, "loginUsername").send_keys(self.env("REDDIT_USERNAME"))
        self._drv.find_element(By.ID, "loginPassword").send_keys(self.env("REDDIT_PASSWORD"))

        # click on login button
        btn = self._drv.find_element(By.CSS_SELECTOR, "button[type='submit']")
        btn.click()

        # wait for login to complete
        sleep(self._drv.timeout)

        # not always here, so in a try except
        # this is the "what topic are you interested in" popup
        try:
            close_btn = self._drv.find_element(
                By.XPATH,
                '/html/body/div[1]/div/div[2]/div[4]/div/div/div/header/div[1]/div[2]/button/i'
            )
            close_btn.click()
            sleep(self._drv.timeout)
        except NoSuchElementException:
            pass

        # kill cookie popup
        cookie = self._drv.find_element(By.XPATH, '//button[text()="Accept all"]')
        cookie.click()
        sleep(self._drv.timeout)

    def get_post(self, subreddit_name: str = "AskReddit"):
        self._current_posts = {"comments": []}

        # get subreddit hot post of the moment
        for submission in self.subreddit(subreddit_name).hot(limit=1):
            # selenium to that submission
            self._drv.get(self._base_url + submission.permalink)

            # check for nsfw warning page
            if submission.over_18:
                try:
                    self._drv.find_element(By.XPATH, '//button[text()="Yes"]').click()
                    sleep(self._drv.timeout)
                except NoSuchElementException:
                    pass

            # wait for the submission page to fully load
            try:
                post = WebDriverWait(self._drv, self._drv.timeout).until(
                    lambda x: x.find_element(By.ID, submission.name)
                )
            except TimeoutException:
                continue

            # if the page loaded, get the submission content (id, title) and screenshot the submission
            else:
                s_path = f"{self.base_path}post_{submission.name}.png"
                post.screenshot(s_path)
                self._current_posts["subreddit"] = subreddit_name
                self._current_posts["id"] = submission.name
                self._current_posts["title"] = submission.title
                self._current_posts["s_title"] = s_path
                self._current_posts["nsfw"] = submission.over_18

            # set max comments to get
            comment_amount = len(submission.comments) if len(submission.comments) <= 15 else 15

            # get comments and their content
            for comment in submission.comments[:comment_amount]:
                _id = f"t1_{comment.id}"  # comment div id
                try:
                    post = WebDriverWait(self._drv, self._drv.timeout).until(
                        lambda x: x.find_element(By.ID, _id)
                    )
                except TimeoutException:
                    continue
                # executed only if the comment loaded
                else:
                    # screenshot the comment and get the comment content
                    s_path = f"{self.base_path}comment_{_id}.png"
                    post.screenshot(s_path)
                    self._current_posts["comments"].append(
                        {
                            "id": _id,
                            "comment": comment.body,
                            "s_comment": s_path
                        }
                    )
        # return the post data
        return self._current_posts
