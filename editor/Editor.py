import os

from environs import Env
from pydub import AudioSegment


# class that will be used to create the video
# still need to implement it
class VideoEditor:
    two_seconds = 2

    def __init__(self, env: Env):
        self._env = env
        os.environ["IMAGEMAGICK_BINARY"] = f"{os.getcwd()}\\imagemagick\\magick.exe;"

        # ensure that ffmpeg is in the path
        os.environ["PATH"] += f"{os.getcwd()}\\ffmpeg\\bin;"

    def create_video(self, post_data):
        audio_path = self._create_audio(post_data)
        return audio_path

    def _create_audio(self, post_data):
        audios = [AudioSegment.from_file(os.getcwd() + "\\" + post_data["a_title"], "mp3"),
                  AudioSegment.silent(duration=self.two_seconds * 1000)]
        for i in post_data["comments"]:
            audios.append(AudioSegment.from_mp3(i["a_comment"]))
            audios.append(AudioSegment.silent(duration=self.two_seconds * 1000))
        merged = audios[0]
        for i in range(1, len(audios)):
            merged += audios[i]
        output_path = f"templates\\audio\\merged_{post_data['id']}.mp3"
        merged.export(output_path, format="mp3")
        return output_path
