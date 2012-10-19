#!/usr/bin/env python
import cv2
import sys
from VideoWrapper import VideoWrapper, SplitType

class Client:
  # Initialise the client class.
  # The video can be of type string, cv image or video wrapper.
  def __init__(self, video, splitType, start = None, end = None):
    self.splitType = splitType
    if isinstance(video, VideoWrapper):
      self.video = video
    elif isinstance(video, type(cv2.VideoCapture())):
      self.video = VideoWrapper(video, start = start, end = end)
    elif isinstance(video, str):
      self.video = VideoWrapper(cv2.VideoCapture(video), start = start, end = end)
    else:
      assert 0, ("Unknown type of video parameter (%s)" % type(video))

  # Run the correct functions based on what the client wants.
  def run(self):
    return self.video.getSegments(self.splitType)

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
    cv2.namedWindow("Video renderer %d" % (i +1))

  # Loop till ESC pressed
  while((cv2.waitKey(33) & 0xFF) != 27):
    for (i, segment) in enumerate(segments):
      _, img = segment.video.read()
      cv2.imshow("Video renderer %d" % (i + 1), img)

  cv2.destroyAllWindows()
