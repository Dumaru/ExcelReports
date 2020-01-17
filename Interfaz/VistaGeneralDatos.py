from PyQt5.QtWidgets import (QApplication, QMainWindow, QFileDialog, QAbstractItemView,
                             QAction, QTableWidgetItem, QTableWidget, QHeaderView)
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
import pandas as pd
from PandasUtils import PandasDataLoader
import UiUtils
from VentanaFiltros import VentanaFiltros
from VentanaAnalisisHorario import VentanaAnalisisHorario

class VistaGeneralDatos(QMainWindow):
    def __init__(self, parent=None, pandasUtilsInstance=None):
        super(VistaGeneralDatos, self).__init__(parent)
        # State fields
        self.pandasUtils = pandasUtilsInstance if pandasUtilsInstance is not None else PandasDataLoader.getInstance()
        self.ratsSeleccionados = dict()
        self.operadoresSeleccionados = dict()
        self.viendoIncidentales = False
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
        # Boton exportar
        self.pushButtonGuardarDatos.clicked.connect(self.fnProcesaGuardarDatos)
        # Boton Analisis horario
        self.pushButtonAnalisisHorario.clicked.connect(
            self.fnVentanaAnalisisHorario)
        # Btn Ver datos indidentales
        self.pushButtonVerDatosIncidentales.clicked.connect(
            self.fnFiltroDatosIncidentales)
        # Btn Ver tabla original
        self.pushButtonVerTablaOriginal.clicked.connect(
            self.fnMuestraTablaOriginal)
        # Btn volver a principal de inicio
        self.actionIr_A_Principal.triggered.connect(
            self.fnMuestraVentanaPrincipal)
        # Btn ventana filtro  de datos
        self.pushButtonFiltrarDatos.clicked.connect(self.fnVentanaFiltroDatos)
        # Btn asignar nombres para los emais
        self.pushButtonAsignarNombresIMEI.clicked.connect(
            self.fnAsignaNombresPorEmais)
        # Fill the table with a df where all the EMAIS are
        self.tableWidgetDatosExcel.setWordWrap(False)
        self.tableWidgetDatosExcel.setTextElideMode(Qt.ElideRight)# Qt.ElideNone
        self.tableWidgetDatosExcel.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidgetDatosExcel.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.fillTableWidget(
            self.pandasUtils.getDfCompletoEmaisOk(self.pandasUtils.getDfCompletoEmaisOk(self.pandasUtils.allData)))

    def reseteoFiltros(self):
        self.operadoresSeleccionados = {
            op: 1 for op in self.operadoresSeleccionados.keys()}
        self.ratsSeleccionados = {
            rat: 1 for rat in self.ratsSeleccionados.keys()}

    def fnMuestraTablaOriginal(self):
        self.viendoIncidentales = False
        self.reseteoFiltros()
        self.fillTableWidget(
            self.pandasUtils.allData
        )

    def fnMuestraVentanaPrincipal(self):
        self.parent().show()
        self.hide()

    def fnVentanaFiltroDatos(self):
        print(f"Fn ventana filtro de datos")
        self.hide()
        ventanaFiltroDatos = VentanaFiltros(
            parent=self, pandasUtilsInstance=self.pandasUtils)
        ventanaFiltroDatos.show()

    def fnAsignaNombresPorEmais(self):
        self.pandasUtils.allData = self.pandasUtils.setUniqueNameIdColumn(
            self.pandasUtils.getDfCompletoEmaisOk(self.pandasUtils.allData)
        ) 
        self.fillTableWidget(
            self.pandasUtils.allData
        )
        print(f"Fn asgina nombre a emai")

    def fnFiltroDatosIncidentales(self):
        self.viendoIncidentales = True
        self.fillTableWidget(
            self.pandasUtils.dfIncidentales
        )

    def fnVentanaAnalisisHorario(self):
        self.hide()
        df = self.fnAplicaFiltrosDfOk()
        ventanaAnalisisHorario = VentanaAnalisisHorario(self, self.pandasUtils, data=df)
        ventanaAnalisisHorario.show()
        print(f"Fn analisis horario")




    def fnProcesaGuardarDatos(self):
        print("Fn procesa guardar datos")
        filePath = self.saveFileDialog()
        if(filePath):
            dfToSave = self.fnAplicaFiltrosDfOk()
            self.pandasUtils.saveToExcelFile(
                dfToSave, filePath, False, self.saveProcessFinished)

    def saveProcessFinished(self):
        UiUtils.showInfoMessage(parent=self, title="Guardado de archivo",
                                description=f"Se guardo el archivo.")

    def saveFileDialog(self):
        """
        Opens a save file dialog and returns the path to the file
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(
            self, "Guardar archivo", "", "Excel Files (*.xlsx)", options=options)
        return fileName

    def fnAplicaFiltrosDfOk(self):
        """
        Calls filltable according to all the filters that the user has set and returns the df
        """
        df = self.pandasUtils.allData if self.viendoIncidentales is False else self.pandasUtils.dfIncidentales
        # TODO: Tambien tener en cuenta que pudo haber digitado un imei
        listaRats = [rat for rat, v in self.ratsSeleccionados.items() if v is True]
        listaOps = [op for op, v in self.operadoresSeleccionados.items() if v is True]
        dfFiltradoRats = self.pandasUtils.filterDfByColumnValues(
            self.pandasUtils.allData, "RAT", listaRats
        )
        dfFiltradosOps = self.pandasUtils.filterDfByColumnValues(
            dfFiltradoRats, "OPERATOR", listaOps
        )

        return dfFiltradosOps

    def fnProcesaFiltroImei(self):
        imei = self.textEditBuscarDatos.toPlainText()
        if(len(imei) > 0):
            df = self.pandasUtils.filterDfByEmai(
                self.pandasUtils.allData, imei)
            if(df.shape[0] > 0):
                print("Shape del filtro ", df.shape)
                self.fillTableWidget(df)
            else:
                UiUtils.showInfoMessage(self,
                                        title=f"Busqueda de imei: {imei} ",
                                        description=f"No se encontro el imei {imei} .")

    def fillTableWidget(self, df: pd.DataFrame = None):
        # TODO: Hacerla general recibiendo el widget
        # Limpiar contenidos de tabla
        headerList = tuple(df.columns.values)
        self.tableWidgetDatosExcel.clearContents()
        self.tableWidgetDatosExcel.setColumnCount(len(headerList))
        self.tableWidgetDatosExcel.setHorizontalHeaderLabels(headerList)
        self.tableWidgetDatosExcel.horizontalHeader().setStretchLastSection(True)
        self.tableWidgetDatosExcel.horizontalHeader(
        ).setSectionResizeMode(QHeaderView.Stretch)
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
                self.fnAplicaFiltrosDfOk()
            )

    def fnProcesaSeleccionOperadores(self, action: QAction):
        print(f"Fn procesa seleccion opeadores {action}")
        self.operadoresSeleccionados[str(action.data())] = action.isChecked()
        self.fnMuestraCantidadEnOperadores()

    def fnMuestraCantidadEnOperadores(self):
        """
        This function is called when there is a change in the selected rats dictionary
        """
        listaOps = [op for op,v in self.operadoresSeleccionados.items() if v]
        if len(listaOps) > 0:
            cantidad = self.pandasUtils.getCantidadDatos(
                self.pandasUtils.allData, 'OPERATOR', listaOps)
            self.labelOperadorDatos.setText(str(cantidad))
            self.fillTableWidget(
                self.fnAplicaFiltrosDfOk()
            )
