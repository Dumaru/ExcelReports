import sys
import os
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.uic import loadUi
from LoadingOverlay import Overlay 

class ExcelReportsInicio(QMainWindow):
    """
    Window class to load all the files from a directory
    """
    def __init__(self, parent=None):
        # Calls the super class to init all the values in the this object
        super(ExcelReportsInicio, self).__init__()
        loadUi("UI/InicioSubirDatos.ui", self)
        self.setupUi()
        self.filesDirectories = []
        self.overlay = Overlay(self)
        self.overlay.hide()
    
    def setupUi(self):
        # Links all the events for the different actions and buttons
        self.actionAbrir.triggered.connect(self.fnProcessOpenDir)
        self.pushButtonAnadirArchivo.clicked.connect(self.fnProcesaAddArchivo)
        self.pushButtonEliminar.clicked.connect(self.fnProcesaElimnarArchivo)
        self.pushButtonCargarDatos.clicked.connect(self.fnProcesaCargarDatos)
        self.pushButtonMostrarDatos.clicked.connect(self.fnProcesaMostarDatos)

    def fnProcessOpenDir(self):
        dirPath = self.fnAbrirDir()
        if(dirPath):
            with os.scandir(dirPath) as it:
                for entry in it:
                    if not entry.name.startswith(('.','~$')) and entry.is_file():
                        self.filesDirectories.append(entry.path)
                        self.fnMuestraDirectorios()

    def fnMuestraDirectorios(self):
        self.listWidgetListaArchivos.clear()
        self.listWidgetListaArchivos.addItems(self.filesDirectories)

    def fnAbrirDir(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileDir = str(QFileDialog.getExistingDirectory(self, "Selecciona una carpeta"))
        print(f"Files Folder {fileDir}")
        return fileDir

    def fnProcesaAddArchivo(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Añadir archivo", "","All Files (*);;Excel files (*.xlsx)", options=options)
        if fileName:
            print(fileName)
            self.filesDirectories.append(fileName)
            self.fnMuestraDirectorios()
            print(f"Directory {fileName}")

    def fnProcesaElimnarArchivo(self):
        selectedItems = self.listWidgetListaArchivos.selectedItems()
        self.filesDirectories = list(set(self.filesDirectories).difference([item.text() for item in selectedItems ]))
        self.fnMuestraDirectorios()

    def fnProcesaCargarDatos(self):
        self.overlay.show()

    def fnProcesaMostarDatos(self):
        print("Fn procesa mostrar datos")

    def resizeEvent(self, event):
        self.overlay.resize(event.size())
        event.accept()

class VistaGeneralDatos(QMainWindow):
    def __init__(self, parent=None):
        super(VistaGeneralDatos, self).__init__()
        loadUi('UI/VistaGeneralDatos.ui')
    
    
if(__name__=="__main__"):
    # Instanciates a new QApplication with the given terminal parameters
    app=QApplication(sys.argv)
    inicioCarga = ExcelReportsInicio()
    inicioCarga.show()
    # vistaGeneralDatos = VistaGeneralDatos()
    # vistaGeneralDatos.show()
    sys.exit(app.exec_())
