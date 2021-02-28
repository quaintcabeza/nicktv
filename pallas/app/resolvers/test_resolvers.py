#!/usr/bin/env pytest

from datetime import datetime
import unittest
from unittest.mock import patch
from resolvers import resolve_now_playing, db_bridge, media_bridge

class TestResolvers(unittest.TestCase):

    @patch.object(db_bridge, 'get_now_playing')
    def test_resolve_now_playing_nothing_scheduled(self, mock_get_now_playing):
        mock_get_now_playing.return_value = None

        exp = {
            "__typename": "NothingPlaying",
            "tryAgainInMin": 1
        }
        res = resolve_now_playing("_", "_")
        self.assertEqual(exp, res)

    @patch.object(db_bridge, 'get_last_played')
    @patch.object(db_bridge, 'get_now_playing')
    def test_resolve_now_playing_already_played(self, mock_get_now_playing, mock_get_last_played):
        mock_get_now_playing.return_value = {
            "name": "Key and Peele",
            "showStart": datetime(2021, 2, 25, 15, 0).isoformat(),
            "showEnd": datetime(2021, 2, 25, 15, 30).isoformat()
        }
        mock_get_last_played.return_value = {
            "name": "Key and Peele",
            "uri": "bobloblaw",
            "lastPlayed": datetime(2021, 2, 25, 15, 23).isoformat()
        }

        exp = {
            "__typename": "NothingPlaying",
            "tryAgainInMin": 1
        }
        res = resolve_now_playing("_", "_")
        self.assertEqual(exp, res)

    @patch.object(media_bridge, 'get_next_audio_uri')
    @patch.object(media_bridge, 'get_next_video_uri')
    @patch.object(db_bridge, 'get_last_played')
    @patch.object(db_bridge, 'get_now_playing')
    def test_resolve_now_playing_nothing_found(
        self,
        mock_get_now_playing,
        mock_get_last_played,
        mock_get_next_video_uri,
        mock_get_next_audio_uri
    ):
        mock_get_now_playing.return_value = {
            "name": "Key and Peele",
            "showStart": datetime(2021, 2, 25, 15, 0).isoformat(),
            "showEnd": datetime(2021, 2, 25, 15, 30).isoformat()
        }
        mock_get_last_played.return_value = None
        mock_get_next_video_uri.return_value = None
        mock_get_next_audio_uri.return_value = None

        exp = {
            "__typename": "NothingPlaying",
            "tryAgainInMin": 1
        }
        res = resolve_now_playing("_", "_")
        self.assertEqual(exp, res)

    @patch.object(media_bridge, 'get_next_audio_uri')
    @patch.object(media_bridge, 'get_next_video_uri')
    @patch.object(db_bridge, 'get_last_played')
    @patch.object(db_bridge, 'get_now_playing')
    def test_resolve_now_playing_video_found_never_played_before(
        self,
        mock_get_now_playing,
        mock_get_last_played,
        mock_get_next_video_uri,
        mock_get_next_audio_uri
    ):
        mock_get_now_playing.return_value = {
            "name": "Key and Peele",
            "showStart": datetime(2021, 2, 25, 15, 0).isoformat(),
            "showEnd": datetime(2021, 2, 25, 15, 30).isoformat()
        }
        mock_get_last_played.return_value = None
        mock_get_next_video_uri.return_value = "/bublublub.mp4"
        mock_get_next_audio_uri.return_value = "/piper.mp3"

        exp = {
            "__typename": "Video",
            "uri": "/bublublub.mp4",
            "name": "Key and Peele",
            "url": "http://192.168.1.22:2222/bublublub.mp4" ,
            "lastPlayed": None
        }
        res = resolve_now_playing("_", "_")
        self.assertEqual(exp, res)

    @patch.object(media_bridge, 'get_next_audio_uri')
    @patch.object(media_bridge, 'get_next_video_uri')
    @patch.object(db_bridge, 'get_last_played')
    @patch.object(db_bridge, 'get_now_playing')
    def test_resolve_now_playing_video_found(
        self,
        mock_get_now_playing,
        mock_get_last_played,
        mock_get_next_video_uri,
        mock_get_next_audio_uri
    ):
        mock_get_now_playing.return_value = {
            "name": "Key and Peele",
            "showStart": datetime(2021, 2, 25, 15, 0).isoformat(),
            "showEnd": datetime(2021, 2, 25, 15, 30).isoformat()
        }
        mock_get_last_played.return_value = {
            "name": "Key and Peele",
            "uri": "bobloblaw",
            "lastPlayed": datetime(2021, 2, 24, 15, 23).isoformat()
        }
        mock_get_next_video_uri.return_value = "/bublublub.mp4"
        mock_get_next_audio_uri.return_value = "/piper.mp3"

        exp = {
            "__typename": "Video",
            "uri": "/bublublub.mp4",
            "name": "Key and Peele",
            "url": "http://192.168.1.22:2222/bublublub.mp4" ,
            "lastPlayed": datetime(2021, 2, 24, 15, 23).isoformat()
        }
        res = resolve_now_playing("_", "_")
        self.assertEqual(exp, res)

    @patch.object(media_bridge, 'get_next_audio_uri')
    @patch.object(media_bridge, 'get_next_video_uri')
    @patch.object(db_bridge, 'get_last_played')
    @patch.object(db_bridge, 'get_now_playing')
    def test_resolve_now_playing_audio_found(
        self,
        mock_get_now_playing,
        mock_get_last_played,
        mock_get_next_video_uri,
        mock_get_next_audio_uri
    ):
        mock_get_now_playing.return_value = {
            "name": "Key and Peele",
            "showStart": datetime(2021, 2, 25, 15, 0).isoformat(),
            "showEnd": datetime(2021, 2, 25, 15, 30).isoformat()
        }
        mock_get_last_played.return_value = {
            "name": "Key and Peele",
            "uri": "bobloblaw",
            "lastPlayed": datetime(2021, 2, 24, 15, 23).isoformat()
        }
        mock_get_next_video_uri.return_value = None
        mock_get_next_audio_uri.return_value = "/piper.mp3"

        exp = {
            "__typename": "Audio",
            "uri": "/piper.mp3",
            "name": "Key and Peele",
            "url": "http://192.168.1.22:2222/piper.mp3" ,
            "lastPlayed": datetime(2021, 2, 24, 15, 23).isoformat()
        }
        res = resolve_now_playing("_", "_")
        self.assertEqual(exp, res)
