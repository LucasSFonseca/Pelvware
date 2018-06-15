import sys
from PyQt4 import QtGui, QtCore
import numpy as np

# --- Non-static Visualizer lib
import pyqtgraph as pg


# Non-static data Visualizer (!!!!!Not working!!!!!)
class DataVisualizer(pg.PlotWidget):
    data = np.empty(100)
    ptr = 0

    def __init__(self):

        pg.PlotWidget.__init__(self)

        self.setDownsampling(mode='peak')
        self.setClipToView(True)

        curve = self.plot()

    def updateData(self):

        if ptr >= data.shape[0]:
            tmp = data
            data = np.empty(data.shape[0] * 2)
            data[:tmp.shape[0]] = tmp

        curve.setData(data[:ptr])
        curve.setPos(-ptr, 0)


class ApplicationWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("Pelvware")

        # Creation of the menu File
        self.file_menu = QtGui.QMenu('&File', self)
        self.file_menu.addAction('&Open')
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

        btn = QtGui.QPushButton('Teste')
        btn2 = QtGui.QPushButton('Teste')
        vBoxLayout.addWidget(btn)
        vBoxLayout.addWidget(btn2)
        vBoxLayout.addStretch(1)

        dataVisualizer = DataVisualizer()
        hBoxLayout2.addWidget(dataVisualizer)

        timer = pg.QtCore.QTimer()
        timer.timeout.connect(dataVisualizer.updateData)
        timer.start(50)

    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()


qApp = QtGui.QApplication(sys.argv)

applicationWindow = ApplicationWindow()
applicationWindow.show()
sys.exit(qApp.exec_())
