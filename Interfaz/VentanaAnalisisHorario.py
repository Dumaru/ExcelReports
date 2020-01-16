import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUi
import pandas as pd
class VentanaAnalisisHorario(QMainWindow):
    def __init__(self, parent=None):
        super(VentanaAnalisisHorario, self).__init__(parent)
        # State fields
        self.fromDate = ""
        self.toDate = ""
        self.datosCombo = []
        # UI
        loadUi('UI/VistaDetalleHoras.ui', self)
        self.setupUi()
    
    def setupUi(self):
        # Principales
        self.pushButtonVerDatosTablaFiltrada.clicked.connect(self.fnVerDatosTablaHorario)
        self.pushButtonGraficarDatosTablaFiltrada.clicked.connect(self.fnGraficarDatosTabla)
        # Estaticos
        self.pushButtonVerDatosEstaticos.clicked.connect(self.fnVerDatosEstaticosTablaHorario)
        self.pushButtonGraficarDatosEstaticos.clicked.connect(self.fnGraficarDatosEstaticosTabla)


    def fnGraficarDatosTabla(self):
        self.setearFechas()
        print(f"Graficar tabla filtrada {self.fromDate} - {self.finalDate}")

    def fnVerDatosTablaHorario(self):
        self.setearFechas()
        print(f"Graficar tabla filtrada {self.fromDate} - {self.finalDate}")
        print(f"fnVerDatosTablaHorario ")

    def setearFechas(self):
        dateTimeFormat = 'yyyy-MM-dd hh:mm:ss'
        pythonDateFormat = "%Y-%m-%d %X"
        self.fromDate = pd.to_datetime(self.dateTimeEditIngresoInicial.dateTime().toString(dateTimeFormat), format=pythonDateFormat)
        self.finalDate = pd.to_datetime(self.dateTimeEditIngresoFinal.dateTime().toString(dateTimeFormat), format=pythonDateFormat)

    def fnGraficarDatosEstaticosTabla(self):
        print("Graficar tabla filtrada estaticos")

    def fnVerDatosEstaticosTablaHorario(self):
        print(f"fnVerDatosTablaHorario estatico")



if(__name__=="__main__"):
    app = QApplication(sys.argv)
    ventanaAnalisisHorario = VentanaAnalisisHorario()
    ventanaAnalisisHorario.show()
    sys.exit(app.exec())
    



