#!/usr/bin/env python

import cv2
import enzyme
import unittest
from VideoInfo import VideoInfo

class VideoInfoTest(unittest.TestCase):
    def setUp(self):
        oldCapture = cv2.VideoCapture
        oldParse   = enzyme.parse
        enzyme.parse     = hijackedParse
        cv2.VideoCapture = hijackedCapture
        self.info = VideoInfo("dummy")
        enzyme.parse     = oldParse
        cv2.VideoCapture = oldCapture

    def test_numberOfFrames(self):
        self.assertEqual(self.info.numberOfFrames(), 100)

    def test_length(self):
        self.assertEqual(self.info.length(), 1)

    def test_prettyTitle(self):
        self.info.info.title = None
        self.assertEqual(self.info.prettyTitle(), "Unknown")
        self.info.info.title = "Bob"
        self.assertEqual(self.info.prettyTitle(), "Bob")

    def test_prettyLength(self):
        self.assertEqual(self.info.prettyLength(), "1 seconds (100 frames)")

def hijackedParse(filename):
    return Hijacked()

def hijackedCapture(filename):
    return Hijacked()


class Hijacked:
    def __init__(self):
        self.title = None

    def get(self, _):
        return 100
