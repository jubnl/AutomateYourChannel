# https://gist.github.com/gavin19/8e2ed7547efcbb376e94f2057f951526
from pprint import pprint

from environs import Env

from editor import VideoEditor
from reddit import Reddit
from tts import TTS
from upload import get_uploader, UploaderType


class Bot:
    def __init__(self, ytb_creds, tiktok_creds, instagram_creds):
        self.env = Env()
        self.env.read_env()
        self.editor = VideoEditor()
        self.reddit = Reddit(
            self.env("REDDIT_CLIENT_ID"),
            self.env("REDDIT_CLIENT_SECRET"),
            self.env("REDDIT_USER_AGENT"),
            self.env("REDDIT_USERNAME"),
            self.env("REDDIT_PASSWORD")
        )
        self.tts = TTS()
        self.ytb_uploader = get_uploader(UploaderType.Youtube, ytb_creds)
        self.tiktok_uploader = get_uploader(UploaderType.TikTok, tiktok_creds)
        self.instagram_uploader = get_uploader(UploaderType.Instagram, instagram_creds)

    def post_new_video(self):
        post_data = self.tts.add_tts(self.reddit.get_post())
        # video_data = editor.create_video(post_data)
        # self.ytb_uploader.upload(video_data)
        # self.tiktok_uploader.upload(video_data)
        # self.instagram_uploader.upload(video_data)
        pprint(post_data)
