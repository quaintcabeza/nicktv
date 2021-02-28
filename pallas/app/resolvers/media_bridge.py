import logging
import urllib
from wcmatch import wcmatch


logger = logging.getLogger('gunicorn.error.' + __name__)


class MediaBridge:
    @staticmethod
    def get_instance():
        return MediaBridge(
            root='/www/media',
            supported_video_formats='*.mp4|*.m4v|*.mov',
            supported_audio_formats='*.mp3'
        )

    def __init__(self, root: str, supported_video_formats: str, supported_audio_formats: str):
        self.supported_video_formats = supported_video_formats
        self.supported_audio_formats = supported_audio_formats
        self.root = root

    def get_next_video_uri(self, name: str, last_played_uri: str):
        uris = self._get_sorted_media_file_uris(name, self.supported_video_formats)
        return self._get_next_media_uri(name, last_played_uri, uris)

    def get_next_audio_uri(self, name: str, last_played_uri: str):
        uris = self._get_sorted_media_file_uris(name, self.supported_audio_formats)
        return self._get_next_media_uri(name, last_played_uri, uris)

    @classmethod
    def _get_next_media_uri(cls, name: str, last_played_uri: str, uris: list[str]):
        if not uris:
            return None

        if not last_played_uri:
            logger.info(f"Never played on NickTV before: {name}")
            return uris[0]

        if not last_played_uri in uris:
            logger.warning(f"Did not find uri [{last_played_uri}] in list for: {name}")
            return uris[0]

        idx = uris.index(last_played_uri)
        next_idx = (idx + 1) % len(uris)
        logger.info(f"Next on NickTV for {name}: {uris[next_idx]}")
        return uris[next_idx]

    def _get_sorted_media_file_uris(self, name: str, supported_formats: str):
        all_uris = sorted(wcmatch.WcMatch(
            self.root,
            supported_formats,
            flags= wcmatch.RECURSIVE | wcmatch.IGNORECASE
        ).match())

        lower_case_name = name.lower()
        uris_for_name = [
            urllib.parse.quote(uri)
            for uri in all_uris
            if lower_case_name in uri.lower()
        ]
        return uris_for_name
