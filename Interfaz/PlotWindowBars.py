import sys
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import random


class PlotWindowBars(QDialog):
    def __init__(self, parent=None):
        super(PlotWindowBars, self).__init__(parent)

        # a figure instance to plot on
        self.figure = plt.figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Just some button connected to `plot` method
        # self.button = QPushButton('Plot')
        # self.button.clicked.connect(self.plot)

        # set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        # layout.addWidget(self.button)
        self.setLayout(layout)

    def plot(self, xLabel: str="X", yLabel: str="Y", x=None, y=None):
        ''' plot some random stuff '''
        # instead of ax.hold(False)
        self.figure.clear()

        # create an axis
        ax = self.figure.add_subplot(111)

        idx = [i for i in range(len(x[:20]))]
        heights = y[:20]
        width = 0.4
        # plot data
        ax.bar(idx, heights, width=width)
        ax.set_xticks(idx)
        ax.set_xticklabels(x[:20], rotation=80)
        ax.set_xlabel(xLabel)
        ax.set_ylabel(yLabel)

        # refresh canvas
        self.figure.tight_layout()
        self.canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    PlotWindow = Window()
    PlotWindow.show()

    sys.exit(app.exec_())
