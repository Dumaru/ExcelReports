import sys
import os
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.uic import loadUi


class ExcelReportsInicio(QMainWindow):
    """
    Window class to load all the files from a directory
    """
    def __init__(self, parent=None):
        # Calls the super class to init all the values in the this object
        super(ExcelReportsInicio, self).__init__()
        loadUi("UI/InicioSubirDatos.ui", self)
        self.setupUi()
    
    def setupUi(self):
        self.actionAbrir.triggered.connect(self.fnProcessOpenDir)

    def fnProcessOpenDir(self):
        dirPath = self.fnAbrirDir()
        if(dirPath):
            fileNames = os.listdir()
            self.listWidgetListaArchivos.addItems(fileNames)

    def fnAbrirDir(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileDir = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        print(f"Files Folder {fileDir}")
        return fileDir


if(__name__=="__main__"):
    # Instanciates a new QApplication with the given terminal parameters
    app=QApplication(sys.argv)
    inicioCarga = ExcelReportsInicio()
    inicioCarga.show()
    sys.exit(app.exec_())
