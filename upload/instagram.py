from environs import Env


# instagram uploader class
# still need to be implemented
class _Instagram:
    def __init__(self, env: Env):
        self.env = env
        self._login()

    def _login(self):
        pass

    def upload(self, video_path):
        pass