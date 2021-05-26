import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

form_class = uic.loadUiType("VSM.ui")[0]


class MyWindow(QDialog, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.data = open('input.txt', 'r').read().split()
        self.string = self.data[3:]
        self.length = len(self.string) + 1
        self.memory = {i: 0 for i in range(1, int(self.data[1]) + 1)}
        self.setWindowTitle('Virtual Storage Management')
        self.set_ui()

    def set_ui(self):
        self.label.setText('LRU(Least Recently Used)' if self.data[0] == 1 else 'LFU(Least Frequently Used)')
        self.label_3.setText(self.data[1])
        self.label_5.setText(self.data[2])

        self.tableWidget.setColumnCount(int(self.data[1]) + 2)
        self.tableWidget.setRowCount(self.length)
        head = {0: '참조 스트링', 1: '주기억장치 상태', int(self.data[1]) + 1: '페이지 부재\n발생 여부'}
        self.tableWidget.setVerticalHeaderLabels([''] + [str(i) for i in range(1, self.length)])
        self.tableWidget.setSpan(0, 1, 1, int(self.data[1]))
        for i, j in head.items():
            self.tableWidget.setItem(0, i, QTableWidgetItem(j))
            self.tableWidget.item(0, i).setTextAlignment(0x0004 | 0x0080)
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.setColumnWidth(1, int(self.width() / 6))
        self.tableWidget.setColumnWidth(2, int(self.width() / 6))
        self.tableWidget.setColumnWidth(3, int(self.width() / 6))
        self.tableWidget.resizeRowsToContents()

    def set_table(self):
        for i in range(1, self.length):
            self.tableWidget.setItem(i, 0, QTableWidgetItem(str(self.string[i - 1])))
            self.tableWidget.item(i, 0).setTextAlignment(0x0004 | 0x0080)
        print(self.memory)


app = QApplication(sys.argv)
myWindow = MyWindow()
myWindow.set_table()

myWindow.show()
app.exec()

