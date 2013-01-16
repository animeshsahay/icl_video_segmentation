import cv2
from FaceClustering import clusterFaces, convertFaces

class Segmenter:
    def __init__(self):
        self.segments = []

    def run(self, options):
        """
        Loops over frames and splits them into segments. Split
        differently depending on the options passed in
        """

        options      = mergeDefaults(options)
        splitType    = options['splitType']
        videoWrapper = options['videoWrapper']

        start = videoWrapper.start
        end   = videoWrapper.end
        fps   = videoWrapper.fps

        frameNo   = start
        currStart = start

        if splitType == SplitType.ON_FACE_CLUSTERS:
            options['steps'] += 2
        else:
            options['steps'] += 1

        options['currStep'] += 1

        if splitType == SplitType.EVERY_SECOND:
            options['xSeconds'] = 1
            splitType = SplitType.EVERY_X_SECONDS
        elif splitType == SplitType.EVERY_TWO_SECONDS:
            options['xSeconds'] = 2
            splitType = SplitType.EVERY_X_SECONDS

        if splitType == SplitType.ON_FACE_CLUSTERS:
            options["stateCallback"]("Step %d / %d: Preparing for face clustering. (This may take a while)" % (options["currStep"], options["steps"]))
            options["currStep"] += 1
            lastClusterFound  = currStart
            frameCheckLength  = options["segmentLength"]
            currFrameClusters = {}
            newFrameClusters  = {}
            clusters          = {}
            faces             = videoWrapper.getFaces()

            options["clusters"] = clusterFaces(convertFaces(videoWrapper), options)
            for i, l in enumerate(options["clusters"]):
                for frame, face in l:
                    if frame not in clusters:
                        clusters[frame] = []
                    clusters[frame].append(i)

        options['stateCallback']("Step %d / %d: Finding segments..." % (options["currStep"], options["steps"]))
        options["currStep"] += 1

        # Grabs until frameNo=end or until actual end of the video is reached
        for frameNo in xrange(start, end):
            #update progress bar
            options['progressCallback']((frameNo - start) * 100 / (end - start))
            
            frame = videoWrapper.getFrame(frameNo)

            # Splitting on black frames
            if splitType == SplitType.ON_BLACK_FRAMES:
                # Convert to black and white
                frame = binarise(frame)
                if checkBlackFrame(frame):
                    if frameNo - currStart > 0:
                        self.segments.append(videoWrapper.getSegment(currStart, frameNo))
                    currStart = frameNo + 1

            # Splitting every x seconds
            elif splitType == SplitType.EVERY_X_SECONDS:
                if ((frameNo - start) % int(options["xSeconds"] * fps) == 0 and frameNo > start) or frameNo == end:
                    self.segments.append(videoWrapper.getSegment(currStart, frameNo + 1))
                    currStart = frameNo + 1

            # Splitting on face clusters
            elif splitType == SplitType.ON_FACE_CLUSTERS:
                if frameNo == end - 1:
                    if options["verbose"] >= 1:
                        print("Segment between %d - %d" % (currStart, frameNo))
                    self.segments.append(videoWrapper.getSegment(currStart, frameNo))
                elif lastClusterFound + frameCheckLength <= frameNo:
                    if options["verbose"] >= 1:
                        print("Segment between %d - %d" % (currStart, lastClusterFound + 1))
                    self.segments.append(videoWrapper.getSegment(currStart, lastClusterFound + 1))

                if lastClusterFound + frameCheckLength <= frameNo:
                    currFrameClusters = newFrameClusters
                    newFrameClusters = {}
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

                if all([v == 0 for v in currFrameClusters.values()]):
                    lastClusterFound = frameNo

                if lastClusterFound == frameNo:
                    for cluster, count in newFrameClusters.items():
                        if cluster not in currFrameClusters:
                            currFrameClusters[cluster] = 0
                        currFrameClusters[cluster] += count
                    newFrameClusters = {}

                #print "-------------------------"
                #print frameNo
                #print currFrameClusters
                #print newFrameClusters
                #print "-------------------------"

            # Unknown splitting type
            else:
                raise Exception("Unknown/unimplemented splitting type")

            frameNo += 1

        # No split possible - return self
        if self.segments == []:
           self.segments = [videoWrapper]

def binarise(frame):
    """
    Binarise a grayscale frame. Threshold of 10 to maximise number of white
    pixels, thereby speeding up non black frame detection in checkBlackFrame.
    """
    frame    = cv2.cvtColor(frame, cv2.cv.CV_RGB2GRAY)
    _, frame = cv2.threshold(frame, 10, 255, cv2.THRESH_BINARY)
    return frame

def checkBlackFrame(frame):
    """ Checks if frame is entirely black. """
    for col in frame:
        for pixel in col:
            if pixel != 0:
                return False

    return True

def mergeDefaults(options):
    """
    Merges the default values into the options dictionary
    """
    defaults = {"stateCallback"    : lambda x: None,
                "progressCallback" : lambda x: None,
                "currStep"         : 0,
                "segmentLength"    : 20,
                "verbose"          : 1}

    for k, v in defaults.items():
        if k not in options:
            options[k] = v

    return options

class SplitType:
    """ What to segment on. """
    ON_BLACK_FRAMES   = 0
    EVERY_SECOND      = 1
    EVERY_TWO_SECONDS = 2
    ON_FACE_CLUSTERS  = 3
    EVERY_X_SECONDS   = 4
