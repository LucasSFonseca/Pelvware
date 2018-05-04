import pyqtgraph as pg
from PyQt4 import QtGui, QtCore
import numpy as np

app = QtGui.QApplication([])

# Creation of the window and main widget.
win = QtGui.QMainWindow()
cw = QtGui.QWidget()
win.setCentralWidget(cw)

#
layout = QtGui.QHBoxLayout()
h = QtGui.QVBoxLayout()
h2 = QtGui.QHBoxLayout()
layout.addLayout(h)
layout.addLayout(h2)
cw.setLayout(layout)

pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'r')
p1 = pg.PlotWidget()

h2.addWidget(p1)

#menubar  = win.menuBar()
#fileMenu = menubar.addMenu('&File')

btn = QtGui.QPushButton('Button')
btn2 = QtGui.QPushButton('Button2')
h.addWidget(btn)
h.addWidget(btn2)
h.addStretch(1)

win.setWindowTitle("Teste")
win.setGeometry(300, 300, 1200, 800)
win.show()

p1.setDownsampling(mode='peak')
p1.setClipToView(True)
p1.setRange(xRange=[-100, 0])
p1.setLimits(xMax=0)
curve1 = p1.plot(pen='r')

data1 = np.empty(100)

ptr1 = 0


def update1():
    global data1, ptr1
    data1[ptr1] = np.random.normal()
    ptr1 += 1
    if ptr1 >= data1.shape[0]:
        tmp = data1
        data1 = np.empty(data1.shape[0] * 2)
        data1[:tmp.shape[0]] = tmp

    curve1.setData(data1[:ptr1])
    curve1.setPos(-ptr1, 0)

    #curve2.setData(data1)
    #curve2.setPos(ptr1, 0)


timer = pg.QtCore.QTimer()
timer.timeout.connect(update1)
timer.start(50)

if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()