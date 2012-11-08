from cv2 import *
from VideoWrapper import *

class Segmenter:
    def __init__(self, bar, label):
        self.segments = []
        self.progressBar = bar
        self.barState = label
        self.argsSet = False

    def setArgs(self, s, e, f, vid, sType):
        """
        Loads additional arguments needed for the segmentation, therefore **MUST** be called before run()
        Called from Client, since they are not available in the DesktopClient where the object is created.
        """
        self.start_ = s
        self.end = e
        self.fps = f
        self.video = vid
        self.splitType = sType
        self.argsSet = True

    def run(self):
        """
        Only call after setArgs()! Depends on the arguments provided by Client before it can perform segmentation
        Loops over the frames and splits them into segments, depending on the provided split type
        """
        assert(self.argsSet)

        # Set progress bar label
        self.barState.setText("Step 1/2: Finding segments...")

        frameNo = self.start_
        currStart = self.start_
        self.video.set(cv.CV_CAP_PROP_POS_FRAMES, self.start_)

        # Grabs until frameNo=self.end or until actual end of the video is reached
        while self.video.grab() and frameNo <= self.end:
            #update progress bar
            self.progressBar.setProperty("value", (frameNo*100/self.end))
            
            (_, frame) = self.video.retrieve()
            
            # Convert to black and white
            frame = binarise(frame)

            # Splitting on black frames
            if self.splitType == SplitType.ON_BLACK_FRAMES and checkBlackFrame(frame):
                if frameNo-currStart > 0:
                   self.segments.append(VideoWrapper(self.video, currStart, frameNo))
                currStart = frameNo + 1

            # Splitting every second
            elif self.splitType == SplitType.EVERY_SECOND:
                if ((frameNo - start) % int(self.fps) == 0 and frameNo > self.start_) or frameNo == self.end:
                    self.segments.append(VideoWrapper(self.video, currStart, frameNo))
                    currStart = frameNo + 1
            
            # Splitting every other second
            elif self.splitType == SplitType.EVERY_TWO_SECONDS:
                if ((frameNo - self.start_) % int(2 * self.fps) == 0 and frameNo > self.start_) or frameNo == self.end:
                    self.segments.append(VideoWrapper(self.video, currStart, frameNo))
                    currStart = frameNo + 1

            frameNo += 1

        # No split possible - return self
        if self.segments == []:
           self.segments = [self]

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

class SplitType:
    """ What to segment on. """
    ON_BLACK_FRAMES = 0
    EVERY_SECOND = 1
    EVERY_TWO_SECONDS = 2
    # on faces...