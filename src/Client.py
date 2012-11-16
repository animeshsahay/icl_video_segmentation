#!/usr/bin/env python
from cv2 import *
import sys
import tempfile
import os
from random import random
from VideoWrapper import VideoWrapper
from PyQt4 import QtCore
from PyQt4 import QtGui
from Segmenter import *

class Client:
    # Initialise the client class.
    # The video can be of type string, cv image or video wrapper.
    def __init__(self, video, splitType, progressBar, label, start = None, end = None):
        self.splitType = splitType
        self.progressBar = progressBar
        self.barState = label
        assert any(splitType == v for (k, v) in SplitType.__dict__.items() if not k.startswith('__')), "Invalid split type"
        if isinstance(video, VideoWrapper):
            self.videoWrapper = video
        elif isinstance(video, type(VideoCapture())):
            self.videoWrapper = VideoWrapper(video, start, end)
        elif isinstance(video, str):
            self.videoWrapper = VideoWrapper(VideoCapture(video), start, end)
        else:
            assert 0, ("Unknown type of video parameter (%s)" % type(video))

    # Run the correct functions based on what the client wants.
    def run(self, highlight, seg):
        # set arguments in Segmenter and start the segmentation        
        seg.run(self.videoWrapper.start, self.videoWrapper.end, self.videoWrapper.fps, self.videoWrapper.video, self.splitType)

        # Changing the progress bar label text
        self.barState.setText("Step 2/2: Writing segments to files...")

        # Writing segments into files:
        segments = seg.segments
        segmentNames = []
        directory = tempfile.mkdtemp()
        
        # set bar to 1% so there's something there while waiting for the first iteration to complete
        self.progressBar.setProperty("value", 1)
        
        # the i is used as a loop counter for the progress bar
        i = 1
        for segment in segments:
            self.progressBar.setProperty("value", (i*100/len(segments)))
            QtGui.QApplication.processEvents()
            i += 1
            rnd = str(random())
            segmentNames.append(("%s/out_%s.avi" % (directory, rnd), segment.start, segment.end))

            # If we want faces visible, show them
            if highlight:
                faces = segment.getFaces()
                segment.write("%s/out_%s.avi" % (directory, rnd),
                    frameModifier = lambda frameNo, frame:
                        integrateFace(frameNo, frame, faces))
            else:
                segment.write("%s/out_%s.avi" % (directory, rnd))

        # update progress bar label and return
        self.barState.setText("Segmentation completed")
        return segmentNames

def integrateFace(frameNo, frame, faces):
  """Integrates faces into the frame if applicable"""
  for (f, rects) in faces:
    if f == frameNo:
      for (x, y, width, height) in rects:
        rectangle(frame, (x, y), (x + width, y + height), (255, 0, 0), 2)
  return frame

# If we call this file directly, convert the video and show it onscreen.
if __name__ == "__main__":
    # If we haven't got enough arguments, display usage instructions.
    if len(sys.argv) < 3:
        print("USAGE: %s FILENAME SPLIT_TYPE" % sys.argv[0])
        sys.exit()

    # Convert the video
    segments = Client(sys.argv[1], int(sys.argv[2])).run()

    # Show it onscreen
    for i, _ in enumerate(segments):
        namedWindow("Video renderer %d" % (i +1))

    # Loop till ESC pressed
    while((waitKey(33) & 0xFF) != 27):
        for (i, segment) in enumerate(segments):
            _, img = segment.video.read()
            imshow("Video renderer %d" % (i + 1), img)

    destroyAllWindows()

