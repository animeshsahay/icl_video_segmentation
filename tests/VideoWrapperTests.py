#!/usr/bin/env python

import unittest

import cv2
from VideoWrapper import VideoWrapper, BoundsError, within, toOffset

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
                           (frameCount, frameCount),
                           (frameCount - 1, frameCount),
                           (frameCount - 1, frameCount - 1)]:
            self.assertIsNotNone(VideoWrapper(self.skyfall, start, end))

    def test_faceMemoisation(self):
        """
        Check return time of memoisation and faces are the same
        """
        wrapper = VideoWrapper(self.skyfall, 350, 380)
        self.assertIsNone(wrapper.faces)
        faces = wrapper.getFaces()
        self.assertIsNotNone(wrapper.faces)
        wrapper.video = None
        self.assertEqual(faces, wrapper.getFaces())

    def test_faceReturn(self):
        """
        Check at least a certain amount of faces are returned
        """
        wrapper = VideoWrapper(self.skyfall, 360, 380)
        self.assertTrue(len(wrapper.getFaces()) >= 15 and len(wrapper.getFaces()) <= 20)

    def test_frameReturn(self):
        """
        Check a certain frame is returned
        """
        self.assertIsNotNone(VideoWrapper(self.skyfall, 360, 380).getFrame(360))
        self.assertRaises(AssertionError, VideoWrapper(self.skyfall, 360, 380).getFrame, 359)

    def test_checkWithin(self):
        """
        Check within returns true in the correct circumstances
        """
        vals = [((0, 0), (0, 0), True),
                ((0, 10), (0, 10), True),
                ((0, 10), (0, 0), False),
                ((-5, 5), (-5, 10), True),
                ((0, 5), (2, 4), False),
                ((2, 4), (0, 5), True)]

        for inside, outside, result in vals:
            self.assertEqual(within(inside, outside), result)

    def test_checkToOffset(self):
        """
        Check that offsets are correctly converted
        """
        vals = [(0, "0:0:0.000"),
                (100, "0:1:40.000"),
                (5000, "1:23:20.000"),
                (0.5, "0:0:0.500"),
                (0.125, "0:0:0.125")]

        for i, s in vals:
            self.assertEqual(toOffset(i), s)
            if i != 0:
                self.assertEqual(toOffset(-i), "-{0}".format(s))
