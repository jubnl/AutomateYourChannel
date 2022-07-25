from .instagram import _Instagram
from .tiktok import _TikTok
from .youtube import _Youtube


class UploaderType:
    Youtube = "youtube"
    TikTok = "tiktok"
    Instagram = "instagram"


def get_uploader(uploader_type: str, creds):
    if uploader_type == UploaderType.Youtube:
        return _Youtube(creds)
    elif uploader_type == UploaderType.TikTok:
        return _TikTok(creds)
    elif uploader_type == UploaderType.Instagram:
        return _Instagram(creds)
    else:
        raise Exception("Unknown uploader type")

