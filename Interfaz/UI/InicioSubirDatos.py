# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'InicioSubirDatos.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(824, 707)
        MainWindow.setStyleSheet("\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:1 rgba(85, 125, 255, 255));")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 15, 5, 1, 1)
        self.pushButtonAnadirArchivo = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonAnadirArchivo.setMaximumSize(QtCore.QSize(16777215, 48))
        font = QtGui.QFont()
        font.setFamily("Corbel")
        font.setPointSize(11)
        self.pushButtonAnadirArchivo.setFont(font)
        self.pushButtonAnadirArchivo.setStyleSheet("background-color: rgb(85, 170, 255);\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(63, 117, 194, 200), stop:1 rgba(255, 255, 255, 255));\n"
"\n"
"")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../Recursos/icons8-añadir-libro-100.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonAnadirArchivo.setIcon(icon)
        self.pushButtonAnadirArchivo.setIconSize(QtCore.QSize(30, 30))
        self.pushButtonAnadirArchivo.setObjectName("pushButtonAnadirArchivo")
        self.gridLayout.addWidget(self.pushButtonAnadirArchivo, 7, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 15, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 3, 3, 1, 1)
        self.pushButtonEliminar = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Corbel")
        font.setPointSize(11)
        self.pushButtonEliminar.setFont(font)
        self.pushButtonEliminar.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0.517413 rgba(55, 117, 206, 229), stop:1 rgba(255, 255, 255, 255));\n"
"\n"
"")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../Recursos/icons8-eliminar-400.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonEliminar.setIcon(icon1)
        self.pushButtonEliminar.setIconSize(QtCore.QSize(40, 40))
        self.pushButtonEliminar.setObjectName("pushButtonEliminar")
        self.gridLayout.addWidget(self.pushButtonEliminar, 7, 3, 1, 1)
        self.listWidgetListaArchivos = QtWidgets.QListWidget(self.centralwidget)
        self.listWidgetListaArchivos.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-color: rgb(0, 0, 0);")
        self.listWidgetListaArchivos.setAutoScrollMargin(23)
        self.listWidgetListaArchivos.setObjectName("listWidgetListaArchivos")
        self.gridLayout.addWidget(self.listWidgetListaArchivos, 6, 1, 1, 5)
        self.pushButtonCargarDatos = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Corbel")
        font.setPointSize(11)
        self.pushButtonCargarDatos.setFont(font)
        self.pushButtonCargarDatos.setStyleSheet("background-color: rgb(85, 170, 255);\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0.517413 rgba(55, 117, 206, 229), stop:1 rgba(255, 255, 255, 255));")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("../Recursos/upload.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonCargarDatos.setIcon(icon2)
        self.pushButtonCargarDatos.setIconSize(QtCore.QSize(40, 40))
        self.pushButtonCargarDatos.setObjectName("pushButtonCargarDatos")
        self.gridLayout.addWidget(self.pushButtonCargarDatos, 7, 4, 1, 1)
        self.pushButtonMostrarDatos = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonMostrarDatos.setMaximumSize(QtCore.QSize(16777215, 16777213))
        font = QtGui.QFont()
        font.setFamily("Corbel")
        font.setPointSize(11)
        self.pushButtonMostrarDatos.setFont(font)
        self.pushButtonMostrarDatos.setStyleSheet("\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0.517413 rgba(55, 117, 206, 229), stop:1 rgba(255, 255, 255, 255));\n"
"")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/newPrefix/icons8-ver-80.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonMostrarDatos.setIcon(icon3)
        self.pushButtonMostrarDatos.setIconSize(QtCore.QSize(40, 40))
        self.pushButtonMostrarDatos.setObjectName("pushButtonMostrarDatos")
        self.gridLayout.addWidget(self.pushButtonMostrarDatos, 3, 5, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 8, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setMaximumSize(QtCore.QSize(167777, 167777))
        self.label_2.setStyleSheet("image: url(:/newPrefix/Logo.png);")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 3, 2)
        self.verticalLayout.addLayout(self.gridLayout)
        self.gridLayout_2.addLayout(self.verticalLayout, 1, 1, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem3, 2, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 824, 26))
        self.menubar.setObjectName("menubar")
        self.menuArchivo = QtWidgets.QMenu(self.menubar)
        self.menuArchivo.setObjectName("menuArchivo")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionAbrir = QtWidgets.QAction(MainWindow)
        self.actionAbrir.setObjectName("actionAbrir")
        self.actionNueva_Ventana = QtWidgets.QAction(MainWindow)
        self.actionNueva_Ventana.setObjectName("actionNueva_Ventana")
        self.actionGuardar = QtWidgets.QAction(MainWindow)
        self.actionGuardar.setObjectName("actionGuardar")
        self.actionGuardar_Como = QtWidgets.QAction(MainWindow)
        self.actionGuardar_Como.setObjectName("actionGuardar_Como")
        self.actionSalir = QtWidgets.QAction(MainWindow)
        self.actionSalir.setObjectName("actionSalir")
        self.menuArchivo.addAction(self.actionAbrir)
        self.menuArchivo.addAction(self.actionNueva_Ventana)
        self.menuArchivo.addAction(self.actionGuardar)
        self.menuArchivo.addAction(self.actionGuardar_Como)
        self.menuArchivo.addAction(self.actionSalir)
        self.menubar.addAction(self.menuArchivo.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButtonAnadirArchivo.setText(_translate("MainWindow", "Añadir Archivos"))
        self.label.setText(_translate("MainWindow", "Lista de Archivos"))
        self.pushButtonEliminar.setWhatsThis(_translate("MainWindow", "<html><head/><body><p><img src=\":/newPrefix/Iocom png.png\"/></p></body></html>"))
        self.pushButtonEliminar.setText(_translate("MainWindow", "Eliminar Archivo"))
        self.pushButtonCargarDatos.setText(_translate("MainWindow", "Cargar Datos"))
        self.pushButtonMostrarDatos.setText(_translate("MainWindow", "Ver Datos"))
        self.menuArchivo.setTitle(_translate("MainWindow", "Archivo"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionAbrir.setText(_translate("MainWindow", "Abrir"))
        self.actionNueva_Ventana.setText(_translate("MainWindow", "Nueva Ventana"))
        self.actionGuardar.setText(_translate("MainWindow", "Guardar"))
        self.actionGuardar_Como.setText(_translate("MainWindow", "Guardar Como "))
        self.actionSalir.setText(_translate("MainWindow", "Salir "))
import Re_rc
import qrc_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
