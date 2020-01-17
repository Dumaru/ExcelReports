import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUi
import pandas as pd
from PandasUtils import PandasDataLoader


class VentanaFiltros(QMainWindow):
    def __init__(self, parent=None, pandasUtilsInstance=None):
        super(VentanaFiltros, self).__init__(parent)
        # State fields
        self.pandasUtils = pandasUtilsInstance if pandasUtilsInstance is not None else PandasDataLoader.getInstance()
        self.taInicial = 0
        self.taFinal = 0
        self.ratsSeleccionados = {'2G': 1, '3G': 1, '4G':1}
        self.valoresTA = set()
        self.tomarMsPower = False
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
        
        # Checkbox tomar datos
        self.checkBoxTomarDatoMSPower.stateChanged.connect(self.fnProcesaTomaDatosMsPower)
        # Pusb buttons signals
        self.pushButtonObtenerDatosFiltrados.clicked.connect(self.fnProcesaObtenerDatosFiltrados)
        self.pushButtonGenerarGraficas.clicked.connect(self.fnGeneraGraficaDatosFiltrados)
        self.pushButtonVerAnalisis.clicked.connect(self.fnMuestraVentanaAnalisis)
        self.pushButtonBuscarDatos.clicked.connect(self.fnProcesaBusquedaDatos)
        
        self.actionIrADatosGenerales.triggered.connect(self.fnMostrarDatosGenerales)

    def fnMostrarDatosGenerales(self):
        self.parent().show()
        self.hide()
    def fnProcesaBusquedaDatos(self):
        datoBuscar = self.textEditBusarDatos.toPlainText()
        if(len(datoBuscar)>0):
            print(f"Fn procesa busqueda de datos {datoBuscar} ")
    def fnMuestraVentanaAnalisis(self):
        print(f"Fn muestra ventana analisis de datos")
    def fnGeneraGraficaDatosFiltrados(self):
        print(f"Fn genera grafica datos filtrados")

    def fnProcesaObtenerDatosFiltrados(self):
        print(f"Fn procesa obtener datos filtrados")

    def fnProcesaTomaDatosMsPower(self):
        self.tomarMsPower = self.checkBoxTomarDatoMSPower.isChecked()
        print(f"Fn procesa toma datos ms power {self.tomarMsPower}")

    def fnProcesaSeleccionRat(self, state):
        self.ratsSeleccionados['2G'] = self.checkBox2G.isChecked()
        self.ratsSeleccionados['3G'] = self.checkBox3G.isChecked()
        self.ratsSeleccionados['4G'] = self.checkBox4G.isChecked()
        if not self.ratsSeleccionados['2G'] and not self.ratsSeleccionados['3G'] and not self.ratsSeleccionados['4G'] :
            self.checkBox2G.setChecked(True)
            self.checkBox3G.setChecked(True)
            self.checkBox4G.setChecked(True)

        self.seteaValoresTA()
        print(f"Fn procesa seleccion {self.ratsSeleccionados}")

    def seteaValoresTA(self):
        if self.checkBox2G.isChecked():
            self.valoresTA = {0,1}
        if self.checkBox3G.isChecked():
            self.valoresTA = {0,1,2}
        if self.checkBox4G.isChecked():
            self.valoresTA = {0,1,2,3,4,5,6}
        self.updateTaUi()
    def updateTaUi(self):
        pass

    def fnAplicarFiltrosDf(self, df: pd.DataFrame):
        dfFiltrado = self.pandasUtils.tiempoAvanceFilterTA(
            self.pandasUtils.allData, list(self.valoresTA)
        )
        if self.tomarMsPower:
            dfFiltrado = self.pandasUtils.msPowerRangeFilter(self.pandasUtils.allData)

    def getTaValues(self):
        self.valoresTA = set(self.textEditTaValues.split(','))
if(__name__ == "__main__"):
    app = QApplication(sys.argv)
    ventanaFiltros = VentanaFiltros()
    ventanaFiltros.show()
    sys.exit(app.exec())
