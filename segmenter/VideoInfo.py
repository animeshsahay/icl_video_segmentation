import cv2
import enzyme

class VideoInfo:
    def __init__(self, filePath):
        self.info = enzyme.parse(filePath)
        self.video = cv2.VideoCapture(filePath)

    def numberOfFrames(self):
        return int(self.video.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))

    def length(self):
        return int(self.numberOfFrames() / self.video.get(cv2.cv.CV_CAP_PROP_FPS))

    # Pretty print methods - nice formatting of video information.
    def prettyTitle(self):
        if self.info.title == None:
            return "Unknown"

        return self.video.title
    
    def prettyLength(self):
        return str(self.length()) + " seconds (" + str(self.numberOfFrames()) + " frames)"
