import sys
from PyQt5.QtWidgets import QMessageBox, QApplication, QMenu, QAction

def showInfoMessage(parent=None, title: str = "", description: str = "") -> QMessageBox:
    msb = QMessageBox()
    msb.setIcon(QMessageBox.Information)
    msb.setWindowTitle(title)
    msb.setText(description)
    # Executes and returns the status
    msb.exec()


def createMenu(menuItems) -> QMenu:
    menu = QMenu()
    for indice, item in enumerate(menuItems, start=0):
        accion = QAction(item, menu)
        accion.setCheckable(True)
        accion.setChecked(True)
        # To know later which indice was clicked we can use setData to get it later in the slot 
        accion.setData(str(item))
        menu.addAction(accion)
    return menu

if(__name__ == "__main__"):
    app = QApplication(sys.argv)
    sys.exit(showInfoMessage(title="SJNDFK",
                             description="sdjfnsdfjnksdfnjksdfjknds"))
