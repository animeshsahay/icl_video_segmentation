#!/usr/bin/env python

import math
import unittest

import cv2
import numpy as np
from FaceClustering import *

class FaceClusteringTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_clusterFaces(self):
        self.assertEqual(clusterFaces([], {}), [])
        self.assertEqual(clusterFaces([0, 1, 2, 3], {"clusterAlgorithm" : lambda f, o: [[0, 2], [1, 3]]}), [[0, 2], [1, 3]])

    def test_getDist(self):
        tests = [([5, 6, 7], [0, 0, 0], math.sqrt(110)),
                 ([3, 4], [0, 0], 5),
                 ([], [], 0)]

        for vals1, vals2, expected in tests:
            self.assertEqual(getDist(np.array(vals1), np.array(vals2)), expected)

    def test_mergeDefaults(self):
        defaults = {"clusterThreshold" : 0.63,
                    "comparator"       : PCAComparator,
                    "clusterAlgorithm" : meanShiftCluster,
                    "k"                : 2,
                    "cutoff"           : 1,
                    "maxIterations"    : -1}

        self.compare(mergeDefaults({}), defaults)

        defaults["k"] = 5
        self.compare(mergeDefaults({"k" : 5}), defaults)

    def compare(self, dict1, dict2):
        for key1, value1 in dict1.items():
            for key2, value2 in dict2.items():
                if key1 == key2:
                    self.assertTrue(value1 == value2 or (callable(value1) and callable(value2)))
