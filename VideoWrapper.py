#!/usr/bin/env python
import cv
from datetime import time

class VideoWrapper:
	def __init__(self, video, start=None, end=None):
		self.video = video
		self.start = start
		self.end = end

	def getSegments(self, type):
		if type == SplitType.ON_BLACK_FRAMES:
			return [self]


class SplitType:
	ON_BLACK_FRAMES=0
	# on faces...