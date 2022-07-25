from selenium.webdriver import Firefox, FirefoxOptions


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class FirefoxDriver(Firefox):
    def __init__(self):
        opts = FirefoxOptions()
        opts.add_argument("--headless")
        opts.set_preference("dom.push.enabled", False)
        super().__init__(options=opts)
