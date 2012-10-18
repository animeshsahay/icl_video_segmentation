#!/usr/bin/env python
from cv2 import *

class VideoWrapper:
    def __init__(self, video, start=0, end=200):
        self.video = video
        self.start = start
        self.end = end
        bounds = (0, self.video.get(cv.CV_CAP_PROP_FRAME_COUNT))

        assert start <= end
        assert within((start, end), bounds)
        assert self.video.isOpened()

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.start == other.start and self.end == other.end and self.video == other.video

    def __ne__(self, other):
        return not self.__eq__(other)

    def getSegments(self, splitType):
        """
        Returns a list of segments, each a subset of the original video.
        The split method depends on parameter splitType.
        Return [self] if no split was possible.
        """
        segments = []
        frameNo = self.start
        currStart = self.start

        self.video.set(cv.CV_CAP_PROP_POS_FRAMES, self.start)

        # Grabs until frameNo=self.end or until actual end of the video is reached
        while self.video.grab() and frameNo <= self.end:
            (_, frame) = self.video.retrieve()
            # Convert to black and white
            frame = binarise(frame)

            # Splitting on black frames
            if splitType == SplitType.ON_BLACK_FRAMES and checkBlackFrame(frame):
                segments.append(VideoWrapper(self.video, currStart, frameNo))
                currStart = frameNo+1

            frameNo += 1

        # No split possible - return self
        if segments == []:
            return [self]
 
        return segments

    def play(self):
        """ Simple video player. """
        self.video.set(cv.CV_CAP_PROP_POS_FRAMES, self.start)
        while self.video.get(cv.CV_CAP_PROP_POS_FRAMES) < self.end:
            (_, frame) = self.video.read()
            imshow("Bob", frame)
            waitKey()

def binarise(frame):
    frame = cvtColor(frame, cv.CV_RGB2GRAY)
    (_, frame) = threshold(frame, 10, 255, THRESH_BINARY)
    return frame

def checkBlackFrame(frame):
    """ Checks if frame is entirely black. """
    for col in frame:
        for pixel in col:
            if pixel != 0:
                return False

    return True

# (a,b) within (c,d)
def within((a, b), (c, d)):
    return a >= c and a <= d and b >= c and b <= d

class SplitType:
    """ What to segment on. """
    ON_BLACK_FRAMES=0
    # on faces...
