import pyttsx3


class TTS:
    def __init__(self):
        # init the tts engine
        self._tts = pyttsx3.init()

    def add_tts(self, data):
        # create tts for post/comment content
        a_path = f"templates/audio/post_tts_{data['id']}.mp3"
        self._tts.save_to_file(data["title"], a_path)
        self._tts.runAndWait()
        data["a_title"] = a_path

        for comment in data["comments"]:
            a_path = f"templates/audio/comment_tts_{i['id']}.mp3"
            self._tts.save_to_file(comment["comment"], a_path)
            self._tts.runAndWait()
            comment["a_comment"] = a_path

        # return data with tts mp3 file paths
        return data
