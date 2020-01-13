from PyQt5.QtWidgets import QMessageBox
def showInfoMessage(parent=None, title="", description=""):
    msb = QMessageBox()
    msb.setWindowTitle(title)
    msb.setText(description)
    msb.exec()

if(__name__="__main__"):
    showInfoMessage(title="SJNDFK", description="sdjfnsdfjnksdfnjksdfjknds")