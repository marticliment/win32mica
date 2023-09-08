import ctypes

from win32mica import ApplyMica, MicaTheme, MicaStyle
from PySide6 import QtWidgets, QtCore

root = QtWidgets.QApplication()
app = QtWidgets.QMainWindow()
app.setAttribute(QtCore.Qt.WA_TranslucentBackground)
app.setWindowTitle("Qt Dark")
app.setGeometry(100, 100, 300, 200)
ApplyMica(app.winId(), MicaTheme.DARK, MicaStyle.DEFAULT)
app.show()

app2 = QtWidgets.QMainWindow()
app2.setAttribute(QtCore.Qt.WA_TranslucentBackground)
app2.setWindowTitle("Qt Light")
app2.setGeometry(400, 100, 300, 200)
ApplyMica(app2.winId(), MicaTheme.LIGHT, MicaStyle.DEFAULT)
app2.show()

app3 = QtWidgets.QMainWindow()
app3.setAttribute(QtCore.Qt.WA_TranslucentBackground)
app3.setWindowTitle("Qt Dark Alt")
app3.setGeometry(100, 330, 300, 200)
ApplyMica(app3.winId(), MicaTheme.DARK, MicaStyle.ALT)
app3.show()

app4 = QtWidgets.QMainWindow()
app4.setAttribute(QtCore.Qt.WA_TranslucentBackground)
app4.setWindowTitle("Qt Light Alt")
app4.setGeometry(400, 330, 300, 200)
ApplyMica(app4.winId(), MicaTheme.LIGHT, MicaStyle.ALT)
app4.show()

app5 = QtWidgets.QMainWindow()
app5.setAttribute(QtCore.Qt.WA_TranslucentBackground)
app5.setWindowTitle("Qt Auto")
app5.setGeometry(700, 100, 300, 200)

label = QtWidgets.QLabel("Change the system theme\nfrom the settings!")
def ApplyStyleSheet(theme):
    if theme == MicaTheme.DARK:
        label.setStyleSheet("color: white")
    else:
        label.setStyleSheet("color: black")

ApplyMica(app5.winId(), MicaTheme.AUTO, MicaStyle.DEFAULT, OnThemeChange=ApplyStyleSheet)
app5.show()
app5.setCentralWidget(label)

app6 = QtWidgets.QMainWindow()
app6.setAttribute(QtCore.Qt.WA_TranslucentBackground)
app6.setWindowTitle("Qt Auto Alt")
app6.setGeometry(700, 330, 300, 200)

label2 = QtWidgets.QLabel("Change the system theme\nfrom the settings!")
def ApplyStyleSheet(theme):
    if theme == MicaTheme.DARK:
        label2.setStyleSheet("color: white")
    else:
        label2.setStyleSheet("color: black")

ApplyMica(app6.winId(), MicaTheme.AUTO, MicaStyle.ALT, OnThemeChange=ApplyStyleSheet)
app6.show()
app6.setCentralWidget(label2)


root.exec()
