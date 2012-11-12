#!/usr/bin/python -d
import sys
from PyQt4 import phonon
from PyQt4 import QtCore, QtGui
from Gui import Ui_MainWindow
from VideoWrapper import *
from Client import *
from SegmentRegister import *
from VideoInfo import *
import time
from multiprocessing import Process, Queue
from Segmenter import *

class DesktopClient(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.segments = SegmentRegister([])
        self.basicInfo = None

        QtCore.QObject.connect(self.ui.segmentButton, QtCore.SIGNAL("clicked()"), self.segment)
        QtCore.QObject.connect(self.ui.browseButton, QtCore.SIGNAL("clicked()"), self.browse)
        QtCore.QObject.connect(self.ui.playButton, QtCore.SIGNAL("clicked()"), self.ui.videoPlayer.play)
        QtCore.QObject.connect(self.ui.pauseButton, QtCore.SIGNAL("clicked()"), self.ui.videoPlayer.pause)
        QtCore.QObject.connect(self.ui.nextButton, QtCore.SIGNAL("clicked()"), self.next)
        QtCore.QObject.connect(self.ui.previousButton, QtCore.SIGNAL("clicked()"), self.previous)
        QtCore.QObject.connect(self.ui.filePath, QtCore.SIGNAL("returnPressed()"), self.preload)
        QtCore.QObject.connect(self.ui.lastFrameButton, QtCore.SIGNAL("clicked()"), self.setLastFrame)

    def setLastFrame(self):
        """ Set the end frame to be the last frame of the video. """
        self.ui.endFrame.setText(str(self.basicInfo.numberOfFrames()))

    def browse(self):
        """ Opens a system "browse" dialog box and preloads the video file. """
        file = str(QtGui.QFileDialog.getOpenFileName(self, "Open Video"))
        self.ui.filePath.setText(file)

        self.preload()

    def errorBox(self, name):
        """ Customized error box. """
        birthday, error = "007", "Wrong video file: please load Skyfall trailer."
        if name == "Jasper":
            birthday, error = "1311", "Please enter a valid path."
        elif name == "Ben":
            birthday, error = "2211", "Start and end frames out of bounds."
        elif name == "Roxana":
            birthday, error = "2405b", ""
        elif name == "Agnieszka":
            birthday, error = "2405a", ""
        elif name == "Charlie":
            birthday, error = "2709", ""

        QtGui.QMessageBox.critical(self, "Error " + birthday, error)

    def preload(self):
        """
        Creates a VideoInfo object to fill in basic info about video file.
        Does not cause any segmenting or bounds checking to occur.
        """
        try:
            self.basicInfo = VideoInfo(str(self.ui.filePath.text()))
        except:
            self.errorBox("Jasper")
            return

        self.ui.startFrame.setText("0")
        self.ui.endFrame.setText("")
        self.ui.videoTitleLabel.setText("Title: " + self.basicInfo.prettyTitle())
        self.ui.videoLengthLabel.setText("Video length: " + self.basicInfo.prettyLength())
        self.ui.lastFrameButton.setEnabled(True)

    def load(self, segment):
        """ 
        Loads but does not play a video file.
        Makes sure the first frame is shown by calling "pause()".
        """
        media = phonon.Phonon.MediaSource(segment)
        self.ui.videoPlayer.load(media)
        self.ui.videoPlayer.pause()

    def next(self):
        """ Grabs next segment, loads it, and updates GUI accordingly. """
        self.load(self.segments.next())
        self.updateSegLabel()
        self.updatePreviousNextButton()

    def previous(self):
        """ Grabs previous segment, loads it, and updates GUI accordingly. """
        self.load(self.segments.previous())
        self.updateSegLabel()
        self.updatePreviousNextButton()

    def updateSegLabel(self):
        self.ui.currSeg.setText("Current segment: " + str(self.segments.index+1) + "/" + str(self.segments.length()))

    def updatePreviousNextButton(self):
        """
        Enable or disable the "previous" and "next" buttons depending on the 
        index of the current segment.
        """
        self.ui.previousButton.setDisabled(self.segments.first())
        self.ui.nextButton.setDisabled(self.segments.last())

    def setControls(self, enabled):
        """ Global GUI button toggle. """
        self.ui.pauseButton.setEnabled(enabled)
        self.ui.playButton.setEnabled(enabled)
        self.ui.nextButton.setEnabled(enabled)
        self.ui.previousButton.setEnabled(enabled)
        self.ui.lastFrameButton.setEnabled(enabled)

        if enabled:
            self.updateSegLabel()
        else:
            self.ui.currSeg.setText("Video not yet segmented.")

    # TODO : Define a split type for when nothing is ticked
    def getSplitType(self):
        """ Radio button options to SplitType map. """
        if self.ui.blackFramesOption.isChecked():
            return SplitType.ON_BLACK_FRAMES
        if self.ui.everySecondOption.isChecked():
            return SplitType.EVERY_SECOND
        if self.ui.everyTwoSecondsOption.isChecked():
            return SplitType.EVERY_TWO_SECONDS

        return None

    def segment(self):
        """
        Calls the Client class to perform segmenting. Handles bound checking
        errors. Fills in segment register and updates GUI (button activation).
        """
        self.setControls(False)
        self.currSegment = 0

        cap = None
        try:
            start = int(self.ui.startFrame.text())
            end = int(self.ui.endFrame.text())
            cap = Client(str(self.ui.filePath.text()), self.getSplitType(), self.ui.segProgress, self.ui.barState, start, end)
        except IOError:
            return self.errorBox("Jasper")
        except (ValueError, BoundsError):
            return self.errorBox("Ben")

        # create Segmenter object to segment the video
        self.seg = Segmenter(self.ui.segProgress, self.ui.barState)
        
        # call Client.run, which in turn calls Segmenter.run to perform the segmentation
        segmentNames = cap.run(self.ui.highlightFacesOption.isChecked(), self.seg) 

        #load segments into the GUI
        self.segments = SegmentRegister(segmentNames)
        self.ui.videoBackground.hide()
        self.setControls(True)
        self.updatePreviousNextButton()
        self.load(self.segments.current()) 

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    client = DesktopClient()
    client.show()
    sys.exit(app.exec_())
