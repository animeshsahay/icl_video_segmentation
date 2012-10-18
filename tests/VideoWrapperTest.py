#!/usr/bin/env python
import unittest
from VideoWrapper import *

class VideoWrapperTest(unittest.TestCase):
    def setUp(self):
        self.skyfall = VideoCapture("res/skyfall.mp4")
        self.instance = VideoWrapper(self.skyfall, 30, 230)
        self.empty = VideoWrapper(self.skyfall, 3, 3)

    # start <= end in all segments
    def test_startLesserThanEnd(self):
        vids = [self.instance]

        for vid in vids:
            self.assertLessEqual(vid.start, vid.end)
            children = vid.getSegments(SplitType.ON_BLACK_FRAMES)

            # Not finished, append
            if children != [vid]:
                vids += children

    def test_unsplittableReturnsItself(self):
        self.assertEqual(self.empty.getSegments(SplitType.ON_BLACK_FRAMES), [self.empty])

    def test_structuralEquality(self):
        a = VideoWrapper(self.skyfall, 1, 2)
        b = VideoWrapper(self.skyfall, 1, 2)
        self.assertEqual(a, b)

    def test_structuralNotEquality(self):
        a = VideoWrapper(self.skyfall, 1, 3)
        b = VideoWrapper(self.skyfall, 1, 2)
        self.assertNotEqual(a, b)

    def test_faultsOnEmptyVideo(self):
        try:
            VideoWrapper(VideoCapture("empty"))
            self.fail("Didn't raise AssertionError")
        except AssertionError, _:
            pass

    # TODO : start and end out of bounds

if __name__ == '__main__':
    unittest.main()
