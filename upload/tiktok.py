from upload.base_uploader import _BaseUploader


class _TikTok(_BaseUploader):
    def __init__(self, creds):
        self.creds = creds
        self._login()

    def _login(self):
        pass

    def upload(self, video_path):
        pass