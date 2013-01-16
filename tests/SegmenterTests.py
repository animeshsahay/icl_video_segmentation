#!/usr/bin/env python

import unittest
from Segmenter import *

class SegmenterTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_checkBlackFrame(self):
        self.assertTrue(checkBlackFrame([[]]))
        self.assertTrue(checkBlackFrame([[0, 0, 0, 0, 0]]))
        self.assertFalse(checkBlackFrame([[0, 1, 0, 0, 0]]))

    def test_mergeDefaults(self):
        defaults = {"stateCallback"    : lambda x: None,
                    "progressCallback" : lambda x: None,
                    "currStep"         : 0,
                    "segmentLength"    : 20,
                    "verbose"          : 1}

        self.compare(mergeDefaults({}), defaults)

        defaults["verbose"] = 0
        self.compare(mergeDefaults({"verbose" : 0}), defaults)

    def compare(self, dict1, dict2):
        for key1, value1 in dict1.items():
            for key2, value2 in dict2.items():
                if key1 == key2:
                    self.assertTrue(value1 == value2 or (callable(value1) and callable(value2)))
