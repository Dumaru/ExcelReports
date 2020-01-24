import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFileDialog, QAbstractItemView,
                             QAction, QActionGroup, QTableWidgetItem, QTableWidget, QHeaderView, QMenu)
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
import pandas as pd
from PandasUtils import PandasDataLoader
from PlotWindow import PlotWindow
from FiltrosContainer import FiltrosContainer
import UiUtils
from VistaAnalisisDatos import VentanaAnalisisDatos

from LoadingOverlay import Overlay

from UIPyfiles.VistaFiltros import Ui_VistaFiltros
from UI.Recursos import images_rc

from PlotWindowBars import PlotWindowBars

class VentanaFiltros(QMainWindow, Ui_VistaFiltros):
    ACTION_IMSIS = 1
    ACTION_FECHAS = 2
    ACTION_CANALES = 3
    ACTION_OPERADORES = 4

    def __init__(self, parent=None, pandasUtilsInstance=None):
        super(QMainWindow, self).__init__(parent)
        Ui_VistaFiltros.__init__(self)
        self.setupUi(self)
        # State fields
        self.pandasUtils = pandasUtilsInstance if pandasUtilsInstance is not None else PandasDataLoader.getInstance()
        self.filtros2G = FiltrosContainer()
        self.filtros3G = FiltrosContainer()
        self.filtros4G = FiltrosContainer()
        # UI
        # loadUi('UI/VistaFiltros.ui', self)
        self.overlay = Overlay(self)
        # self.setupUiCustom()

    def setupUiCustom(self):
        self.overlay.hide()
        # Set rats based on the db
        # RAT Checkboxes setup
        # self.pandasUtils.setUniqueColumnValues(self.pandasUtils.allData, 'RAT')
        # self.ratsSeleccionados = {
            # rat: True for rat in self.pandasUtils.getUniqueColumnValues('RAT')
        # }
        self.pandasUtils.setTempDf(self.pandasUtils.getAllData())
        self.checkBox2G.setChecked(True)
        self.checkBox3G.setChecked(True)
        self.checkBox4G.setChecked(True)
        self.checkBox2G.stateChanged.connect(self.fnProcesaSeleccionRat)
        self.checkBox3G.stateChanged.connect(self.fnProcesaSeleccionRat)
        self.checkBox4G.stateChanged.connect(self.fnProcesaSeleccionRat)
        self.seteaValoresTA()
        # Checkbox tomar datos ms power de 2g 3g y 4g
        self.checkBoxTomarDatoMSPower2G.stateChanged.connect(self.fnProcesaTomaDatosMsPower)
        self.checkBoxTomarDatoMSPower3G.stateChanged.connect(self.fnProcesaTomaDatosMsPower)
        self.checkBoxTomarDatoMSPower4G.stateChanged.connect(self.fnProcesaTomaDatosMsPower)
        # Push buttons signals
        self.pushButtonObtenerDatosFiltrados.clicked.connect(self.fnProcesaObtenerDatosFiltrados)
        self.pushButtonGenerarGraficas.clicked.connect(self.fnGeneraGraficaDatosFiltrados)
        self.pushButtonVerAnalisis.clicked.connect(self.fnMuestraVentanaAnalisis)
        self.pushButtonBuscarDatos.clicked.connect(self.fnProcesaBusquedaDatos)
        self.pushButtonGuardarBusqueda.clicked.connect(self.fnGuardarTablaFiltrada)
        # Limpiar selecciones last lac etc
        self.pushButtonLimpiarSeleccion2G.clicked.connect(lambda state: self.fnProcesaLimpiezaRat("2G"))
        self.pushButtonLimpiarSeleccion3G.clicked.connect(lambda state: self.fnProcesaLimpiezaRat("3G"))
        self.pushButtonLimpiarSeleccion4G.clicked.connect(lambda state: self.fnProcesaLimpiezaRat("4G"))

        self.actionIrADatosGenerales.triggered.connect(self.fnMostrarDatosGenerales)

        # Tabla previsualizacion
        self.tableWidgetMostrarSeleccion.setWordWrap(False)
        self.tableWidgetMostrarSeleccion.setAlternatingRowColors(True)
        self.tableWidgetMostrarSeleccion.setTextElideMode(Qt.ElideRight)  # Qt.ElideNone

        # Tabla Datos filtrados
        # Seleccionar toda la fila
        # self.tableWidgetVerDatosFiltrados.setSelectionBehavior(QAbstractItemView.SelectRows)
        # Seleccionar una fila a la vez
        self.tableWidgetVerDatosFiltrados.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableWidgetVerDatosFiltrados.setAlternatingRowColors(True)
        self.tableWidgetVerDatosFiltrados.setWordWrap(False)
        self.tableWidgetVerDatosFiltrados.setTextElideMode(Qt.ElideRight)  # Qt.ElideNone

        self.tableWidgetVerDatosFiltrados.setContextMenuPolicy(Qt.CustomContextMenu)
        # Establece la funcion que crea el menu contextual y le pasa la posicion
        self.tableWidgetVerDatosFiltrados.customContextMenuRequested.connect(self.menuContextualDatosFiltrados)
        # Menus y sus botones
        lastLacFreq2G = self.pandasUtils.lastLacFrecuenciaSeries(self.pandasUtils.allData2G)
        self.filtros2G.valoresLastLac = {lastLac: True for lastLac, f in lastLacFreq2G.items()}
        self.menu2GLastLac = UiUtils.createDynamicMenu(lastLacFreq2G)
        self.pushButtonLastLac2G.setMenu(self.menu2GLastLac)
        self.menu2GLastLac.triggered.connect(self.fnProcesaMenuLastLac2G)

        lastLacFreq3G = self.pandasUtils.lastLacFrecuenciaSeries(self.pandasUtils.allData3G)
        self.filtros3G.valoresLastLac = {lastLac: True for lastLac, f in lastLacFreq3G.items()}
        self.menu3GLastLac = UiUtils.createDynamicMenu(lastLacFreq3G)
        self.pushButtonLastLac3G.setMenu(self.menu3GLastLac)
        self.menu3GLastLac.triggered.connect(self.fnProcesaMenuLastLac3G)

        lastLacFreq4G = self.pandasUtils.lastLacFrecuenciaSeries(self.pandasUtils.allData4G)
        self.filtros4G.valoresLastLac = {lastLac: True for lastLac, f in lastLacFreq4G.items()}
        self.menu4GLastLac = UiUtils.createDynamicMenu(self.pandasUtils.lastLacFrecuenciaSeries(self.pandasUtils.allData4G))
        self.pushButtonLastLac4G.setMenu(self.menu4GLastLac)
        self.menu4GLastLac.triggered.connect(self.fnProcesaMenuLastLac4G)

        # self.fnAplicaFiltros()
        # self.fillTableWidget(self.tableWidgetVerDatosFiltrados, self.pandasUtils.tempDf)

    def fnGuardarTablaFiltrada(self):
        # print("Fn procesa guardar datos tabla filtrada")
        def saveTable(msg):
            self.pandasUtils.saveToExcelFile(
            self.pandasUtils.tempDf.sort_values(by="HITS"), filePath, False, self.saveProcessFinished)
            self.overlay.killAndHide()
        filePath = self.saveFileDialog()
        if(filePath):
            self.overlay.show()
            self.fnAplicaFiltros(saveTable)


        # print("Fn generacion del reporte")

    def saveProcessFinished(self):
        UiUtils.showInfoMessage(parent=self, title="Guardado de archivos",
                                description=f"Se guardo el archivo de la tabla filtrada correctamente.")

    def saveFileDialog(self):
        """
        Opens a save file dialog and returns the path to the file
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(
            self, "Guardar archivo", "", "Excel Files (*.xlsx)", options=options)
        return fileName

    def fnProcesaMenuLastLac2G(self, action):
        # print(f"Procesamiento menu de 2g antes: {action.data()} valores filtro 2g last lac {self.filtros2G.valoresLastLac}")
        self.filtros2G.valoresLastLac[float(action.data())] = not self.filtros2G.valoresLastLac[float(action.data())]
        # print(f"Procesamiento menu de 2g despues: {action.data()} valores filtro 2g last lac {self.filtros2G.valoresLastLac}")

    def fnProcesaMenuLastLac3G(self, action):
        # print(f"Procesamiento menu de 3g antes: {action.data()} valores filtro 3g last lac {self.filtros3G.valoresLastLac}")
        self.filtros3G.valoresLastLac[float(action.data())] = not self.filtros3G.valoresLastLac[float(action.data())]

    def fnProcesaMenuLastLac4G(self, action):
        # print(f"Procesamiento menu de 4g antes: {action.data()} valores filtro 4g last lac {self.filtros4G.valoresLastLac}")
        self.filtros4G.valoresLastLac[float(action.data())] = not self.filtros4G.valoresLastLac[float(action.data())]

    def fnProcesaLimpiezaRat(self, rat: str):
        if rat == "2G":
            for action in self.menu2GLastLac.actions():
                action.setChecked(True)
            # print("Limpieza 2g")
        if rat == "3G":
            for action in self.menu3GLastLac.actions():
                action.setChecked(True)
            # print("Limpieza 3g")
        if rat == "4G":
            for action in self.menu4GLastLac.actions():
                action.setChecked(True)
            # print("Limpieza 4g")

    def fnProcesaDeseleccion(self, tableWidget: QTableWidget):
        tableWidget.selectionModel().clearSelection()

    def fillTableWidget(self, qtable: QTableWidget, df: pd.DataFrame = None):
        # TODO: Hacerla general recibiendo el widget
        # Limpiar contenidos de tabla
        headerList = tuple(df.columns.values)
        qtable.clearContents()
        qtable.setColumnCount(len(headerList))
        qtable.setHorizontalHeaderLabels(headerList)
        # self.qtable.horizontalHeader().setStretchLastSection(True)
        qtable.horizontalHeader(
        ).setSectionResizeMode(QHeaderView.Stretch)
        rowCount = 0
        for row in df.itertuples():
            # Sets the number of rows in this table's model to rows. If this is less than rowCount(),
            # the data in the unwanted rows is discarded.
            qtable.setRowCount(rowCount+1)
            for i, columnName in enumerate(headerList):
                # val = QTableWidgetItem(row._asdict()[str(columnName)])
                val = QTableWidgetItem(str(row._asdict()[columnName]))
                qtable.setItem(rowCount, i, val)
            rowCount += 1

    def menuContextualDatosFiltrados(self, posicion):
        indices = self.tableWidgetVerDatosFiltrados.selectedIndexes()
        if indices:
            menu = QMenu()

            # To make all the actions belong to a group
            itemsGrupo = QActionGroup(self)
            itemsGrupo.setExclusive(True)

            """
            Acciones: imsis, ver horario (Hits), ver channel, Operadores
            """
            actionImsis = QAction("Ver IMSIS asociados", itemsGrupo)
            actionImsis.setData(VentanaFiltros.ACTION_IMSIS)
            menu.addAction(actionImsis)

            actionFechas = QAction("Ver fechas y hits asociados", itemsGrupo)
            actionFechas.setData(VentanaFiltros.ACTION_FECHAS)
            menu.addAction(actionFechas)

            actionCanales = QAction("Ver canales asociados asociados", itemsGrupo)
            actionCanales.setData(VentanaFiltros.ACTION_CANALES)
            menu.addAction(actionCanales)

            actionOps = QAction("Ver operadores asociados", itemsGrupo)
            actionOps.setData(VentanaFiltros.ACTION_OPERADORES)
            menu.addAction(actionOps)

            itemsGrupo.triggered.connect(self.fnProcesaMenuContextual)

            menu.exec(self.tableWidgetVerDatosFiltrados.viewport().mapToGlobal(posicion))

    def fnProcesaMenuContextual(self, action):
        accion = action.data()
        try:
            currentTableItem = int(self.tableWidgetVerDatosFiltrados.currentItem().text()) if len(self.tableWidgetVerDatosFiltrados.currentItem().text()) > 0 else None
        except Exception as e:
            print(e)
            currentTableItem = None
        # print(f"Procesa menu contetual {accion}")
        if accion == VentanaFiltros.ACTION_IMSIS:
            # print("Accion imsis")
            dfImei = self.pandasUtils.filterDfByEmai(self.pandasUtils.getAllData(), currentTableItem)
            dfAgrupado = self.pandasUtils.getGroupedByEmaisIMSIS(dfImei)
            self.fillTableWidget(self.tableWidgetMostrarSeleccion, dfAgrupado)
        elif accion == VentanaFiltros.ACTION_FECHAS:
            # print("Accion fechas")
            dfImei = self.pandasUtils.filterDfByEmai(self.pandasUtils.getAllData(), currentTableItem)
            dfAgrupado = self.pandasUtils.getGroupedByEmaisDates(dfImei)
            self.fillTableWidget(self.tableWidgetMostrarSeleccion, dfAgrupado)
        elif accion == VentanaFiltros.ACTION_CANALES:
            # print("Accion canales")
            dfImei = self.pandasUtils.filterDfByEmai(self.pandasUtils.getAllData(), currentTableItem)
            dfAgrupado = self.pandasUtils.getGroupedByEmaisCanales(dfImei)
            self.fillTableWidget(self.tableWidgetMostrarSeleccion, dfAgrupado)
        elif accion == VentanaFiltros.ACTION_OPERADORES:
            dfImei = self.pandasUtils.filterDfByEmai(self.pandasUtils.getAllData(), currentTableItem)
            dfAgrupado = self.pandasUtils.getGroupedByEmaisOps(dfImei)
            self.fillTableWidget(self.tableWidgetMostrarSeleccion, dfAgrupado)
            # print("Accion operadores")

    def fnMostrarDatosGenerales(self):
        self.parent().show()
        self.hide()

    def fnProcesaBusquedaDatos(self):
        # print("Empieza busqueda de datos")
        datoBuscar = self.textEditBuscarDatos.toPlainText()
        # print(f"Dato buscar {datoBuscar}")
        if(len(datoBuscar) > 0 and self.pandasUtils.isFloat(datoBuscar)):
            df = self.fnAplicaFiltrosNoGroupingReturns()
            df = self.pandasUtils.filterDfByEmai(df, datoBuscar)
            df = self.pandasUtils.getGroupedByEmais(df)
            self.fillTableWidget(self.tableWidgetVerDatosFiltrados, df)

    def fnMuestraVentanaAnalisis(self):
        self.hide()
        ventanaAnalisis = VentanaAnalisisDatos(self, self.pandasUtils, self.pandasUtils.tempDf)
        ventanaAnalisis.show()
        # print(f"Fn muestra ventana analisis de datos")

    def fnGeneraGraficaDatosFiltrados(self):
        def generaGrafica(msg):
            series = self.pandasUtils.hitsByDate(self.fnAplicaFiltrosNoGroupingReturns())
            plotWindow = PlotWindowBars(self)
            plotWindow.plot(x=pd.to_datetime(series.index), y=series.values, xLabel='DATE', yLabel='HITS')
            plotWindow.show()
            self.overlay.killAndHide()
        # print(f"Dimesiones df a graficar {self.pandasUtils.tempDf}")
        ventanaGrafica = PlotWindow(self)
        # Get the x and y values of current stuff
        self.overlay.show()
        self.fnAplicaFiltros(generaGrafica)

    def fnProcesaObtenerDatosFiltrados(self):
        """ Setea todos los valores de la interfaz en los campos de instancia"""
        # Valores de TA
        valores2g = self.lineEditValorRangosTA2G.text().split(',')
        self.filtros2G.valoresTA = set(map(int, valores2g)) if self.pandasUtils.checkInts(valores2g) else []

        valores3g = self.lineEditValorRangosTA3G.text().split(',')
        self.filtros3G.valoresTA = set(map(int, valores3g)) if self.pandasUtils.checkInts(valores3g) else []

        valores4g = self.lineEditValorRangosTA4G.text().split(',')
        self.filtros4G.valoresTA = set(map(int, valores4g)) if self.pandasUtils.checkInts(valores4g) else []
        # Hits minimos
        self.filtros2G.hitsMinimos = int(self.lineEditValorHitsMinimos2G.text()) if self.lineEditValorHitsMinimos2G.text().isnumeric() else 0
        self.filtros3G.hitsMinimos = int(self.lineEditValorHitsMinimos3G.text()) if self.lineEditValorHitsMinimos3G.text().isnumeric() else 0
        self.filtros4G.hitsMinimos = int(self.lineEditValorHitsMinimos4G.text()) if self.lineEditValorHitsMinimos4G.text().isnumeric() else 0
        # Toma de valores de ms power
        self.filtros2G.msPowerInicial = float(self.lineEditValorRangoInicialMSPOWER2G.text(
        )) if self.filtros2G.tomarMsPower and self.pandasUtils.isFloat(self.lineEditValorRangoInicialMSPOWER2G.text()) else None
        self.filtros2G.msPowerFinal = float(self.lineEditValorRangoFinalMSPOWER2G.text(
        )) if self.filtros2G.tomarMsPower and self.pandasUtils.isFloat(self.lineEditValorRangoFinalMSPOWER2G.text()) else None
        self.filtros3G.msPowerInicial = float(self.lineEditValorRangoInicialMSPOWER3G.text(
        )) if self.filtros3G.tomarMsPower and self.pandasUtils.isFloat(self.lineEditValorRangoInicialMSPOWER3G.text()) else None
        self.filtros3G.msPowerFinal = float(self.lineEditValorRangoFinalMSPOWER3G.text(
        )) if self.filtros3G.tomarMsPower and self.pandasUtils.isFloat(self.lineEditValorRangoFinalMSPOWER3G.text()) else None
        self.filtros4G.msPowerInicial = float(self.lineEditValorRangoInicialMSPOWER4G.text(
        )) if self.filtros4G.tomarMsPower and self.pandasUtils.isFloat(self.lineEditValorRangoInicialMSPOWER4G.text()) else None
        self.filtros4G.msPowerFinal = float(self.lineEditValorRangoFinalMSPOWER4G.text(
        )) if self.filtros4G.tomarMsPower and self.pandasUtils.isFloat(self.lineEditValorRangoFinalMSPOWER4G.text()) else None


        def obtencion(msg):
            self.fillTableWidget(self.tableWidgetVerDatosFiltrados, self.pandasUtils.tempDf)
            self.overlay.killAndHide()
        self.overlay.show()
        self.fnAplicaFiltros(obtencion)

    def fnAplicaFiltrosNoGroupingReturns(self):
        # Procesa de aplicacion de filtros
        dfs = list()
        if self.filtros2G.selected:
            df2G = self.pandasUtils.tiempoAvanceFilterTA(self.pandasUtils.allData2G, self.filtros2G.valoresTA)
            df2GMsPower = self.pandasUtils.msPowerRangeFilter(df2G, self.filtros2G.msPowerInicial, self.filtros2G.msPowerFinal)
            df2GLastLac = self.pandasUtils.filterDfByColumnValues(df2GMsPower, 'LAST_LAC', self.filtros2G.valoresLastLac)
            df2GHitsMin = self.pandasUtils.filterByHitsGrouping(df2GLastLac, 'IMEI', self.filtros2G.hitsMinimos)

            dfs.append(df2GHitsMin)
        if self.filtros3G.selected:
            df3G = self.pandasUtils.tiempoAvanceFilterTA(self.pandasUtils.allData3G, self.filtros3G.valoresTA)
            df3GMsPower = self.pandasUtils.msPowerRangeFilter(df3G, self.filtros3G.msPowerInicial, self.filtros3G.msPowerFinal)
            df3GLastLac = self.pandasUtils.filterDfByColumnValues(df3GMsPower, 'LAST_LAC', self.filtros3G.valoresLastLac)
            df3GHitsMin = self.pandasUtils.filterByHitsGrouping(df3GLastLac, 'IMEI', self.filtros3G.hitsMinimos)
            dfs.append(df3GHitsMin)
        if self.filtros4G.selected:
            df4G = self.pandasUtils.tiempoAvanceFilterTA(self.pandasUtils.allData4G, self.filtros4G.valoresTA)
            df4GMsPower = self.pandasUtils.msPowerRangeFilter(df4G, self.filtros4G.msPowerInicial, self.filtros4G.msPowerFinal)
            df4GLastLac = self.pandasUtils.filterDfByColumnValues(df4GMsPower, 'LAST_LAC', self.filtros4G.valoresLastLac)
            df4GHitsMin = self.pandasUtils.filterByHitsGrouping(df4GLastLac, 'IMEI', self.filtros4G.hitsMinimos)
            dfs.append(df4GHitsMin)
        # Empieza a agrupar todo
        return self.pandasUtils.concatDfs(dfs)

    def fnAplicacionFiltrosFinished(self, msg):
        self.overlay.killAndHide()
        self.fillTableWidget(self.tableWidgetVerDatosFiltrados, self.pandasUtils.tempDf)
        UiUtils.showInfoMessage(parent=self, title="Resultado de aplicación de filtros",
                                description=msg)
        print(f"Se termino la aplicación de filtros {msg}")

    def fnAplicaFiltros(self, callback):
        # Procesa de alicacion de filtros
        self.pandasUtils.fnAplicaFiltros(self.filtros2G, self.filtros3G, self.filtros4G, callback)
        # dfs = list()
        # if self.filtros2G.selected:
        #     df2G = self.pandasUtils.tiempoAvanceFilterTA(self.pandasUtils.allData2G, self.filtros2G.valoresTA)
        #     df2GMsPower = self.pandasUtils.msPowerRangeFilter(df2G, self.filtros2G.msPowerInicial, self.filtros2G.msPowerFinal)
        #     df2GLastLac = self.pandasUtils.filterDfByColumnValues(df2GMsPower, 'LAST_LAC', self.filtros2G.getSelectedLastLacValues())
        #     df2GHitsMin = self.pandasUtils.filterByHitsGrouping(df2GLastLac, 'IMEI', self.filtros2G.hitsMinimos)
        #     dfs.append(df2GHitsMin)
        # if self.filtros3G.selected:
        #     df3G = self.pandasUtils.tiempoAvanceFilterTA(self.pandasUtils.allData3G, self.filtros3G.valoresTA)
        #     df3GMsPower = self.pandasUtils.msPowerRangeFilter(df3G, self.filtros3G.msPowerInicial, self.filtros3G.msPowerFinal)
        #     df3GLastLac = self.pandasUtils.filterDfByColumnValues(df3GMsPower, 'LAST_LAC', self.filtros3G.getSelectedLastLacValues())
        #     df3GHitsMin = self.pandasUtils.filterByHitsGrouping(df3GLastLac, 'IMEI', self.filtros3G.hitsMinimos)
        #     dfs.append(df3GHitsMin)
        # if self.filtros4G.selected:
        #     df4G = self.pandasUtils.tiempoAvanceFilterTA(self.pandasUtils.allData4G, self.filtros4G.valoresTA)
        #     df4GMsPower = self.pandasUtils.msPowerRangeFilter(df4G, self.filtros4G.msPowerInicial, self.filtros4G.msPowerFinal)
        #     df4GLastLac = self.pandasUtils.filterDfByColumnValues(df4GMsPower, 'LAST_LAC', self.filtros4G.getSelectedLastLacValues())
        #     df4GHitsMin = self.pandasUtils.filterByHitsGrouping(df4GLastLac, 'IMEI', self.filtros4G.hitsMinimos)
        #     dfs.append(df4GHitsMin)
        # # Empieza a agrupar todo
        # newDf = self.pandasUtils.concatDfs(dfs)
        # self.pandasUtils.setTempDf(self.pandasUtils.getGroupedByEmais(newDf))
        # if(self.pandasUtils.tempDf.shape[0]>0):
        #     self.pandasUtils.setTempDf(self.pandasUtils.tempDf.sort_values(by="HITS", ascending=False))

    def fnProcesaTomaDatosMsPower(self):
        self.filtros2G.tomarMsPower = self.checkBoxTomarDatoMSPower2G.isChecked()
        self.filtros3G.tomarMsPower = self.checkBoxTomarDatoMSPower3G.isChecked()
        self.filtros4G.tomarMsPower = self.checkBoxTomarDatoMSPower4G.isChecked()
        # Setear a None los valores de los rangos para que al hacer la llamada se devuelve el df sin consultar
        if self.filtros2G.tomarMsPower is False:
            self.filtros2G.msPowerInicial = None
            self.filtros2G.msPowerFinal = None
        if self.filtros3G.tomarMsPower is False:
            self.filtros3G.msPowerInicial = None
            self.filtros3G.msPowerFinal = None
        if self.filtros4G.tomarMsPower is False:
            self.filtros4G.msPowerInicial = None
            self.filtros4G.msPowerFinal = None

        # print(f"Fn procesa toma datos ms power {self.filtros2G} {self.filtros3G} {self.filtros4G}")

    def fnProcesaSeleccionRat(self, state):
        self.filtros2G.selected = self.checkBox2G.isChecked()
        self.filtros3G.selected = self.checkBox3G.isChecked()
        self.filtros4G.selected = self.checkBox4G.isChecked()
        if not self.filtros2G.selected and not self.filtros3G.selected and not self.filtros4G.selected:
            self.checkBox2G.setChecked(True)
            self.checkBox3G.setChecked(True)
            self.checkBox4G.setChecked(True)
            self.filtros2G.selected = self.checkBox2G.isChecked()
            self.filtros3G.selected = self.checkBox3G.isChecked()
            self.filtros4G.selected = self.checkBox4G.isChecked()
        # print(f"Rats seleccion 2g {self.filtros2G.selected} 3g {self.filtros3G.selected} 4g {self.filtros4G.selected}")
        self.seteaValoresTA()

    def seteaValoresTA(self):
        if self.checkBox2G.isChecked():
            self.filtros2G.valoresTA = {0, 1}
            self.lineEditValorRangosTA2G.setText(",".join(map(str, list(self.filtros2G.valoresTA))))

        if self.checkBox3G.isChecked():
            self.filtros3G.valoresTA = {0, 1, 2}
            self.lineEditValorRangosTA3G.setText(",".join(map(str, list(self.filtros3G.valoresTA))))

        if self.checkBox4G.isChecked():
            self.filtros4G.valoresTA = {0, 1, 2, 3, 4, 5, 6}
            self.lineEditValorRangosTA4G.setText(",".join(map(str, list(self.filtros4G.valoresTA))))


    def resizeEvent(self, event):
        self.overlay.resize(event.size())
        event.accept()

if(__name__ == "__main__"):
    app = QApplication(sys.argv)
    ventanaFiltros = VentanaFiltros()
    ventanaFiltros.show()
    sys.exit(app.exec())