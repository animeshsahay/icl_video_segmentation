#!/usr/bin/python -d

import sys
from PyQt4 import phonon
from PyQt4 import QtCore, QtGui
from Gui import Ui_MainWindow
 
class DesktopClient(QtGui.QMainWindow):
  def __init__(self, parent=None):
    QtGui.QWidget.__init__(self, parent)
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)
    

    QtCore.QObject.connect(self.ui.loadButton, QtCore.SIGNAL("clicked()"), self.load)
    QtCore.QObject.connect(self.ui.browseButton, QtCore.SIGNAL("clicked()"), self.browse)
    
  def browse(self):
    file = str(QtGui.QFileDialog.getOpenFileName(self, "Open Video"))
    self.ui.filePath.setText(file)
 
  def load(self):
    media = phonon.Phonon.MediaSource(self.ui.filePath.text())
    self.ui.videoPlayer.load(media)
    self.ui.videoPlayer.play()
 
if __name__ == "__main__":
  app = QtGui.QApplication(sys.argv)
  client = DesktopClient()
  client.show()
  sys.exit(app.exec_())
