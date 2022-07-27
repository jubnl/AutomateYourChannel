# https://gist.github.com/gavin19/8e2ed7547efcbb376e94f2057f951526

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
        self._editor = VideoEditor(self._env)

        # get reddit instance
        self._reddit = Reddit(self._env)

        # get tts instance
        self._tts = TTS()

        # get uploaders
        self._ytb_uploader = get_uploader(UploaderType.Youtube, self._env)
        self._tiktok_uploader = get_uploader(UploaderType.TikTok, self._env)
        self._instagram_uploader = get_uploader(UploaderType.Instagram, self._env)

    # post a new video
    def run(self):
        post_data = self._tts.add_tts(self._reddit.get_post())
        video_data = self._editor.create_video(post_data)


if __name__ == "__main__":
    bot = Bot()
    bot.run()
