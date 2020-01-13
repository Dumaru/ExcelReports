import math, sys
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Overlay(QWidget):

    def __init__(self, parent = None):
        super(Overlay, self).__init__(parent)
        # QWidget.__init__(self, parent)
        palette = QPalette(self.palette())
        palette.setColor(palette.Background, Qt.transparent)
        self.setPalette(palette)
        # self.centerOnScreen()

    # def centerOnScreen (self):
        # '''centerOnScreen() Centers the window on the screen.'''
        # resolution = QDesktopWidget().screenGeometry()
        # self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                #   (resolution.height() / 2) - (self.frameSize().height() / 2)) 

    def paintEvent(self, event):
    
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(event.rect(), QBrush(QColor(255, 255, 255, 127)))
        painter.setPen(QPen(Qt.NoPen))
        
        for i in range(6):
            if (self.counter / 5) % 6 == i:
                painter.setBrush(QBrush(QColor(127 + (self.counter % 5)*32, 127, 127)))
            else:
                painter.setBrush(QBrush(QColor(127, 127, 127)))
            painter.drawEllipse(
                self.width()/2 + 30 * math.cos(2 * math.pi * i / 6.0) - 10,
                self.height()/2 + 30 * math.sin(2 * math.pi * i / 6.0) - 10,
                20, 20)
        
        painter.end()
    

    def showEvent(self, event):
        """ Process the show widget event, stating the timer"""
        # Creates a new timer with a time interval of 50 miliseconds and sets the timer id  
        self.timerId = self.startTimer(100)
        self.counter = 0
    
    def timerEvent(self, event):
    
        self.counter += 1
        self.update()
        # if self.counter == 60:
            # self.killTimer(self.timer)
            # self.hide()
    def killAndHied(self):
            self.killTimer(self.timer)
            self.hide()
