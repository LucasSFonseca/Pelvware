import sys
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QUrl
from PyQt4.QtWebKit import QWebView

from plotly.offline import plot
from plotly.graph_objs import Scatter


class Browser(QWebView):

    def __init__(self):
        QWebView.__init__(self)
        self.loadFinished.connect(self._result_available)

    def _result_available(self, ok):
        frame = self.page().mainFrame()
        print unicode(frame.toHtml()).encode('utf-8')


app = QApplication(sys.argv)
view = Browser()
view.load(QUrl(plot([Scatter(x=[1, 2, 3], y=[3, 1, 6])], auto_open=False, show_link=False, filename='teste.html')))
view.show()
app.exec_()