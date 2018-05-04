import sys
from PyQt4 import QtGui, QtCore, QtWebKit

from plotly.offline import plot
from plotly.graph_objs import Scatter, Scattergl, Figure, Layout

import numpy as np


class Browser(QtWebKit.QWebView):
    def __init__(self):
        QtWebKit.QWebView.__init__(self)
        self.loadFinished.connect(self._result_available)

    def _result_available(self, ok):
        frame = self.page().mainFrame()
        #print unicode(frame.toHtml()).encode('utf-8')


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
        view = Browser()

        vBoxLayout.addWidget(btn)
        vBoxLayout.addWidget(btn2)
        vBoxLayout.addStretch(1)
        hBoxLayout2.addWidget(view)

        random_x = np.linspace(-1000, 1000, 1000)
        random_y = np.random.randn(1000)

        #layout = Layout(showlegend=False)

        #trace = Scattergl(x=random_x, y=random_y)
        #data = [trace]
        #fig = Figure(data=data, layout=layout)

        view.load(
            QtCore.QUrl(
                plot(
                    [Scattergl(x=random_x, y=random_y)],
                    auto_open=False,
                    show_link=False,
                    filename='teste.html')))
        view.settings().setAttribute(QtWebKit.QWebSettings.WebGLEnabled, True)
        view.settings().setAttribute(QtWebKit.QWebSettings.JavascriptEnabled, True)
        view.show()

    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()


qApp = QtGui.QApplication(sys.argv)

applicationWindow = ApplicationWindow()
applicationWindow.show()
sys.exit(qApp.exec_())
