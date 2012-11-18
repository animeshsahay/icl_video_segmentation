from cv2 import *
from VideoWrapper import *
from FaceClustering import *

class Segmenter:
    def __init__(self, progressCallback = lambda percent: None, stateCallback = lambda text: None):
        self.segments         = []
        self.progressCallback = progressCallback
        self.stateCallback    = stateCallback

    def run(self, videoWrapper, splitType):
        """
        Only call after setArgs()! Depends on the arguments provided by Client before it can perform segmentation
        Loops over the frames and splits them into segments, depending on the provided split type
        """

        start = videoWrapper.start
        end   = videoWrapper.end
        fps   = videoWrapper.fps
        video = videoWrapper.video

        # Set progress bar label
        self.stateCallback("Step 1/2: Finding segments...")

        frameNo = start
        currStart = start

        if splitType == SplitType.ON_FACE_CLUSTERS:
            lastClusterFound  = currStart
            frameCheckLength  = 10
            currFrameClusters = {}
            newFrameClusters  = {}
            clusters          = {}
            faces             = videoWrapper.getFaces()

            _clusters         = clusterFaces(convertFaces(videoWrapper, faces))
            for i, l in enumerate(_clusters):
                for frame, face in l:
                    if frame not in clusters:
                        clusters[frame] = []
                    clusters[frame].append(i)

        video.set(cv.CV_CAP_PROP_POS_FRAMES, start)

        # Grabs until frameNo=end or until actual end of the video is reached
        while video.grab() and frameNo <= end:
            #update progress bar
            self.progressCallback((frameNo - start) * 100 / end)
            
            (_, frame) = video.retrieve()
            
            # Convert to black and white
            frame = binarise(frame)

            # Splitting on black frames
            if splitType == SplitType.ON_BLACK_FRAMES and checkBlackFrame(frame):
                if frameNo - currStart > 0:
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

            # Splitting on face clusters
            elif splitType == SplitType.ON_FACE_CLUSTERS:
                if frameNo == end:
                    self.segments.append(VideoWrapper(video, currStart, frameNo))
                elif lastClusterFound + frameCheckLength <= frameNo:
                    self.segments.append(VideoWrapper(video, currStart, lastClusterFound))

                if lastClusterFound + frameCheckLength <= frameNo:
                    currFrameClusters = newFrameClusters
                    lastClusterFound, currStart = frameNo, lastClusterFound + 1

                discardFrame = frameNo - frameCheckLength - 1
                if discardFrame in clusters and discardFrame >= currStart:
                    for cluster in clusters[discardFrame]:
                        currFrameClusters[cluster] -= 1

                if frameNo in clusters:
                    for cluster in clusters[frameNo]:
                        if cluster in currFrameClusters:
                            lastClusterFound = frameNo

                        if cluster not in newFrameClusters:
                            newFrameClusters[cluster] = 0
                        newFrameClusters[cluster] += 1

                    if lastClusterFound == frameNo:
                        for cluster, count in newFrameClusters.items():
                            if cluster not in currFrameClusters:
                                currFrameClusters[cluster] = 0
                            currFrameClusters[cluster] += 1

            # Unknown splitting type
            else:
                raise Exception("Unknown/unimplemented splitting type")

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
    ON_FACE_CLUSTERS = 3
