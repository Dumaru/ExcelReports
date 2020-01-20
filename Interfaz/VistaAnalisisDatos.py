import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFileDialog, QAbstractItemView,
                             QAction, QActionGroup, QTableWidgetItem, QTableWidget, QHeaderView, QMenu)
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
import pandas as pd
from PandasUtils import PandasDataLoader
import UiUtils
from PlotWindowBars import PlotWindowBars


class VentanaAnalisisDatos(QMainWindow):
    def __init__(self, parent=None, pandasUtilsInstance=None, data: pd.DataFrame = None):
        super(VentanaAnalisisDatos, self).__init__(parent)
        # State fields
        self.pandasUtils = pandasUtilsInstance if pandasUtilsInstance is not None else PandasDataLoader.getInstance()
        self.data = data
        # UI
        loadUi('UI/VistaAnalisisDatos.ui', self)
        self.setupUi()

    def setupUi(self):
        # Botones y signals
        print(f"Setup Ui")
        self.pushButtonGuardarReporte.clicked.connect(self.fnGeneraReporte)
        self.pushButtonGuardarDatosIMISISIMEI.clicked.connect(self.fnGuardarIMSISIMEIS)
        self.actionVer_Filtros.triggered.connect(self.fnMostrarVentanaFiltros)
        self.pushButtonGraficar.clicked.connect(self.fnGraficarHitsImei)
        # Llenar tabla con lo que venia del otro lado
        self.data.sort_values(by="HITS", inplace=True)
        self.fillTableWidget(self.tableWidgetVerDatosFiltrados, self.data)

    def fnGraficarHitsImei(self):
        print("Vista analisis datos se empieza a graficar")
        plotWindow = PlotWindowBars(self)
        df = self.data.sort_values(by="HITS", ascending=False)
        x = df['IMEI'].values
        y = df['HITS'].values
        print(f"X {x} Y{y}")
        plotWindow.plot(x=x, y=y, xLabel="IMEI", yLabel="HITS AMOUNT")
        plotWindow.show()
        print("Vista analisis datos se termina de graficar")


    def fnMostrarVentanaFiltros(self):
        self.hide()
        self.parent().show()

    def fnGuardarIMSISIMEIS(self):
        groupedIMSIS = self.pandasUtils.getGroupedByIMSI(self.pandasUtils.getAllData())
        self.fillTableWidget(self.tableWidgetVerDatosFiltrados, groupedIMSIS)
        # Guardar
        print(f"Fn guardar IMSIS vs IMEIS")

    def fnGeneraReporte(self):
        print("Fn procesa guardar datos reporte")
        filePath = self.saveFileDialog()
        if(filePath):
            self.pandasUtils.saveToExcelFile(
                self.data, filePath, False, self.saveProcessFinished)

        print("Fn generacion del reporte")

    def saveProcessFinished(self):
        UiUtils.showInfoMessage(parent=self, title="Guardado de archivos",
                                description=f"Se guardo el archivo de reporte correctamente.")

    def saveFileDialog(self):
        """
        Opens a save file dialog and returns the path to the file
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(
            self, "Guardar archivo", "", "Excel Files (*.xlsx)", options=options)
        return fileName

    def fnMuestraVentanaGeneral(self):
        self.hide()
        self.parent().show()

    def fillTableWidget(self, qtable: QTableWidget, df: pd.DataFrame = None):
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


if(__name__ == "__main__"):
    app = QApplication(sys.argv)
    ventanaAnalisisHorario = VentanaAnalisisDatos()
    ventanaAnalisisHorario.show()
    sys.exit(app.exec())
