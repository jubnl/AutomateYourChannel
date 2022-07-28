import os

from PIL import Image
from pydub import AudioSegment


# class that will be used to create the video
# still need to implement it
class VideoEditor:
    silent_time = 1.5
    silent_clip = AudioSegment.silent(duration=silent_time * 1000)
    fifty_nine_seconds = 59
    width = 1080
    height = 1920

    def __init__(self):
        # set env var
        os.environ["IMAGEMAGICK_BINARY"] = f"{os.getcwd()}\\imagemagick\\magick.exe;"
        os.environ["PATH"] += f"{os.getcwd()}\\ffmpeg\\bin;"

    def create_video(self, post_data):
        post_data = self._create_audio(post_data)
        self._delete_audios()
        post_data = self._update_last_clip_time(post_data)
        self._resizes_images(post_data)
        # title_clip = ImageClip(post_data["s_title"], duration=post_data["duration"])
        return post_data

    def _create_audio(self, post_data):
        merge = AudioSegment.from_file(post_data["a_title"], "wav")
        merge += self.silent_clip
        for i in post_data["comments"]:
            merge += AudioSegment.from_file(i["a_comment"], format="wav")
            merge += self.silent_clip
        merge = merge[:self.fifty_nine_seconds * 1000]
        output_path = f"templates\\audio\\merged_{post_data['id']}.wav"
        merge.export(output_path, format="wav")
        post_data["a_merged"] = output_path

        return post_data

    @staticmethod
    def _delete_audios():
        filelist = [f for f in os.listdir("templates\\audio") if f.endswith(".wav") and not f.startswith("merged_")]
        for f in filelist:
            os.remove(f"templates\\audio\\{f}")

    def _resizes_images(self, post_data):
        background = Image.new("L", (self.width, self.height), 0)
        foreground = Image.open(post_data["s_title"])
        background.paste(
            foreground,
            (int((self.width - foreground.width) / 2),
             int(self.height * .25)),
            foreground
        )
        background.save(post_data["s_title"])
        for comment in post_data["comments"]:
            background = Image.new("L", (self.width, self.height), 0)
            foreground = Image.open(comment["s_comment"])
            background.paste(
                foreground,
                (int((self.width - foreground.width) / 2),
                 int(self.height * .25)),
                foreground
            )
            background.save(comment["s_comment"])

    @staticmethod
    def _update_last_clip_time(post_data):
        total = 59
        total -= post_data["duration"]
        for i in post_data["comments"]:
            total -= i["duration"]
        post_data["comments"][-1]["duration"] += total
        return post_data
