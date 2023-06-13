import ctypes

try:
    import win32mica as mc
    from PySide6 import QtWidgets, QtCore
except ImportError:
    import os
    os.system("pip install win32mica PySide2")

root = QtWidgets.QApplication()
app = QtWidgets.QMainWindow()
app.setAttribute(QtCore.Qt.WA_TranslucentBackground)
app.setWindowTitle("Qt Dark")
app.setGeometry(100, 100, 300, 200)
mc.ApplyMica(app.winId(), mc.MICAMODE.DARK)
app.show()

app2 = QtWidgets.QMainWindow()
app2.setAttribute(QtCore.Qt.WA_TranslucentBackground)
app2.setWindowTitle("Qt Light")
app2.setGeometry(400, 100, 300, 200)
mc.ApplyMica(app2.winId(), mc.MICAMODE.LIGHT)
app2.show()

root.exec_()