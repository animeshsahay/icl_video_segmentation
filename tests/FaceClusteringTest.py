mport unittest
import sys
from VideoWrapper import *

# Note : Skyfall trailer has 3672 frames.
class VideoWrapperTest(unittest.TestCase):
        def setUp(self):
            self.skyfall = VideoCapture("res/skyfall.mp4")
            self.instance = VideoWrapper(self.skyfall, 30, 230)
            self.empty = VideoWrapper(self.skyfall, 3, 3)

            #Video instances for face detection tests.
            self.blackFrame = VideoWrapper(self.skyfall, 184, 186)
            self.videoWithoutFace = VideoWrapper(self.skyfall, 300, 330)
            self.videoWithOneFace = VideoWrapper(self.skyfall, 197, 200)
            self.videoWithTwoFaces = VideoWrapper(self.skyfall, 272, 273)
            self.womanInTheCar = VideoWrapper(self.skyfall, 338, 351)

            def test_faultsOnStartBiggerThanEnd(self):
            try:
                VideoWrapper(self.skyfall, 10, 5)
                self.fail("Didn't raise AssertionError on start > end")
            except AssertionError, _:                                                                                                       
                pass
