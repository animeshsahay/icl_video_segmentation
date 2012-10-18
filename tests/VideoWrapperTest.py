#!/usr/bin/env python
import unittest
from VideoWrapper import *

class VideoWrapperTest(unittest.TestCase):
    def setUp(self):
        self.skyfall = VideoCapture("res/skyfall.mp4")
        self.instance = VideoWrapper(self.skyfall, 30, 230)
        self.empty = VideoWrapper(self.skyfall, 3, 3)

    def test_faultsOnStartBiggerThanEnd(self):
        try:
            VideoWrapper(self.skyfall, 10, 5)
            self.fail("Didn't raise AssertionError on start > end")
        except AssertionError, _:
            pass

    # start <= end in all segments
    def test_startLesserThanEndRec(self):
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
            self.fail("Didn't raise AssertionError on wrong filename")
        except AssertionError, _:
            pass

    def test_within(self):
        self.assertTrue(within((1,2), (0,3)))
        self.assertFalse(within((0,3), (1,2)))
        self.assertTrue(within((3,2), (0,4)))
        self.assertFalse(within((9, 2), (1, 8)))

    def test_faultsOnOutOfBounds(self):
        try:
            VideoWrapper(self.skyfall, -1, 2)
            self.fail("Didn't raise AssertionError on negative start index")
        except AssertionError, _:
            pass

    def test_blackFrames(self):
        self.skyfall.set(cv.CV_CAP_PROP_POS_FRAMES, 0)
        (_, blackFrame) = self.skyfall.read()
        self.skyfall.set(cv.CV_CAP_PROP_POS_FRAMES, 31)
        (_, notSoBlackFrame) = self.skyfall.read()

        
        self.assertTrue(checkBlackFrame(binarise(blackFrame)))
        self.assertFalse(checkBlackFrame(binarise(notSoBlackFrame)))

if __name__ == '__main__':
    unittest.main()
