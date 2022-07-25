# https://gist.github.com/gavin19/8e2ed7547efcbb376e94f2057f951526
from pprint import pprint

from environs import Env

from editor import VideoEditor
from reddit import Reddit
from tts import TTS
from upload import get_uploader, UploaderType


class Bot:
    def __init__(self):
        # get environment variables
        self._env = Env()
        self._env.read_env()

        # get editor
        self._editor = VideoEditor()

        # get reddit instance
        self._reddit = Reddit(self._env)

        # get tts instance
        self._tts = TTS()

        # get uploaders
        self._ytb_uploader = get_uploader(UploaderType.Youtube, self._env)
        self._tiktok_uploader = get_uploader(UploaderType.TikTok, self._env)
        self._instagram_uploader = get_uploader(UploaderType.Instagram, self._env)

    # post a new video
    def post_new_video(self):
        post_data = self._tts.add_tts(self._reddit.get_post())
        # video_data = editor.create_video(post_data)
        # self.ytb_uploader.upload(video_data)
        # self.tiktok_uploader.upload(video_data)
        # self.instagram_uploader.upload(video_data)
        pprint(post_data)


if __name__ == "__main__":
    bot = Bot()
    bot.post_new_video()
