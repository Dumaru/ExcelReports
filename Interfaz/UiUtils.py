import sys
from PyQt5.QtWidgets import QMessageBox, QApplication
def showInfoMessage(parent=None, title:str ="", description: str="")->QMessageBox:
    msb = QMessageBox()
    msb.setIcon(QMessageBox.Information)
    msb.setWindowTitle(title)
    msb.setText(description)
    # Executes and returns the status
    msb.exec()

if(__name__=="__main__"):
    app = QApplication(sys.argv)
    sys.exit(showInfoMessage(title="SJNDFK", description="sdjfnsdfjnksdfnjksdfjknds"))