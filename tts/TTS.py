import os
from ast import literal_eval
from base64 import b64decode
from urllib.parse import quote

from pydub import AudioSegment
from requests import post


class TTS:
    silent_time = 1.5
    fifty_nine_seconds = 59

    def __init__(self):
        self.base_url = "https://warp-co.rs/https://api16-normal-useast5.us.tiktokv.com/media/api/text/speech/invoke" \
                        "/?text_speaker=en_uk_003&req_text= "
        self.headers = {"Origin": "https://warp-co.rs/"}
        self.base_path = "templates\\audio\\"

    def add_tts(self, post_data):
        response = post(self.base_url + quote(post_data["title"]), headers=self.headers)
        a_path = self.base_path + f"post_tts_{post_data['id']}.wav"
        post_data["duration"] = self._process_response(response, a_path) + self.silent_time
        post_data["a_title"] = a_path

        duration = post_data["duration"]

        n = 0
        for comment in post_data["comments"]:
            if duration > self.fifty_nine_seconds:
                break
            n += 1
            a_path = f"{self.base_path}comment_tts_{comment['id']}.wav"
            response = post(self.base_url + quote(comment["comment"]), headers=self.headers)
            comment["duration"] = self._process_response(response, a_path) + self.silent_time
            comment["a_comment"] = a_path
            duration += comment["duration"]
        post_data["comments"] = post_data["comments"][:n]
        os.remove("tmp.mp3")
        return post_data

    @staticmethod
    def _process_response(response, wav_path):
        with open("tmp.mp3", "wb") as f:
            f.write(b64decode(literal_eval(response.text)["data"]["v_str"]))
        tmp = AudioSegment.from_mp3("tmp.mp3")
        tmp.export(wav_path, format="wav")
        return tmp.duration_seconds
