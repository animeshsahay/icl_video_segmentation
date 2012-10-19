#!/usr/bin/env python
import unittest
from Client import *

class ClientTest(unittest.TestCase):
  def setUp(self):
    self.instance = Client(None, None)

  def test_notExistingVideo(self, video):
    self.video = video
    self.assertRaise(IOError, open, os.path.join())

  def test_invalidSplitType(self, splitType):
    self.splitType = splitType
    validSplitTypes = [k for k in Test.__dict__.keys() if not k.startswith('__')]
    self.assertTrue(splitType in validSplitTypes)
