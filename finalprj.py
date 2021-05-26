import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

form_class = uic.loadUiType("VSM.ui")[0]


class MyWindow(QDialog, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Virtual Storage Management')

    def err_msg(self):
        err = QMessageBox(self)
        err.setWindowTitle('Error')
        err.setText('ValueError')
        err.show()

    def btn_create(self):
        return

    def btn_release(self):
        return


app = QApplication(sys.argv)
myWindow = MyWindow()
myWindow.show()
app.exec()

