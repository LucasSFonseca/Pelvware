import sys
from PyQt4 import QtGui, QtCore
import numpy as np
from ftplib import FTP

import pyqtgraph as pg


class ApplicationWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("Pelvware")

        # Connecting to the FTPServer
        self.ftp = FTP('10.7.227.206', 'admin', 'admin')
        self.ftp.retrlines('RETR teste', self.writeFile)

        # self.fileName = ''
        self.dataFile = open('teste.log', 'r')

        # Data to be plotted
        self.x = []
        self.y = []
        self.separateData(self.dataFile)

        # Creation of the menu File
        self.file_menu = QtGui.QMenu('&File', self)
        self.file_menu.addAction('&Open', self.selectFile)
        self.file_menu.addAction('&Save')
        self.file_menu.addAction('&Close', self.fileQuit)

        self.menuBar().addMenu(self.file_menu)

        # Creation of the main Widget and of the organizational layouts.
        centralWidget = QtGui.QWidget()
        self.setCentralWidget(centralWidget)

        hBoxLayout1 = QtGui.QHBoxLayout()
        vBoxLayout = QtGui.QVBoxLayout()
        hBoxLayout2 = QtGui.QHBoxLayout()

        hBoxLayout1.addLayout(vBoxLayout)
        hBoxLayout1.addLayout(hBoxLayout2)
        centralWidget.setLayout(hBoxLayout1)
        self.setGeometry(300, 300, 1200, 900)

        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'r')
        # pg.setConfigOption('leftButtonPan', False)

        btn = QtGui.QPushButton('Teste')
        btn2 = QtGui.QPushButton('Teste')

        p1 = pg.PlotWidget()

        vBoxLayout.addWidget(btn)
        vBoxLayout.addWidget(btn2)
        vBoxLayout.addStretch(1)
        hBoxLayout2.addWidget(p1)

        p1.setXRange(0, 400, padding=0)
        p1.showGrid(x=True, y=True)
        p1.plot(x=self.x, y=self.y, pen='r')

        # dataVisualizer = DataVisualizer()
        # hBoxLayout2.addWidget(dataVisualizer)

        # timer = pg.QtCore.QTimer()
        # timer.timeout.connect(dataVisualizer.updateData)
        # timer.start(50)

    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()

    def separateData(self, file):
        for line in file:
            a, b = line.split(';')
            self.x.append(a)
            self.y.append(b)

        self.x = list(map(int, self.x))
        self.y = list(map(float, self.y))

    # ----- Needing correction of file selection ----- #
    def selectFile(self):
        self.fileDialog = QtGui.QFileDialog(self)
        self.fileDialog.show()
        self.fileName = self.fileDialog.getOpenFileName(self, ("Open File"))

    def writeFile(self, text):
        file = open('teste.log', 'a')
        file.write(text)
        file.write('\n')


qApp = QtGui.QApplication(sys.argv)

applicationWindow = ApplicationWindow()
applicationWindow.show()
sys.exit(qApp.exec_())
