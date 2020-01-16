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
        
        # UI
        loadUi('UI/VistaFiltros.ui', self)
        self.setupUi()

    def setupUi(self):
        pass


if(__name__=="__main__"):
    app = QApplication(sys.argv)
    ventanaFiltros = VentanaFiltros()
    ventanaFiltros.show()
    sys.exit(app.exec())
