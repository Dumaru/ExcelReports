import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFileDialog, QAbstractItemView,
                             QAction, QActionGroup, QTableWidgetItem, QTableWidget, QHeaderView, QMenu)
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
import pandas as pd
from PandasUtils import PandasDataLoader


class VentanaAnalisisHorario(QMainWindow):
    RANGO_DIA = 0
    RANGO_MADRUGADA = 0
    RANGO_MANANA = 0
    RANGO_TARDE = 0
    RANGO_NOCHE = 0
    def __init__(self, parent=None, pandasUtilsInstance=None, data: pd.DataFrame = None):
        super(VentanaAnalisisHorario, self).__init__(parent)
        # State fields
        self.fromDate = None
        self.toDate = None
        self.fromTime = None
        self.toTime = None
        self.pandasUtils = pandasUtilsInstance if pandasUtilsInstance is not None else PandasDataLoader.getInstance()
        self.datosCombo = []
        self.data = data
        self.rangoSeleccionadoIndex = None
        self.viendoMenores = False
        self.valorFiltro = None
        # UI
        loadUi('UI/VistaDetalleHoras.ui', self)
        self.setupUi()

    def setupUi(self):
        # Principales
        self.pushButtonVerDatosTablaFiltrada.clicked.connect(
            self.fnVerDatosTablaHorario)
        self.pushButtonGraficarDatosTablaFiltrada.clicked.connect(
            self.fnGraficarDatosTabla)
        # Estaticos
        self.pushButtonVerDatosEstaticos.clicked.connect(
            self.fnVerDatosEstaticosTablaHorario)
        self.setearValoresEstaticos()
        self.pushButtonGraficarDatosEstaticos.clicked.connect(
            self.fnGraficarDatosEstaticosTabla)
        # Action
        self.actionVolverDatos_General.triggered.connect(
            self.fnMuestraVentanaGeneral)
        self.comboBoxOrganizacionJornadas.currentIndexChanged.connect(self.seteaIndexRango)

        # Tabla estaticos
        # Seleccionar toda la fila
        self.tableWidgetMostrarDatosEstaticos.setSelectionBehavior(
            QAbstractItemView.SelectRows)
        # Seleccionar una fila a la vez
        self.tableWidgetMostrarDatosEstaticos.setSelectionMode(
            QAbstractItemView.SingleSelection)
        self.tableWidgetMostrarDatosEstaticos.horizontalHeader().setStretchLastSection(True)
        self.tableWidgetMostrarDatosEstaticos.setEditTriggers(
            QAbstractItemView.NoEditTriggers)
        self.tableWidgetMostrarDatosEstaticos.setAlternatingRowColors(True)
        # ---Tabla dinamicos---
        # Seleccionar toda la fila
        self.tableWidgetMostrarDatosFiltrados.setSelectionBehavior(
            QAbstractItemView.SelectRows)
        # Seleccionar una fila a la vez
        self.tableWidgetMostrarDatosFiltrados.setSelectionMode(
            QAbstractItemView.SingleSelection)
        self.tableWidgetMostrarDatosFiltrados.horizontalHeader().setStretchLastSection(True)
        self.tableWidgetMostrarDatosFiltrados.setEditTriggers(
            QAbstractItemView.NoEditTriggers)
        self.tableWidgetMostrarDatosFiltrados.setAlternatingRowColors(True)

    def seteaIndexRango(self, index):
        self.rangoSeleccionadoIndex = index
        print(f"Fn procesa rango seleccionado {self.rangoSeleccionadoIndex }")

    def fnMuestraVentanaGeneral(self):
        self.hide()
        self.parent().show()

    def fnAplicaRangosTablasDinamicas(self):
        filtroDates = self.pandasUtils.filtroDatetimes(
            self.data, self.fromDate, self.toDate)
        return self.pandasUtils.getGroupedByEmaisHorario(filtroDates)

    def fnAplicaRangosTablasEstaticas(self):
        self.setearValoresEstaticos()

        filtroDates = self.pandasUtils.filtroHoras(
            self.data, self.fromTime, self.toTime)
        return self.pandasUtils.getGroupedByEmaisHorario(filtroDates)

    def fnGraficarDatosTabla(self):
        self.setearFechas()
        self.fillTableWidget(
            self.tableWidgetMostrarDatosFiltrados, self.fnAplicaRangosTablasDinamicas()
        )
        print(f"Graficar tabla filtrada {self.fromDate} - {self.finalDate}")

    def fnVerDatosTablaHorario(self):
        self.setearFechas()
        self.fillTableWidget(self.tableWidgetMostrarDatosFiltrados,
                             self.fnAplicaRangosTablasDinamicas())

    def fnGraficarDatosEstaticosTabla(self):
        self.setearValoresEstaticos()

        self.fillTableWidget(
            self.tableWidgetMostrarDatosFiltrados, self.fnAplicaRangosTablasEstaticas()
        )
        print("Graficar tabla filtrada estaticos")

    def fnVerDatosEstaticosTablaHorario(self):
        self.setearValoresEstaticos()

        print(f"FnVerDatosTablaHorario estatico")

    def fillTableWidget(self, qtable: QTableWidget, df: pd.DataFrame = None):
        # TODO: Hacerla gfeneral {self.fromTime} {self.toTime} recibiendo el widget
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

    def setearValoresEstaticos(self):
        self.viendoMenores = True if self.comboBoxVerMayorMenor.currentIndex() == 1 else False
        self.valorFiltro = int(self.textEditValorFiltro.toPlainText()) if len(self.textEditValorFiltro.toPlainText())>0 else 1
        self.rangoSeleccionadoIndex = self.comboBoxOrganizacionJornadas.currentIndex()
        if self.rangoSeleccionadoIndex == VentanaAnalisisHorario.RANGO_DIA:
            self.fromTime = 0  
            self.toTime = 24
            print(f"Seteados {self.fromTime} {self.toTime}")
        if self.rangoSeleccionadoIndex == VentanaAnalisisHorario.RANGO_MADRUGADA:
            self.fromTime = 0
            self.toTime = 6
            print(f"Seteados {self.fromTime} {self.toTime}")
        if self.rangoSeleccionadoIndex == VentanaAnalisisHorario.RANGO_MANANA:
            self.fromTime = 6
            self.toTime = 12
            print(f"Seteados {self.fromTime} {self.toTime}")
        if self.rangoSeleccionadoIndex == VentanaAnalisisHorario.RANGO_TARDE:
            self.fromTime = 12
            self.toTime = 18
            print(f"Seteados {self.fromTime} {self.toTime}")
        if self.rangoSeleccionadoIndex == VentanaAnalisisHorario.RANGO_NOCHE:
            self.fromTime = 18
            self.toTime = 24
            print(f"Seteados {self.fromTime} {self.toTime}")
        print(f"Estaticos {self.fromTime} {self.toTime} menores {self.viendoMenores} valor {self.valorFiltro}")

    def setearFechas(self):
        dateTimeFormat = 'yyyy-MM-dd hh:mm:ss'
        pythonDateFormat = "%Y-%m-%d %X"
        try:
            self.fromDate = pd.to_datetime(self.dateTimeEditIngresoInicial.dateTime(
            ).toString(dateTimeFormat), format=pythonDateFormat)
            self.finalDate = pd.to_datetime(self.dateTimeEditIngresoFinal.dateTime(
            ).toString(dateTimeFormat), format=pythonDateFormat)
        except expression as identifier:
            self.fromDate = None
            self.finalDate = None


if(__name__ == "__main__"):
    app = QApplication(sys.argv)
    ventanaAnalisisHorario = VentanaAnalisisHorario()
    ventanaAnalisisHorario.show()
    sys.exit(app.exec())
