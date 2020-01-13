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
        self.filesDirectories = []
    
    def setupUi(self):
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
        self.listWidgetListaArchivos.addItems(self.filesDirectories)

    def fnAbrirDir(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileDir = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        print(f"Files Folder {fileDir}")
        return fileDir

    def fnProcesaAddArchivo(self):
        
    def fnProcesaElimnarArchivo(self):
        print("Fn procesa eliminar")

    def fnProcesaCargarDatos(self):
        print("Fn procesa cargar datos")

    def fnProcesaMostarDatos(self):
        print("Fn procesa mostrar datos")

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
