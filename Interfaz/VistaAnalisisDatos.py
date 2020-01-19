import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFileDialog, QAbstractItemView,
                             QAction, QActionGroup, QTableWidgetItem, QTableWidget, QHeaderView, QMenu)
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
import pandas as pd
from PandasUtils import PandasDataLoader


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

    def fnGuardarIMSISIMEIS(self):
        print(f"Fn guardar IMSIS vs IMEIS")

    def fnGeneraReporte(self):
        print("Fn generacion del reporte")


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
