from environs import Env


# upload video to youtube
class _Youtube:
    def __init__(self, env: Env):
        self.env = env
        self._login()

    def _login(self):
        pass

    def upload(self, video_data):
        pass