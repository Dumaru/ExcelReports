import sys
import os
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.uic import loadUi
from LoadingOverlay import Overlay
from PandasUtils import PandasDataLoader
import UiUtils


class ExcelReportsInicio(QMainWindow):
    """
    Window class to load all the files from a directory
    """

    def __init__(self, parent=None, pandasUtilsInstance=None):
        # Calls the super class to init all the values in the this object
        super(ExcelReportsInicio, self).__init__(parent)
        # State Fields
        self.filesDirectories = []
        self.pandasUtils = pandasUtilsInstance if pandasUtilsInstance is not None else PandasDataLoader.getInstance()

        # UI
        loadUi("UI/InicioSubirDatos.ui", self)
        self.overlay = Overlay(self)
        self.setupUi()

    def setupUi(self):
        self.overlay.hide()
        # Links all the events for the different actions and buttons
        self.actionAbrir.triggered.connect(self.fnProcessOpenDir)
        self.pushButtonAnadirArchivo.clicked.connect(self.fnProcesaAddArchivo)
        self.pushButtonEliminar.clicked.connect(self.fnProcesaElimnarArchivo)
        self.pushButtonCargarDatos.clicked.connect(self.fnProcesaCargarDatos)
        self.pushButtonMostrarDatos.clicked.connect(self.fnProcesaMostarDatos)
        self.pushButtonMostrarDatos.setEnabled(False)

    def fnProcessOpenDir(self):
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
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileDir = str(QFileDialog.getExistingDirectory(
            self, "Selecciona una carpeta"))
        print(f"Files Folder {fileDir}")
        return fileDir

    def fnProcesaAddArchivo(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(
            self, "Añadir archivo", "", "All Files (*);;Excel files (*.xlsx)", options=options)
        if fileName:
            print(fileName)
            self.filesDirectories.append(fileName)
            self.fnMuestraDirectorios()
            print(f"Directory {fileName}")

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
            # self.pandasUtils.loadDataframes(self.filesDirectories, self.fnCargaDatosCompleta)
            self.pandasUtils.loadDataframes(
                self.filesDirectories, self.fnCargaDatosCompleta)
        else:
            UiUtils.showInfoMessage(parent=self,
                                    title="Informacion de carga",
                                    description=f"No se han cargado archivos.")

    def fnCargaDatosCompleta(self):
        self.overlay.killAndHide()
        UiUtils.showInfoMessage(parent=self,
                                title="Informacion de carga",
                                description=f"Se cargaron {len(self.pandasUtils.dfsList)} archivos.")
        self.pushButtonMostrarDatos.setEnabled(True)

    def resizeEvent(self, event):
        self.overlay.resize(event.size())
        event.accept()

    def fnProcesaMostarDatos(self):
        """ Muestra la ventana general de datos"""
        self.hide()
        # Alternativamente le podria pasar una referencia al objeto pandas
        vistaGeneralDatos = VistaGeneralDatos(parent=self)
        vistaGeneralDatos.show()


class VistaGeneralDatos(QMainWindow):
    def __init__(self, parent=None, pandasUtilsInstance=None):
        super(VistaGeneralDatos, self).__init__(parent)
        # State fields
        self.pandasUtils = pandasUtilsInstance if pandasUtilsInstance is not None else PandasDataLoader.getInstance()
        # UI
        loadUi('UI/VistaGeneralDatos.ui', self)
        self.setupUi()

    def setupUi(self):
        print("Setting general UI values")
        self.comboBoxRAT.clear()
        self.pandasUtils.setUniqueColumnValues(self.pandasUtils.allData, 'RAT')
        self.comboBoxRAT.addItems(
            self.pandasUtils.getUniqueColumnValues('RAT'))
        self.comboBoxOPERADOR.clear()
        self.pandasUtils.setUniqueColumnValues(
            self.pandasUtils.allData, 'OPERATOR')
        self.comboBoxOPERADOR.addItems(
            self.pandasUtils.getUniqueColumnValues('OPERATOR'))

        self.labelIMEIDatos.setText(
            str(self.pandasUtils.getRowCountForColumn(self.pandasUtils.allData, "IMEI")))
        self.labelIMSIDatos.setText(
            str(self.pandasUtils.getRowCountForColumn(self.pandasUtils.allData, "IMSI")))

        # Connects signals to sloots and callbacks
        self.comboBoxOPERADOR.currentTextChanged.connect(
            self.fnProcesaCambioOperador)
        self.comboBoxRAT.currentTextChanged.connect(self.fnProcesaCambioRAT)
        # Calls manually to set a initial value
        self.fnProcesaCambioRAT(self.pandasUtils.getUniqueColumnValues('RAT')[0])
        self.fnProcesaCambioOperador(self.pandasUtils.getUniqueColumnValues('OPERATOR')[0])
    def fnProcesaCambioRAT(self, paramText):
        print(f"Fn procesa cambio Rat {paramText}")
        cantidad = self.pandasUtils.getCantidadDatos(self.pandasUtils.allData, 'RAT', [paramText])

        self.labelRATContador.setText(str(cantidad))

    def fnProcesaCambioOperador(self, paramText):
        print(f"Fn procesa cambio Operator {paramText}")
        cantidad = self.pandasUtils.getCantidadDatos(
            self.pandasUtils.allData, 'OPERATOR', [paramText])
        self.labelOperadorDatos.setText(str(cantidad))


if(__name__ == "__main__"):
    # Instanciates a new QApplication with the given terminal parameters
    pandasDataInstance = PandasDataLoader()
    app = QApplication(sys.argv)
    inicioCarga = ExcelReportsInicio()
    inicioCarga.show()
    # vistaGeneralDatos = VistaGeneralDatos()
    # vistaGeneralDatos.show()
    sys.exit(app.exec())
