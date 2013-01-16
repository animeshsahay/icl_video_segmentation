#!/usr/bin/env python

import cv2
import numpy as np
from subprocess import call
from os import devnull

class BoundsError(Exception):
    def __init__(self):
        pass

class VideoWrapper:
    """
    Wrapper around VideoCapture supporting segmentation.
    """
    def __init__(self, video, start = None, end = None):
        """
        Constructor takes in a VideoCapture object and an optional start and
        end parameter for the segment.

        If start is None, assume the segment starts at 0.
        If end is None, assume the segment ends at the last valid frame in the video.

        Note that the valid frames in the segment are in range [start, end),
        i.e. end is exclusive.
        """

        if video is None or not video.isOpened():
            raise IOError

        self.video  = video
        self.bounds = (0, int(self.video.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)))
        self.faces  = None

        self.start = start if start != None else self.bounds[0]
        self.end   = end   if end   != None else self.bounds[1]
        self.fps   = self.video.get(cv2.cv.CV_CAP_PROP_FPS)
        self.length = (self.end - self.start) / self.fps

        if self.start > self.end or not within((self.start, self.end), self.bounds):
            raise BoundsError

    def __eq__(self, other):
        return isinstance(other, self.__class__)                     \
               and self.video == other.video                         \
               and self.start == other.start                         \
               and self.end   == other.end

    def write(self, filename, codec,
              frameModifier = lambda frameNo, frame: frame, audiofile = None):
        """
        Writes the segment to file.
        """
        width = int(self.video.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))
        height = int(self.video.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))

        writer = cv2.VideoWriter(filename, cv2.cv.CV_FOURCC(*codec), self.fps, (width, height))

        self.video.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, self.start)
        for i in xrange(self.start, self.end):
            _, frame = self.video.read()
            frame = frameModifier(i, frame)
            writer.write(frame)

        del writer

        split = filename.rsplit(".", 1)
        if audiofile and split[1] == "mkv":
            tmpfilename = "{0}.tmp.{1}".format(split[0], split[1])
            ffmpegcall = ["ffmpeg", "-i", audiofile, "-itsoffset", toOffset(-self.start / self.fps), "-i", filename, "-map", "1:0", "-map", "0:1", "-y", tmpfilename]
            try:
                with open(devnull, "w") as DEVNULL:
                    call(["rm", "-f", tmpfilename], stdout = DEVNULL, stderr = DEVNULL)
                    call(ffmpegcall, stdout = DEVNULL, stderr = DEVNULL)
                    call(["mv", tmpfilename, filename], stdout = DEVNULL, stderr = DEVNULL)
            except OSError:
                pass

    def getSegment(self, start, end):
        """
        Returns a segment.
        Better than creating one yourself if the faces have
        already been found.
        """
        # Start < end is checked in VideoWrapper constructor
        if not within((start, end), (self.start, self.end)):
            raise BoundsError

        wrapper = VideoWrapper(self.video, start, end)

        if self.faces is not None:
            wrapper.faces = [(frameNo, rects)
                             for frameNo, rects in self.faces
                             if  frameNo >= start
                             and frameNo <  end]

        return wrapper

    def getFaces(self, minSize = (30, 30), minNeighbors = 11):
        """
        Returns the faces in a video segment.
        Memoises the result for future use
        """
        cascadefile = "res/haarcascade_frontalface_default.xml"
        cascade     = cv2.CascadeClassifier(cascadefile)

        if self.faces is not None:
            return self.faces

        self.faces = []

        self.video.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, self.start)
        for frameNo in xrange(self.start, self.end):
            _, frame = self.video.read()

            img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            img = cv2.equalizeHist(img)

            rects = cascade.detectMultiScale(img, minNeighbors = minNeighbors,
                                             flags = cv2.cv.CV_HAAR_SCALE_IMAGE,
                                             minSize = minSize)

            if len(rects) > 0:
                self.faces.append((frameNo, rects))

        return self.faces

    def play(self):
        """
        Plays a video frame by frame on key press.
        """
        self.video.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, self.start)
        for _ in xrange(self.start, self.end):
           _, frame = self.video.read()
           cv2.imshow("Video player", frame)
           cv2.waitKey()

    def getFrame(self, frameNo):
        """
        Returns a single frame given a frame number.
        """
        assert(self.start <= frameNo and frameNo < self.end)

        self.video.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, frameNo)
        return self.video.read()[1]

def within((a, b), (c, d)):
    """
    Returns whether (a, b) is within (c, d)
    Assumes that the ranges are valid
    i.e. a <= b and c <= d
    """
    return a >= c and b <= d

def toOffset(secs):
    """
    Converts a number of seconds to an offset into a video
    """
    if secs < 0:
        sign = "-"
        secs = -secs
    else:
        sign = ""

    hh = int(secs // (60 * 60))
    secs -= hh * 60 * 60
    mm = int(secs // 60)
    secs -= mm * 60
    ss = int(secs)
    secs -= ss
    xxx = secs
    assert(hh < 100 and mm < 60 and ss < 60 and xxx < 1000)
    xxx = "{0:.3f}".format(xxx).split(".", 1)[1]
    return "{0}{1}:{2}:{3}.{4}".format(sign, hh, mm, ss, xxx)
