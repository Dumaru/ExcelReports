import sys
from PyQt5.QtWidgets import QMessageBox, QApplication, QMenu, QAction

def showInfoMessage(parent=None,title: str = "", description: str = "") -> QMessageBox:
    msb = QMessageBox(parent=parent)
    msb.setIcon(QMessageBox.Information)
    msb.setWindowTitle(title)
    msb.setText(description)
    status = msb.exec()

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

def createDynamicMenu(menuItems: dict) -> QMenu:
    menu = QMenu()
    for key, value in menuItems.items():
        accion = QAction(str(key)+" Cantidad: "+str(value), menu)
        accion.setCheckable(True)
        accion.setChecked(True)
        # To know later which indice was clicked we can use setData to get it later in the slot 
        accion.setData(str(key))
        menu.addAction(accion)
    return menu


def fnAbrirDir():
        """
        Opens a folder dialog and returns the path to the folder
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileDir = str(QFileDialog.getExistingDirectory(
            self, "Selecciona una carpeta"))
        print(f"Files Folder {fileDir}")
        return fileDir

def saveFileDialog():
    """
    Opens a save file dialog and returns the path to the file
    """
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    fileName, _ = QFileDialog.getSaveFileName(self,"Guardar archivo","","All Files (*);;Text Files (*.txt)", options=options)
    if fileName:
        return fileName

if(__name__ == "__main__"):
    app = QApplication(sys.argv)
    sys.exit(showInfoMessage(title="SJNDFK",
                             description="sdjfnsdfjnksdfnjksdfjknds"))
