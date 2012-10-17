#!/usr/bin/env python
import unittest
from VideoWrapper import *

class VideoWrapperTest(unittest.TestCase):
    def setUp(self):
        self.instance = VideoWrapper(None)

    # start <= end in all segments
    def test_startLTEnd(self):
        vids = [self.instance]

        for vid in vids:
            self.assertLessEqual(vid.start, vid.end)
            children = vid.getSegments(SplitType.ON_BLACK_FRAMES)

            # Not finished
            if children != [vid]:
                vids += children

if __name__ == '__main__':
    unittest.main()
