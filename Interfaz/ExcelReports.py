import sys
import os
import pandas as pd
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFileDialog,
                             QAction, QTableWidgetItem, QTableWidget, QHeaderView)
from PyQt5.uic import loadUi
from LoadingOverlay import Overlay
from PandasUtils import PandasDataLoader
import UiUtils
import pandas as pd


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
            UiUtils.showInfoMessage(title="Informacion de carga",
                                    description=f"No se han cargado archivos.")

    def fnCargaDatosCompleta(self):
        self.overlay.killAndHide()
        UiUtils.showInfoMessage(title="Informacion de carga",
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
        self.ratsSeleccionados = dict()
        self.operadoresSeleccionados = dict()

        # UI
        loadUi('UI/VistaGeneralDatos.ui', self)
        self.setupUi()

    def setupUi(self):
        print("Setting the menus for the buttons")
        self.pandasUtils.setUniqueColumnValues(self.pandasUtils.allData, 'RAT')
        self.ratsSeleccionados = {
            rat: True for rat in self.pandasUtils.getUniqueColumnValues('RAT')}
        menuRats = UiUtils.createMenu(self.ratsSeleccionados.keys())

        self.pandasUtils.setUniqueColumnValues(
            self.pandasUtils.allData, 'OPERATOR')
        self.operadoresSeleccionados = {
            op: True for op in self.pandasUtils.getUniqueColumnValues('OPERATOR')}
        menuOperadores = UiUtils.createMenu(
            self.operadoresSeleccionados.keys())

        self.pushButtonOperadores.setMenu(menuOperadores)
        self.pushButtonRATS.setMenu(menuRats)

        # Establece contadores inicialmente
        self.fnMuestraCantidadEnRats()
        self.fnMuestraCantidadEnOperadores()
        self.labelIMEIDatos.setText(
            str(self.pandasUtils.getRowCountForColumn(self.pandasUtils.allData, "IMEI")))
        self.labelIMSIDatos.setText(
            str(self.pandasUtils.getRowCountForColumn(self.pandasUtils.allData, "IMSI")))

        # Connects signals to sloots and callbacks
        menuOperadores.triggered.connect(self.fnProcesaSeleccionOperadores)
        menuRats.triggered.connect(self.fnProcesaSeleccionRats)
        self.pushButtonBuscarDato.clicked.connect(self.fnProcesaFiltroImei)
        # Fill the table with a df where all the EMAIS are
        self.fillTableWidget(
            self.pandasUtils.getDfCompletoEmaisOk(self.pandasUtils.allData))

    def fnProcesaFiltroImei(self):
        imei = self.textEditBuscarDatos.toPlainText()
        if(len(imei) > 0):
            df = pandasDataInstance.filterDfByEmai(
                pandasDataInstance.allData, imei)
            if(df.shape[0] > 0):
                print("Shape del filtro ", df.shape)
                self.fillTableWidget(df)
            else:
                UiUtils.showInfoMessage(self,
                                        title=f"Busqueda de imei: {imei} ",
                                        description=f"No se encontro el imei {imei} .")

    def fnAplicaFiltrosDfOk(self, df):
        """
        Calls filltable according to all the filters that the user has set and returns the df
        """
        listaRats = [rat for rat, v in self.ratsSeleccionados.items()
                     if v is True]
        listaOps = [rat for rat,
                    v in self.operadoresSeleccionados.items() if v]
        dfFiltradoRats = self.pandasUtils.filterDfByColumnValues(
            self.pandasUtils.allData, "RAT", listaRats
        )
        dfFiltradosOps = self.pandasUtils.filterDfByColumnValues(
            dfFiltradoRats, "OPERATOR", listaOps
        )

        return dfFiltradosOps

    def fillTableWidget(self, df: pd.DataFrame = None):
        # TODO: Hacerla general recibiendo el widget
        # Limpiar contenidos de tabla
        headerList = tuple(df.columns.values)
        self.tableWidgetDatosExcel.clearContents()
        self.tableWidgetDatosExcel.setColumnCount(len(headerList))
        self.tableWidgetDatosExcel.setHorizontalHeaderLabels(headerList)
        self.tableWidgetDatosExcel.horizontalHeader().setStretchLastSection(True)
        self.tableWidgetDatosExcel.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        rowCount = 0
        for row in df.itertuples():
            # Sets the number of rows in this table's model to rows. If this is less than rowCount(),
            # the data in the unwanted rows is discarded.
            self.tableWidgetDatosExcel.setRowCount(rowCount+1)
            for i, columnName in enumerate(headerList):
                # val = QTableWidgetItem(row._asdict()[str(columnName)])
                val = QTableWidgetItem(str(row._asdict()[columnName]))
                
                self.tableWidgetDatosExcel.setItem(rowCount, i, val)
            rowCount += 1

    def fnProcesaSeleccionRats(self, action: QAction):
        print(f"Fn procesa seleccion Rat {action}")
        self.ratsSeleccionados[str(action.data())] = action.isChecked()
        self.fnMuestraCantidadEnRats()

    def fnMuestraCantidadEnRats(self):
        """
        This function is called when there is a change in the selected rats dictionary
        """
        listaRats = [rat for rat, v in self.ratsSeleccionados.items()
                     if v is True]
        print(f"Lista rats {listaRats}")
        if len(listaRats) > 0:
            cantidad = self.pandasUtils.getCantidadDatos(
                self.pandasUtils.allData, 'RAT', listaRats)
            self.labelRATContador.setText(str(cantidad))
            self.fillTableWidget(
                self.fnAplicaFiltrosDfOk(
                                self.pandasUtils.getDfCompletoEmaisOk(
                                    self.pandasUtils.allData)
                            )
                )

    def fnProcesaSeleccionOperadores(self, action: QAction):
        print(f"Fn procesa seleccion opeadores {action}")
        self.operadoresSeleccionados[str(action.data())] = action.isChecked()
        self.fnMuestraCantidadEnOperadores()

    def fnMuestraCantidadEnOperadores(self):
        """
        This function is called when there is a change in the selected rats dictionary
        """
        listaOps = [rat for rat,
                    v in self.operadoresSeleccionados.items() if v]
        if len(listaOps) > 0:
            cantidad = self.pandasUtils.getCantidadDatos(
                self.pandasUtils.allData, 'OPERATOR', listaOps)
            self.labelOperadorDatos.setText(str(cantidad))
            self.fillTableWidget(
                self.fnAplicaFiltrosDfOk(
                    self.pandasUtils.getDfCompletoEmaisOk(
                        self.pandasUtils.allData)
                )
            )


if(__name__ == "__main__"):
    # Instanciates a new QApplication with the given terminal parameters
    pandasDataInstance = PandasDataLoader()
    app = QApplication(sys.argv)
    inicioCarga = ExcelReportsInicio()
    inicioCarga.show()
    # vistaGeneralDatos = VistaGeneralDatos()
    # vistaGeneralDatos.show()
    sys.exit(app.exec())
