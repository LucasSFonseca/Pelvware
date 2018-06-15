import sys
from PyQt4 import QtGui, QtCore
import matplotlib.pyplot as plt
import numpy as np

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure


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

        btn = QtGui.QPushButton('Teste')
        btn2 = QtGui.QPushButton('Teste')

        self.figure = plt.figure(figsize=(12, 15))
        self.canvas = FigureCanvas(self.figure)

        vBoxLayout.addWidget(btn)
        vBoxLayout.addWidget(btn2)
        vBoxLayout.addStretch(1)
        hBoxLayout2.addWidget(self.canvas)

        self.plotGraph()

        # dataVisualizer = DataVisualizer()
        # hBoxLayout2.addWidget(dataVisualizer)

        # timer = pg.QtCore.QTimer()
        # timer.timeout.connect(dataVisualizer.updateData)
        # timer.start(50)

    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()

    def plotGraph(self):
        plt.cla()
        ax = self.figure.add_subplot(111)
        x = np.arange(0.0, 100.0, 0.01)
        y = np.sin(2 * np.pi * x)
        ax.plot(x, y)


qApp = QtGui.QApplication(sys.argv)

applicationWindow = ApplicationWindow()
applicationWindow.show()
sys.exit(qApp.exec_())
