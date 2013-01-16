#!/usr/bin/env python

import unittest

from SegmentRegister import SegmentRegister

class SegmentRegisterTest(unittest.TestCase):
    def setUp(self):
        self.register = SegmentRegister([[i, i * 50, (i + 1) * 50] for i in xrange(5)])

    def test_last(self):
        for x in xrange(5):
            self.register.select(x)
            self.assertEqual(self.register.last(), x == 4)

    def test_first(self):
        for x in xrange(5):
            self.register.select(x)
            self.assertEqual(self.register.first(), x == 0)

    def test_empty(self):
        self.assertEqual(self.register.empty(), False)

    def test_length(self):
        self.assertEqual(self.register.length(), 5)

    def test_current(self):
        for x in xrange(5):
            self.register.select(x)
            self.assertEqual(self.register.current(), x)

    def test_next(self):
        self.register.select(0)
        for x in xrange(4):
            self.assertEqual(self.register.current(), x)
            self.register.next()
        self.assertEqual(self.register.current(), 4)
        self.assertRaises(AssertionError, self.register.next)

    def test_previous(self):
        self.register.select(4)
        for x in xrange(4):
            self.assertEqual(self.register.current(), 4 - x)
            self.register.previous()
        self.assertEqual(self.register.current(), 0)
        self.assertRaises(AssertionError, self.register.previous)

    def test_getIndexFromStartEnd(self):
        for x in xrange(5):
            self.register.select(x)
            self.assertEqual(x, self.register.getIndexFromStartEnd(x * 50, (x + 1) * 50))

    def test_currIndex(self):
        for x in xrange(5):
            self.register.select(x)
            self.assertEqual(self.register.currIndex(), x)
