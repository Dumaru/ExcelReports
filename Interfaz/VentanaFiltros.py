from PyQt5.QtWidgets import QMainWindow

class VentanaFiltros(QMainWindow):
    def __init__(self, parent=None, pandasUtilsInstance=None):
        super(VentanaFiltros, self).__init__(parent)
        # State fields
        self.pandasUtils = pandasUtilsInstance if pandasUtilsInstance is not None else PandasDataLoader.getInstance()
        
        # UI
    
    def setupUi(self):
        pass
    