#!/usr/bin/env python

import cv2
import numpy as np

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
              frameModifier = lambda frameNo, frame: frame):
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

    def getFaces(self):
        """
        Returns the faces in a video segment.
        Memoises the result for future use
        """
        cascadefile = "res/haarcascade_frontalface_default.xml"
        cascade     = cv2.CascadeClassifier(cascadefile)

        if self.faces is not None:
            return self.faces

        self.faces = []
        #self.faces = [(0, np.array([[258, 137,  97,  97]], dtype=np.int32)), (1, np.array([[258, 138,  98,  98]], dtype=np.int32)), (2, np.array([[257, 138,  98,  98]], dtype=np.int32)), (3, np.array([[259, 140,  95,  95]], dtype=np.int32)), (4, np.array([[258, 138,  98,  98]], dtype=np.int32)), (5, np.array([[258, 138,  98,  98]], dtype=np.int32)), (6, np.array([[257, 137, 100, 100]], dtype=np.int32)), (7, np.array([[256, 137,  99,  99]], dtype=np.int32)), (8, np.array([[257, 138,  99,  99]], dtype=np.int32)), (9, np.array([[257, 139,  98,  98]], dtype=np.int32)), (10, np.array([[257, 138, 100, 100]], dtype=np.int32)), (11, np.array([[256, 138,  99,  99]], dtype=np.int32)), (12, np.array([[255, 137, 100, 100]], dtype=np.int32)), (13, np.array([[255, 136, 102, 102]], dtype=np.int32)), (14, np.array([[255, 137, 101, 101]], dtype=np.int32)), (15, np.array([[254, 135, 102, 102]], dtype=np.int32)), (16, np.array([[256, 138,  97,  97]], dtype=np.int32)), (17, np.array([[256, 139,  96,  96]], dtype=np.int32)), (18, np.array([[256, 138,  98,  98]], dtype=np.int32)), (19, np.array([[255, 137,  99,  99]], dtype=np.int32)), (20, np.array([[255, 137,  98,  98]], dtype=np.int32)), (21, np.array([[256, 137,  95,  95]], dtype=np.int32)), (22, np.array([[258, 137,  95,  95]], dtype=np.int32)), (23, np.array([[258, 136,  96,  96]], dtype=np.int32)), (24, np.array([[258, 137,  96,  96]], dtype=np.int32)), (25, np.array([[259, 136,  95,  95]], dtype=np.int32)), (26, np.array([[260, 137,  94,  94]], dtype=np.int32)), (27, np.array([[259, 136,  97,  97]], dtype=np.int32)), (28, np.array([[260, 137,  95,  95]], dtype=np.int32)), (29, np.array([[260, 137,  94,  94]], dtype=np.int32)), (30, np.array([[260, 137,  94,  94]], dtype=np.int32)), (31, np.array([[259, 137,  97,  97]], dtype=np.int32)), (32, np.array([[260, 138,  97,  97]], dtype=np.int32)), (33, np.array([[259, 137,  98,  98]], dtype=np.int32)), (34, np.array([[259, 137,  98,  98]], dtype=np.int32)), (35, np.array([[260, 138,  95,  95]], dtype=np.int32)), (36, np.array([[261, 140,  94,  94]], dtype=np.int32)), (37, np.array([[259, 138,  96,  96]], dtype=np.int32)), (38, np.array([[260, 138,  94,  94]], dtype=np.int32)), (39, np.array([[260, 138,  94,  94]], dtype=np.int32)), (40, np.array([[258, 136,  97,  97]], dtype=np.int32)), (41, np.array([[258, 137,  94,  94]], dtype=np.int32)), (42, np.array([[255, 135,  96,  96]], dtype=np.int32)), (43, np.array([[252, 133, 100, 100]], dtype=np.int32)), (44, np.array([[251, 133,  97,  97]], dtype=np.int32)), (45, np.array([[251, 133,  98,  98]], dtype=np.int32)), (46, np.array([[251, 134,  95,  95]], dtype=np.int32)), (47, np.array([[249, 134,  96,  96]], dtype=np.int32)), (48, np.array([[248, 134,  94,  94]], dtype=np.int32)), (49, np.array([[312, 128,  68,  68]], dtype=np.int32)), (50, np.array([[312, 128,  68,  68]], dtype=np.int32)), (51, np.array([[313, 129,  67,  67]], dtype=np.int32)), (52, np.array([[311, 129,  68,  68]], dtype=np.int32)), (53, np.array([[312, 130,  66,  66]], dtype=np.int32)), (54, np.array([[312, 131,  68,  68]], dtype=np.int32)), (55, np.array([[313, 132,  65,  65]], dtype=np.int32)), (56, np.array([[315, 133,  63,  63]], dtype=np.int32)), (57, np.array([[315, 133,  62,  62]], dtype=np.int32)), (58, np.array([[316, 132,  63,  63]], dtype=np.int32)), (59, np.array([[314, 131,  64,  64]], dtype=np.int32)), (60, np.array([[310, 130,  70,  70]], dtype=np.int32)), (61, np.array([[310, 131,  69,  69]], dtype=np.int32)), (62, np.array([[310, 132,  70,  70]], dtype=np.int32)), (63, np.array([[310, 132,  70,  70]], dtype=np.int32)), (64, np.array([[310, 131,  70,  70]], dtype=np.int32)), (65, np.array([[311, 131,  69,  69]], dtype=np.int32)), (66, np.array([[312, 129,  69,  69]], dtype=np.int32)), (67, np.array([[311, 129,  69,  69]], dtype=np.int32)), (68, np.array([[312, 131,  67,  67]], dtype=np.int32)), (69, np.array([[313, 131,  66,  66]], dtype=np.int32)), (70, np.array([[312, 131,  68,  68]], dtype=np.int32)), (71, np.array([[311, 131,  68,  68]], dtype=np.int32)), (72, np.array([[311, 130,  69,  69]], dtype=np.int32)), (73, np.array([[310, 129,  71,  71]], dtype=np.int32)), (74, np.array([[311, 129,  69,  69]], dtype=np.int32)), (75, np.array([[311, 129,  69,  69]], dtype=np.int32)), (76, np.array([[258, 142,  94,  94]], dtype=np.int32)), (77, np.array([[257, 141,  94,  94]], dtype=np.int32)), (78, np.array([[257, 141,  94,  94]], dtype=np.int32)), (79, np.array([[257, 141,  95,  95]], dtype=np.int32)), (80, np.array([[258, 141,  94,  94]], dtype=np.int32)), (81, np.array([[256, 141,  96,  96]], dtype=np.int32)), (82, np.array([[257, 140,  97,  97]], dtype=np.int32)), (83, np.array([[256, 139,  99,  99]], dtype=np.int32)), (84, np.array([[257, 138, 100, 100]], dtype=np.int32)), (85, np.array([[256, 140,  95,  95]], dtype=np.int32)), (86, np.array([[256, 139,  95,  95]], dtype=np.int32)), (87, np.array([[256, 139,  94,  94]], dtype=np.int32)), (88, np.array([[255, 137,  95,  95]], dtype=np.int32)), (89, np.array([[255, 137,  95,  95]], dtype=np.int32)), (90, np.array([[255, 138,  95,  95]], dtype=np.int32)), (91, np.array([[255, 138,  95,  95]], dtype=np.int32)), (92, np.array([[255, 140,  93,  93]], dtype=np.int32)), (93, np.array([[253, 139,  97,  97]], dtype=np.int32)), (94, np.array([[254, 139,  98,  98]], dtype=np.int32)), (95, np.array([[254, 139,  99,  99]], dtype=np.int32)), (96, np.array([[254, 139,  98,  98]], dtype=np.int32)), (97, np.array([[255, 141,  96,  96]], dtype=np.int32)), (98, np.array([[256, 142,  94,  94]], dtype=np.int32)), (99, np.array([[256, 143,  93,  93]], dtype=np.int32))]
        #return self.faces

        self.video.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, self.start)
        for frameNo in xrange(self.start, self.end):
            _, frame = self.video.read()

            img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            img = cv2.equalizeHist(img)

            rects = cascade.detectMultiScale(img, minNeighbors = 11,
                                             flags = cv2.cv.CV_HAAR_SCALE_IMAGE,
                                             minSize = (30, 30))

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
    return a >= c and a < d and b <= d
