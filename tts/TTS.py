import os

from environs import Env
from google.cloud import texttospeech as tts
from pydub import AudioSegment


class TTS:
    silent_time = 1.5
    fifty_nine_seconds = 59

    def __init__(self, env: Env):
        # init the tts engine
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getcwd() + "\\credentials\\" + env(
            "GOOGLE_AUTH_JSON_FILENAME")
        self._tts = tts.TextToSpeechClient()
        self.voice = tts.VoiceSelectionParams()
        self.voice.name = "en-US-Standard-J"
        self.voice.language_code = "en-US"
        self.voice.ssml_gender = tts.SsmlVoiceGender.MALE
        self.audio_config = tts.AudioConfig()
        self.audio_config.audio_encoding = tts.AudioEncoding.LINEAR16

        # self._tts = pyttsx3.init()
        self.base_path = "templates\\audio\\"

    def add_tts(self, data):
        request = self._prepare_request(data["title"])
        response = self._tts.synthesize_speech(request=request).audio_content
        a_path = f"{self.base_path}post_tts_{data['id']}.wav"
        self._save_to_file(response, a_path)
        data["a_title"] = a_path
        data["duration"] = AudioSegment.from_file(a_path).duration_seconds

        duration = data["duration"] + self.silent_time

        n = 0
        for comment in data["comments"]:
            if duration > self.fifty_nine_seconds:
                break
            a_path = f"{self.base_path}comment_tts_{comment['id']}.wav"
            request = self._prepare_request(comment["comment"])
            response = self._tts.synthesize_speech(request=request).audio_content
            self._save_to_file(response, a_path)
            comment_duration = AudioSegment.from_file(a_path).duration_seconds
            duration += comment_duration + self.silent_time
            comment["duration"] = comment_duration + self.silent_time
            comment["a_comment"] = a_path
            n += 1
        data["comments"] = data["comments"][:n]
        return data

        # print(response)

    @staticmethod
    def _save_to_file(data, path):
        with open(path, "bx") as f:
            f.write(data)

    def _prepare_request(self, text: str):
        synthesis_input = tts.SynthesisInput()
        synthesis_input.text = text
        request = tts.SynthesizeSpeechRequest()
        request.input = synthesis_input
        request.voice = self.voice
        request.audio_config = self.audio_config
        return request
