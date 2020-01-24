import sys
import os
import pandas as pd
import PyQt5
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFileDialog,
                             QAction, QTableWidgetItem, QTableWidget, QHeaderView)
from PyQt5.uic import loadUi
from LoadingOverlay import Overlay
from PandasUtils import PandasDataLoader
import UiUtils
import pandas as pd
from VistaGeneralDatos import VistaGeneralDatos

from UIPyfiles.InicioSubirDatos import Ui_vistaInicioSubirDatos

from UI.Recursos import images_rc


class ExcelReportsInicio(QMainWindow, Ui_vistaInicioSubirDatos):
    """
    Window class to load all the files from a directory
    """

    def __init__(self, parent=None, pandasUtilsInstance=None):
        # Calls the super class to init all the values in the this object
        QMainWindow.__init__(self)
        Ui_vistaInicioSubirDatos.__init__(self)
        self.setupUi(self)
        # State Fields
        self.filesDirectories = []
        self.pandasUtils = pandasUtilsInstance

        # UI
        # loadUi('', self)
        self.overlay = Overlay(self)
        self.setupUiCustom()
        self.vistaGeneralDatos = VistaGeneralDatos(parent=self, pandasUtilsInstance=self.pandasUtils)

    def setupUiCustom(self):
        self.overlay.hide()
        # Links all the events for the different actions and buttons
        self.actionAbrir.triggered.connect(self.fnProcessOpenDir)
        self.pushButtonAnadirArchivo.clicked.connect(self.fnProcesaAddArchivo)
        self.pushButtonEliminar.clicked.connect(self.fnProcesaElimnarArchivo)
        self.pushButtonCargarDatos.clicked.connect(self.fnProcesaCargarDatos)
        self.pushButtonMostrarDatos.clicked.connect(self.fnProcesaMostarDatos)
        self.pushButtonMostrarDatos.setEnabled(False)

    def fnProcessOpenDir(self):
        """ Inicia procesa para abrir un solo directorio"""
        dirPath = self.fnAbrirDir()
        if(dirPath):
            with os.scandir(dirPath) as it:
                for entry in it:
                    if not entry.name.startswith(('.', '~$')) and entry.is_file():
                        self.filesDirectories.append(entry.path)
                        self.fnMuestraDirectorios()

    def fnMuestraDirectorios(self):
        self.listWidgetListaArchivos.clear()
        self.listWidgetListaArchivos.addItems(self.filesDirectories)

    def fnAbrirDir(self):
        """
        Opens a folder dialog and returns the path to the folder
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileDir = str(QFileDialog.getExistingDirectory(
            self, "Selecciona una carpeta"))
        # print(f"Files Folder {fileDir}")
        return fileDir

    def saveFileDialog(self, title: str):
        """
        Opens a save file dialog and returns the path to the file
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(
            self, "Guardar archivo", "", "All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            return fileName

    def fnProcesaAddArchivo(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(
            self, "Añadir archivo", "", "All Files (*);;Excel files (*.xlsx)", options=options)
        if fileName:
            # print(fileName)
            self.filesDirectories.append(fileName)
            self.fnMuestraDirectorios()
            # print(f"Directory {fileName}")

    def fnProcesaElimnarArchivo(self):
        selectedItems = self.listWidgetListaArchivos.selectedItems()
        if(len(selectedItems)):
            self.filesDirectories = list(set(self.filesDirectories).difference([
                                         item.text() for item in selectedItems]))
            self.fnMuestraDirectorios()

    def fnProcesaCargarDatos(self):
        """
        Carga todos los paths en una lista de dataframes de pandas
        """
        if(len(self.filesDirectories) > 0):
            self.overlay.show()
            self.pandasUtils.loadDataframes(
                self.filesDirectories, self.fnCargaDatosCompleta)
        else:
            UiUtils.showInfoMessage(title="Informacion de carga",
                                    description=f"No se han subido archivos a la lista.")

    def fnCargaDatosCompleta(self, msg):
        self.overlay.killAndHide()
        UiUtils.showInfoMessage(title="Informacion de carga", description=msg)
        self.pushButtonMostrarDatos.setEnabled(True)

    def resizeEvent(self, event):
        self.overlay.resize(event.size())
        event.accept()

    def fnProcesaMostarDatos(self):
        """ Muestra la ventana general de datos"""
        self.hide()
        # Alternativamente le podria pasar una referencia al objeto pandas
        self.vistaGeneralDatos.setupUiCustom()
        self.vistaGeneralDatos.show()


if(__name__ == "__main__"):
    # Instanciates a new QApplication with the given terminal parameters

    app = QApplication(sys.argv)

    pandasDataInstance = PandasDataLoader()
    inicioCarga = ExcelReportsInicio(parent=None, pandasUtilsInstance=pandasDataInstance)
    inicioCarga.show()
    # vistaGeneralDatos = VistaGeneralDatos()
    # vistaGeneralDatos.show()
    sys.exit(app.exec())
