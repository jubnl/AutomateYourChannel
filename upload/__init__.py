from environs import Env

from .instagram import _Instagram
from .tiktok import _TikTok
from .youtube import _Youtube


class UploaderType:
    Youtube = "youtube"
    TikTok = "tiktok"
    Instagram = "instagram"


def get_uploader(uploader_type: str, env: Env):
    if uploader_type == UploaderType.Youtube:
        return _Youtube(env)
    elif uploader_type == UploaderType.TikTok:
        return _TikTok(env)
    elif uploader_type == UploaderType.Instagram:
        return _Instagram(env)
    else:
        raise Exception("Unknown uploader type")

