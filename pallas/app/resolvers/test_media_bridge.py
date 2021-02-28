#!/usr/bin/env pytest

import unittest
from .media_bridge import MediaBridge

class TestMediaBridge(unittest.TestCase):

    def test_get_next_media_uri(self):
        name = "Key and Peele"
        uris = [
            "KeyPeeleS01E01.mp4",
            "KeyPeeleS01E02.mp4",
            "KeyPeeleS01E03.mp4",
            "KeyPeeleS02E01.mp4",
            "KeyPeeleS02E02.mp4",
        ]

        res = MediaBridge._get_next_media_uri(name, last_played_uri=None, uris=None)
        self.assertEqual(None, res)

        res = MediaBridge._get_next_media_uri(name, last_played_uri=None, uris=[])
        self.assertEqual(None, res)

        res = MediaBridge._get_next_media_uri(name, last_played_uri=None, uris=uris)
        self.assertEqual(uris[0], res)

        res = MediaBridge._get_next_media_uri(name, last_played_uri="boblob", uris=uris)
        self.assertEqual(uris[0], res)

        res = MediaBridge._get_next_media_uri(name, last_played_uri=uris[0], uris=uris)
        self.assertEqual(uris[1], res)

        res = MediaBridge._get_next_media_uri(name, last_played_uri=uris[2], uris=uris)
        self.assertEqual(uris[3], res)

        res = MediaBridge._get_next_media_uri(name, last_played_uri=uris[4], uris=uris)
        self.assertEqual(uris[0], res)
