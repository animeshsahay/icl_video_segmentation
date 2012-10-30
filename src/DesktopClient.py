#!/usr/bin/python -d

import sys
from PyQt4.phonon import Phonon
from PyQt4 import QtCore, QtGui
from Gui import Ui_MainWindow
 
class DesktopClient(QtGui.QMainWindow):
  def __init__(self, parent=None):
    QtGui.QWidget.__init__(self, parent)
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)
    videoplayer = VideoPlayer()
    
 
if __name__ == "__main__":
  app = QtGui.QApplication(sys.argv)
  client = DesktopClient()
  client.show()
  sys.exit(app.exec_())
