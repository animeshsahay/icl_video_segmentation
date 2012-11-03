# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created: Sat Nov  3 15:11:52 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1292, 556)
        MainWindow.setStyleSheet(_fromUtf8("QGroupBox { \n"
"     border: 1px solid gray; \n"
"     border-radius: 5px; \n"
" } \n"
"\n"
"QGroupBox::title { \n"
"     background-color: transparent;\n"
"     subcontrol-position: top left; /* position at the top left*/ \n"
"     padding:3 8px;\n"
" } "))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.filePath = QtGui.QLineEdit(self.centralwidget)
        self.filePath.setGeometry(QtCore.QRect(20, 10, 851, 27))
        self.filePath.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.filePath.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.filePath.setToolTip(_fromUtf8(""))
        self.filePath.setStatusTip(_fromUtf8(""))
        self.filePath.setWhatsThis(_fromUtf8(""))
        self.filePath.setText(_fromUtf8(""))
        self.filePath.setReadOnly(False)
        self.filePath.setObjectName(_fromUtf8("filePath"))
        self.browseButton = QtGui.QPushButton(self.centralwidget)
        self.browseButton.setGeometry(QtCore.QRect(880, 10, 98, 27))
        self.browseButton.setDefault(False)
        self.browseButton.setObjectName(_fromUtf8("browseButton"))
        self.videoPlayer = phonon.Phonon.VideoPlayer(self.centralwidget)
        self.videoPlayer.setGeometry(QtCore.QRect(20, 40, 961, 471))
        self.videoPlayer.setObjectName(_fromUtf8("videoPlayer"))
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(1000, 10, 281, 331))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox.setFont(font)
        self.groupBox.setFlat(False)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.segmentButton = QtGui.QPushButton(self.groupBox)
        self.segmentButton.setEnabled(True)
        self.segmentButton.setGeometry(QtCore.QRect(10, 270, 98, 27))
        self.segmentButton.setObjectName(_fromUtf8("segmentButton"))
        self.segProgress = QtGui.QProgressBar(self.groupBox)
        self.segProgress.setGeometry(QtCore.QRect(10, 300, 211, 23))
        self.segProgress.setMaximum(100)
        self.segProgress.setProperty("value", 50)
        self.segProgress.setObjectName(_fromUtf8("segProgress"))
        self.blackFramesOption = QtGui.QRadioButton(self.groupBox)
        self.blackFramesOption.setGeometry(QtCore.QRect(20, 50, 141, 22))
        self.blackFramesOption.setObjectName(_fromUtf8("blackFramesOption"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 30, 91, 17))
        self.label.setObjectName(_fromUtf8("label"))
        self.everySecondOption = QtGui.QRadioButton(self.groupBox)
        self.everySecondOption.setGeometry(QtCore.QRect(20, 70, 116, 22))
        self.everySecondOption.setObjectName(_fromUtf8("everySecondOption"))
        self.everyTwoSecondsOption = QtGui.QRadioButton(self.groupBox)
        self.everyTwoSecondsOption.setGeometry(QtCore.QRect(20, 90, 151, 22))
        self.everyTwoSecondsOption.setChecked(True)
        self.everyTwoSecondsOption.setObjectName(_fromUtf8("everyTwoSecondsOption"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(10, 120, 91, 17))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(10, 180, 91, 17))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.startFrame = QtGui.QLineEdit(self.groupBox)
        self.startFrame.setGeometry(QtCore.QRect(10, 140, 113, 27))
        self.startFrame.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.startFrame.setObjectName(_fromUtf8("startFrame"))
        self.endFrame = QtGui.QLineEdit(self.groupBox)
        self.endFrame.setGeometry(QtCore.QRect(10, 200, 113, 27))
        self.endFrame.setText(_fromUtf8(""))
        self.endFrame.setObjectName(_fromUtf8("endFrame"))
        self.highlightFacesOption = QtGui.QCheckBox(self.groupBox)
        self.highlightFacesOption.setGeometry(QtCore.QRect(10, 240, 131, 22))
        self.highlightFacesOption.setObjectName(_fromUtf8("highlightFacesOption"))
        self.lastFrameButton = QtGui.QPushButton(self.groupBox)
        self.lastFrameButton.setEnabled(False)
        self.lastFrameButton.setGeometry(QtCore.QRect(130, 200, 81, 27))
        self.lastFrameButton.setCheckable(False)
        self.lastFrameButton.setObjectName(_fromUtf8("lastFrameButton"))
        self.previousButton = QtGui.QPushButton(self.centralwidget)
        self.previousButton.setEnabled(False)
        self.previousButton.setGeometry(QtCore.QRect(20, 520, 98, 27))
        self.previousButton.setObjectName(_fromUtf8("previousButton"))
        self.nextButton = QtGui.QPushButton(self.centralwidget)
        self.nextButton.setEnabled(False)
        self.nextButton.setGeometry(QtCore.QRect(880, 520, 98, 27))
        self.nextButton.setObjectName(_fromUtf8("nextButton"))
        self.playButton = QtGui.QPushButton(self.centralwidget)
        self.playButton.setEnabled(False)
        self.playButton.setGeometry(QtCore.QRect(400, 520, 98, 27))
        self.playButton.setObjectName(_fromUtf8("playButton"))
        self.pauseButton = QtGui.QPushButton(self.centralwidget)
        self.pauseButton.setEnabled(False)
        self.pauseButton.setGeometry(QtCore.QRect(500, 520, 98, 27))
        self.pauseButton.setObjectName(_fromUtf8("pauseButton"))
        self.videoBackground = QtGui.QGroupBox(self.centralwidget)
        self.videoBackground.setGeometry(QtCore.QRect(20, 40, 961, 471))
        self.videoBackground.setAutoFillBackground(False)
        self.videoBackground.setStyleSheet(_fromUtf8("QGroupBox#videoBackground { \n"
"     background: black;\n"
" } "))
        self.videoBackground.setTitle(_fromUtf8(""))
        self.videoBackground.setObjectName(_fromUtf8("videoBackground"))
        self.groupBox_2 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(1000, 360, 281, 181))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.videoLengthLabel = QtGui.QLabel(self.groupBox_2)
        self.videoLengthLabel.setGeometry(QtCore.QRect(10, 50, 261, 17))
        self.videoLengthLabel.setObjectName(_fromUtf8("videoLengthLabel"))
        self.videoTitleLabel = QtGui.QLabel(self.groupBox_2)
        self.videoTitleLabel.setEnabled(True)
        self.videoTitleLabel.setGeometry(QtCore.QRect(10, 30, 261, 17))
        self.videoTitleLabel.setObjectName(_fromUtf8("videoTitleLabel"))
        self.currSeg = QtGui.QLabel(self.groupBox_2)
        self.currSeg.setGeometry(QtCore.QRect(10, 70, 261, 17))
        self.currSeg.setObjectName(_fromUtf8("currSeg"))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Skyfall Splitter", None, QtGui.QApplication.UnicodeUTF8))
        self.filePath.setPlaceholderText(QtGui.QApplication.translate("MainWindow", "Please load a video file.", None, QtGui.QApplication.UnicodeUTF8))
        self.browseButton.setText(QtGui.QApplication.translate("MainWindow", "Browse", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("MainWindow", "Options", None, QtGui.QApplication.UnicodeUTF8))
        self.segmentButton.setText(QtGui.QApplication.translate("MainWindow", "Segment", None, QtGui.QApplication.UnicodeUTF8))
        self.blackFramesOption.setText(QtGui.QApplication.translate("MainWindow", "On black frames", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Split type", None, QtGui.QApplication.UnicodeUTF8))
        self.everySecondOption.setText(QtGui.QApplication.translate("MainWindow", "Every second", None, QtGui.QApplication.UnicodeUTF8))
        self.everyTwoSecondsOption.setText(QtGui.QApplication.translate("MainWindow", "Every two seconds", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Start frame : ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "End frame : ", None, QtGui.QApplication.UnicodeUTF8))
        self.startFrame.setText(QtGui.QApplication.translate("MainWindow", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.highlightFacesOption.setText(QtGui.QApplication.translate("MainWindow", "Highlight faces", None, QtGui.QApplication.UnicodeUTF8))
        self.lastFrameButton.setText(QtGui.QApplication.translate("MainWindow", "Last frame", None, QtGui.QApplication.UnicodeUTF8))
        self.previousButton.setText(QtGui.QApplication.translate("MainWindow", "Previous", None, QtGui.QApplication.UnicodeUTF8))
        self.nextButton.setText(QtGui.QApplication.translate("MainWindow", "Next", None, QtGui.QApplication.UnicodeUTF8))
        self.playButton.setText(QtGui.QApplication.translate("MainWindow", "Play", None, QtGui.QApplication.UnicodeUTF8))
        self.pauseButton.setText(QtGui.QApplication.translate("MainWindow", "Pause", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("MainWindow", "Info", None, QtGui.QApplication.UnicodeUTF8))
        self.videoLengthLabel.setText(QtGui.QApplication.translate("MainWindow", "Video length: ", None, QtGui.QApplication.UnicodeUTF8))
        self.videoTitleLabel.setText(QtGui.QApplication.translate("MainWindow", "Title:", None, QtGui.QApplication.UnicodeUTF8))
        self.currSeg.setText(QtGui.QApplication.translate("MainWindow", "Video not yet segmented.", None, QtGui.QApplication.UnicodeUTF8))

from PyQt4 import phonon
