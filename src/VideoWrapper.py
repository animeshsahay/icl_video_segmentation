#!/usr/bin/env python
from cv2 import *

class VideoWrapper:
    """
    Wrapper around VideoCapture supporting segmentation.
    """
    def __init__(self, video, start=None, end=None):
        """
        Constructor takes in a VideoCapture object and an optional start and
        end parameter for the segment.

        If start is None, assume the segment starts at 0.
        If end is None, assume the segment ends at the last valid frame in the video.

        Note that the valid frames in the segment are in range [start; end],
        i.e. end is inclusive.
        """
        assert video.isOpened()

        self.video = video
        bounds = (0, int(self.video.get(cv.CV_CAP_PROP_FRAME_COUNT)))

        self.start = start if start != None else bounds[0]
        self.end = end if end != None else bounds[1]-1

        assert self.start <= self.end
        assert within((self.start, self.end), bounds)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.start == other.start and self.end == other.end and self.video == other.video

    def __ne__(self, other):
        return not self.__eq__(other)

    def write(self, filename, codec="THEO"):
        """
        Writes the segment to file.

        Defaults to OGG Theora (unavailable on Mac - give codec "DIVX" with
        extension ".avi").
        """
        fps = self.video.get(cv.CV_CAP_PROP_FPS)
        width = int(self.video.get(cv.CV_CAP_PROP_FRAME_WIDTH))
        height = int(self.video.get(cv.CV_CAP_PROP_FRAME_HEIGHT))

        writer = VideoWriter(filename, cv.CV_FOURCC(*codec), fps, (width, height))

        self.video.set(cv.CV_CAP_PROP_POS_FRAMES, self.start)
        for i in xrange(self.start, self.end):
            _, frame = self.video.read()
            writer.write(frame)

    def getSegments(self, splitType):
        """
        Returns a list of segments, each a subset of the original video.
        The split method depends on parameter splitType.
        Return [self] if no split was possible.

        Assumes that the object was properly initialised, i.e. that self.start
        < max frames in the video.
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
    """
    Binarise a grayscale frame. Threshold of 10 to maximise number of white
    pixels, thereby speeding up non black frame detection in checkBlackFrame.
    """
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
