import sys
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import random


class PlotWindow(QDialog):
    def __init__(self, parent=None):
        super(PlotWindow, self).__init__(parent)

        # a figure instance to plot on
        self.figure = plt.figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Just some button connected to `plot` method
        self.button = QPushButton('Plot')
        self.button.clicked.connect(self.plot)

        # set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def plot(self, data=None, xLabel: str="X", yLabel: str="Y", x=None, y=None):
        ''' plot some random stuff '''
        # instead of ax.hold(False)
        self.figure.clear()

        # create an axis
        ax = self.figure.add_subplot(111)

        # rotate and align the tick labels so they look better
        self.figure.autofmt_xdate()

        # discards the old graph
        # ax.hold(False) # deprecated, see above
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        # plot data
        if x is not None and y is not None:
            ax.plot(x, y, '*-')
            ax.set_xlabel(xLabel)
            ax.set_ylabel(yLabel)
        else:
            ax.plot(xLabel, yLabel, 'ro-',data=data)

        # refresh canvas
        self.canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    PlotWindow = Window()
    PlotWindow.show()

    sys.exit(app.exec_())
