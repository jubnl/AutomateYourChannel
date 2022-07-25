import pyttsx3


class TTS:
    def __init__(self):
        self._tts = pyttsx3.init()

    def add_tts(self, data):
        a_path = f"templates/audio/post_tts_{data['id']}.mp3"
        self._tts.save_to_file(data["title"], a_path)
        self._tts.runAndWait()
        data["a_title"] = a_path

        for i in data["comments"]:
            a_path = f"templates/audio/comment_tts_{i['id']}.mp3"
            self._tts.save_to_file(i["comment"], a_path)
            self._tts.runAndWait()
            i["a_comment"] = a_path

        return data
