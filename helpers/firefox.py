from selenium.webdriver import Firefox, FirefoxOptions


# base class to get a firefox driver
class FirefoxDriver(Firefox):
    def __init__(self):
        self._timeout = 10
        opts = FirefoxOptions()
        opts.add_argument("--headless")
        opts.set_preference("dom.push.enabled", False)
        super().__init__(options=opts)

    @property
    def timeout(self):
        return self._timeout
