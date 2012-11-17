from cv2 import *
from VideoWrapper import *
from PyQt4.QtGui import QApplication

class Segmenter:
    def __init__(self, bar, label):
        self.segments = []
        self.progressBar = bar
        self.barState = label

    def run(self, start, end, fps, video, splitType):
        """
        Only call after setArgs()! Depends on the arguments provided by Client before it can perform segmentation
        Loops over the frames and splits them into segments, depending on the provided split type
        """

        # Set progress bar label
        self.barState.setText("Step 1/2: Finding segments...")

        frameNo = start
        currStart = start
        video.set(cv.CV_CAP_PROP_POS_FRAMES, start)

        # Grabs until frameNo=end or until actual end of the video is reached
        while video.grab() and frameNo <= end:
            #update progress bar
            self.progressBar.setProperty("value", (frameNo*100/end))
            QApplication.processEvents()
            
            (_, frame) = video.retrieve()
            
            # Convert to black and white
            frame = binarise(frame)

            # Splitting on black frames
            if splitType == SplitType.ON_BLACK_FRAMES and checkBlackFrame(frame):
                if frameNo-currStart > 0:
                   self.segments.append(VideoWrapper(video, currStart, frameNo))
                currStart = frameNo + 1

            # Splitting every second
            elif splitType == SplitType.EVERY_SECOND:
                if ((frameNo - start) % int(fps) == 0 and frameNo > start) or frameNo == end:
                    self.segments.append(VideoWrapper(video, currStart, frameNo))
                    currStart = frameNo + 1
            
            # Splitting every other second
            elif splitType == SplitType.EVERY_TWO_SECONDS:
                if ((frameNo - start) % int(2 * fps) == 0 and frameNo > start) or frameNo == end:
                    self.segments.append(VideoWrapper(video, currStart, frameNo))
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
