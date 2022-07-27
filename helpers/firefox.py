import os

from selenium.webdriver import Firefox, FirefoxOptions


class FirefoxDriver(Firefox):
    def __init__(self):
        self._timeout = 10
        opts = FirefoxOptions()
        opts.add_argument("--headless")
        opts.set_preference("dom.push.enabled", False)

        # add geckodriver to path temporarily
        os.environ["PATH"] += f"{os.getcwd()}\\drivers;"
        super().__init__(options=opts)

    @property
    def timeout(self):
        return self._timeout
