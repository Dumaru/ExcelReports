import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFileDialog, QAbstractItemView,
                             QAction, QTableWidgetItem, QTableWidget, QHeaderView)
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
import pandas as pd
from PandasUtils import PandasDataLoader


class VentanaFiltros(QMainWindow):
    def __init__(self, parent=None, pandasUtilsInstance=None):
        super(VentanaFiltros, self).__init__(parent)
        # State fields
        self.pandasUtils = pandasUtilsInstance if pandasUtilsInstance is not None else PandasDataLoader.getInstance()
        self.msInicial = None
        self.msFinal = None
        self.ratsSeleccionados = {'2G': 1, '3G': 1, '4G': 1}
        self.valoresTA = set()
        self.tomarMsPower = False
        self.hitsMinimos = None
        self.lastLacValue = None
        # UI
        loadUi('UI/VistaFiltros.ui', self)
        self.setupUi()

    def setupUi(self):
        # Set rats based on the db
        # RAT Checkboxes setup
        # self.pandasUtils.setUniqueColumnValues(self.pandasUtils.allData, 'RAT')
        # self.ratsSeleccionados = {
            # rat: True for rat in self.pandasUtils.getUniqueColumnValues('RAT')
        # }
        self.checkBox2G.setChecked(True)
        self.checkBox3G.setChecked(True)
        self.checkBox4G.setChecked(True)
        self.checkBox2G.stateChanged.connect(self.fnProcesaSeleccionRat)
        self.checkBox3G.stateChanged.connect(self.fnProcesaSeleccionRat)
        self.checkBox4G.stateChanged.connect(self.fnProcesaSeleccionRat)
        self.seteaValoresTA()
        # Checkbox tomar datos
        self.checkBoxTomarDatoMSPower.stateChanged.connect(
            self.fnProcesaTomaDatosMsPower)
        # Push buttons signals
        self.pushButtonObtenerDatosFiltrados.clicked.connect(
            self.fnProcesaObtenerDatosFiltrados)
        self.pushButtonGenerarGraficas.clicked.connect(
            self.fnGeneraGraficaDatosFiltrados)
        self.pushButtonVerAnalisis.clicked.connect(
            self.fnMuestraVentanaAnalisis)
        self.pushButtonBuscarDatos.clicked.connect(self.fnProcesaBusquedaDatos)

        self.actionIrADatosGenerales.triggered.connect(
            self.fnMostrarDatosGenerales)


        # Tabla Last Lac
        # Seleccionar toda la fila
        self.tableWidgetDatosObtenidosLASTLAC.setSelectionBehavior(
            QAbstractItemView.SelectRows)
        # Seleccionar una fila a la vez
        self.tableWidgetDatosObtenidosLASTLAC.setSelectionMode(
            QAbstractItemView.SingleSelection)
        self.tableWidgetDatosObtenidosLASTLAC.horizontalHeader().setStretchLastSection(True)
        self.tableWidgetDatosObtenidosLASTLAC.setEditTriggers(
            QAbstractItemView.NoEditTriggers)
        self.tableWidgetDatosObtenidosLASTLAC.setAlternatingRowColors(True)

        self.fillTableWidget(self.tableWidgetDatosObtenidosLASTLAC,
                             self.pandasUtils.dfLastLacFrecuencia(self.pandasUtils.allData))
        # Tabla Datos filtrados
        self.tableWidgetVerDatosFiltrados.setContextMenuPolicy(
            Qt.CustomContextMenu)
        # Establece la funcion que crea el menu contextual y le pasa la posicion
        self.tableWidgetVerDatosFiltrados.customContextMenuRequested.connect(self.menuContextualDatosFiltrados)

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
            actionImsis.setData(1)
            menu.addAction()
            actionImsis = QAction("Ver fechas y hits asociados", itemsGrupo)
            actionImsis.setData(2)
            menu.addAction()
            actionImsis = QAction(
                "Ver canales asociados asociados", itemsGrupo)
            actionImsis.setData(3)
            menu.addAction()
            actionImsis = QAction("Ver operadores asociados", itemsGrupo)
            actionImsis.setData(4)
            menu.addAction()

            itemsGrupo.triggered.connect(self.copiarTableWidgetItem)

            menu.exec(self.tabla.viewport().mapToGlobal(posicion))

    def fnMostrarDatosGenerales(self):
        self.parent().show()
        self.hide()

    def fnProcesaBusquedaDatos(self):
        datoBuscar = self.textEditBusarDatos.toPlainText()
        if(len(datoBuscar) > 0):
            print(f"Fn procesa busqueda de datos {datoBuscar} ")

    def fnMuestraVentanaAnalisis(self):
        print(f"Fn muestra ventana analisis de datos")

    def fnGeneraGraficaDatosFiltrados(self):
        print(f"Fn genera grafica datos filtrados")

    def fnProcesaObtenerDatosFiltrados(self):
        self.setLastLacValue()
        if self.lastLacValue is not None:
            self.valoresTA = set(self.lineEditValorRangosTA.text().split(','))
            self.hitsMinimos = self.lineEditValorHitsMinimos.text()
            if self.tomarMsPower:
                self.msInicial = float(self.lineEditValorRangoInicialMSPOWER.text())
                self.msFinal = float(self.lineEditValorRangoFinalMSPOWER.text())
            print(
                f"Fn procesa obtener datos filtrados rats {self.ratsSeleccionados}",
                f"valores TA {self.valoresTA} min hits {self.hitsMinimos}",
                f"tomar ms power {self.tomarMsPower}  valores ms power {self.msInicial} {self.msFinal}",
                f"Last lasc {self.lastLacValue}")
        else:
            print("Debe seleccionar un valor de last lac")
    def setLastLacValue(self):
        filaSeleccionada = [dato.text() for dato in self.tableWidgetDatosObtenidosLASTLAC.selectedItems()]
        if(filaSeleccionada):
            print(f"Fila seleccionada {filaSeleccionada}")
            self.lastLacValue = float(filaSeleccionada[0])

    def fnProcesaTomaDatosMsPower(self):
        self.tomarMsPower = self.checkBoxTomarDatoMSPower.isChecked()
        print(f"Fn procesa toma datos ms power {self.tomarMsPower}")

    def fnProcesaSeleccionRat(self, state):
        self.ratsSeleccionados['2G'] = self.checkBox2G.isChecked()
        self.ratsSeleccionados['3G'] = self.checkBox3G.isChecked()
        self.ratsSeleccionados['4G'] = self.checkBox4G.isChecked()
        if not self.ratsSeleccionados['2G'] and not self.ratsSeleccionados['3G'] and not self.ratsSeleccionados['4G']:
            self.checkBox2G.setChecked(True)
            self.checkBox3G.setChecked(True)
            self.checkBox4G.setChecked(True)

        self.seteaValoresTA()
        print(f"Fn procesa seleccion {self.ratsSeleccionados}")

    def seteaValoresTA(self):
        if self.checkBox2G.isChecked():
            self.valoresTA = {0, 1}
        if self.checkBox3G.isChecked():
            self.valoresTA = {0, 1, 2}
        if self.checkBox4G.isChecked():
            self.valoresTA = {0, 1, 2, 3, 4, 5, 6}
        self.lineEditValorRangosTA.setText(",".join(map(str, list(self.valoresTA))))

    def fnAplicarFiltrosDf(self, df: pd.DataFrame):
        """ Aplica filtros de la UI y regresa el dataframe"""
        dfFiltrado = self.pandasUtils.tiempoAvanceFilterTA(
            self.pandasUtils.allData, list(self.valoresTA)
        )
        if self.tomarMsPower:
            dfFiltrado = self.pandasUtils.msPowerRangeFilter(
                self.pandasUtils.allData)



if(__name__ == "__main__"):
    app = QApplication(sys.argv)
    ventanaFiltros = VentanaFiltros()
    ventanaFiltros.show()
    sys.exit(app.exec())
