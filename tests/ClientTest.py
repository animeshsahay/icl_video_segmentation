#!/usr/bin/env python
import unittest
from Client import *

class ClientTest(unittest.TestCase):
  def test_noVideo(self):
    self.assertRaises(AssertionError, Client, None, None)

  def test_notExistingVideo(self):
    self.assertRaises(IOError, open, "/")

  def test_validAndInvalidSplitType(self):
    validSplitTypes = [v for (k, v) in SplitType.__dict__.items() if not k.startswith('__')]
    for i in range(0, len(validSplitTypes)+10):
      if i in validSplitTypes:
        Client("res/skyfall.mp4", i)
      else:
        self.assertRaises(AssertionError, Client, "res/skyfall.mp4", i)
