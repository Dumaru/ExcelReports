import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi


class ExcelReportsInicio(QMainWindow):
    """
    Window class to load all the files from a directory
    """
    def __init__(self, parent=None):
        # Calls the super class to init all the values in the this object
        super(ExcelReportsInicio, self).__init__()
        loadUi("UI/InicioSubirDatos.ui", self)
    


if(__name__=="__main__"):
    # Instanciates a new QApplication with the given terminal parameters
    app=QApplication(sys.argv)
    inicioCarga = ExcelReportsInicio()
    inicioCarga.show()
    sys.exit(app.exec_())
