from environs import Env

from upload.base_uploader import _BaseUploader


class _Youtube(_BaseUploader):
    def __init__(self, env: Env):
        self.env = env
        self._login()

    def _login(self):
        pass

    def upload(self, video_data):
        pass