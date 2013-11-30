from babelfish import Language
import subliminal
from ...models import Subtitle
from ...settings import config
from .. import library
from .base import SubtitlesLoader


@library.subtitles
class SubliminalLoader(SubtitlesLoader):
    """Subliminal loader"""

    def get_subtitle_url(self, name):
        """Always return ok"""
        return Subtitle(
            name=name,
            wait_for_file=True,
        )

    def download(self, model):
        """Download subtitles using subliminal"""
        video = subliminal.scan_video(model.series.path)
        subtitles = subliminal.download_best_subtitles(
            {video}, {Language('eng')},
        )
        subliminal.save_subtitles(subtitles, True, config.download_path)
