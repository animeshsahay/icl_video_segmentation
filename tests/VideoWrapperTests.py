#!/usr/bin/env python

import unittest

import cv2
from VideoWrapper import VideoWrapper, BoundsError

class VideoWrapperTest(unittest.TestCase):
    def setUp(self):
        self.skyfall = cv2.VideoCapture("res/skyfall.mp4")

    def test_invalid(self):
        self.assertRaises(IOError, VideoWrapper, None)

        video = cv2.VideoCapture("res/skyfall.mp4")
        video.release()
        self.assertRaises(IOError, VideoWrapper, video)

    def test_invalidBounds(self):
        frameCount = int(self.skyfall.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
        for start, end in [(-10, -5),
                           (-5, -10),
                           (-5, 5),
                           (5, -5),
                           (5, 0),
                           (frameCount, frameCount),
                           (frameCount, frameCount + 1),
                           (frameCount - 1, frameCount + 1),
                           (0, frameCount + 1),
                           (-1, frameCount)]:
            self.assertRaises(BoundsError, VideoWrapper, self.skyfall, start, end)

    def test_validBounds(self):
        frameCount = int(self.skyfall.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
        for start, end in [(0, 5),
                           (0, 0),
                           (5, 10),
                           (5, 6),
                           (0, frameCount),
                           (frameCount - 1, frameCount),
                           (frameCount - 1, frameCount - 1)]:
            self.assertIsNotNone(VideoWrapper(self.skyfall, start, end))

    @unittest.skip("Not implemented")
    def test_writeAndRead(self):
        """
        Writes a segment to disk, reads it in and checks length, width, height, etc
        """
        self.fail("Not implemented")

    @unittest.skip("Not implemented")
    def test_faceMemoisation(self):
        """
        Check return time of memoisation and faces are the same
        """
        self.fail("Not implemented")

    @unittest.skip("Not implemented")
    def test_faceReturn(self):
        """
        Check at least a certain amount of faces are returned
        """
        self.fail("Not implemented")

    @unittest.skip("Not implemented")
    def test_frameReturn(self):
        """
        Check at least a certain amount of faces are returned
        """
        self.fail("Not implemented")
