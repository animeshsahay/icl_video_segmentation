# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created: Tue Oct 30 20:40:47 2012
#      by: PyQt4 UI code generator 4.9.4
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
        MainWindow.resize(968, 468)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.filePath = QtGui.QLineEdit(self.centralwidget)
        self.filePath.setGeometry(QtCore.QRect(20, 10, 721, 27))
        self.filePath.setObjectName(_fromUtf8("filePath"))
        self.browseButton = QtGui.QPushButton(self.centralwidget)
        self.browseButton.setGeometry(QtCore.QRect(760, 10, 98, 27))
        self.browseButton.setObjectName(_fromUtf8("browseButton"))
        self.loadButton = QtGui.QPushButton(self.centralwidget)
        self.loadButton.setGeometry(QtCore.QRect(860, 10, 98, 27))
        self.loadButton.setObjectName(_fromUtf8("loadButton"))
