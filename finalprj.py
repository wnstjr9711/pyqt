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
        self.memory = ['0' for i in range(int(self.data[1]))]
        self.recently = ['0' for i in range(int(self.data[1]))]
        self.frequently = {i: 0 for i in range(int(self.data[2]) + 1)}
        self.page_absence = [True for i in range(self.length)]
        self.setWindowTitle('Virtual Storage Management')
        self.set_ui()

    def set_ui(self):
        self.label.setText('LRU(Least Recently Used)' if self.data[0] == '1' else 'LFU(Least Frequently Used)')
        self.label_3.setText(self.data[1])
        self.label_5.setText(self.data[2])

        self.tableWidget.setColumnCount(int(self.data[1]) + 2)
        self.tableWidget.setRowCount(self.length)
        head = {0: '참조 스트링', 1: '주기억장치 상태', int(self.data[1]) + 1: '페이지 부재\n발생 여부'}
        self.tableWidget.setVerticalHeaderLabels([''] + [str(i) for i in range(1, self.length)])
        self.tableWidget.setSpan(0, 1, 1, int(self.data[1]))
        for i, j in head.items():
            self.tableWidget.setItem(0, i, QTableWidgetItem(j))
        self.tableWidget.resizeColumnsToContents()
        w = self.width() / 2
        for i in range(1, int(self.data[1]) + 1):
            self.tableWidget.setColumnWidth(i, int(w / int(self.data[1])))
        self.tableWidget.resizeRowsToContents()

    def set_table(self):
        for i in range(1, self.length):
            cur = str(self.string[i - 1])
            self.tableWidget.setItem(i, 0, QTableWidgetItem(cur))
        self.lru() if self.data[0] == '1' else self.lfu()
        self.show_page_absence()
        self.show_absence_rate()

    def lfu(self):
        for i in range(1, self.length):
            cur = self.string[i - 1]
            f = list()
            for j in self.frequently.items():
                f.append(j) if str(j[0]) in self.memory else None
            change = str(min(f, key=lambda x: x[1])[0])
            if cur not in self.memory:
                self.memory[self.memory.index(change)] = cur
                self.page_absence[i] = False
            self.frequently[int(cur)] = self.frequently.pop(int(cur)) + 1
            for j in range(len(self.memory)):
                self.tableWidget.setItem(i, j + 1, QTableWidgetItem(self.memory[j] if self.memory[j] != '0' else None))

    def lru(self):
        for i in range(1, self.length):
            cur = self.string[i - 1]
            if cur in self.recently:
                self.recently.remove(cur)
            else:
                self.memory[self.memory.index(self.recently.pop(0))] = cur
                self.page_absence[i] = False
            self.recently.append(cur)
            for j in range(len(self.memory)):
                self.tableWidget.setItem(i, j + 1, QTableWidgetItem(self.memory[j] if self.memory[j] != '0' else None))

    def show_page_absence(self):
        for i in range(1, self.length):
            if not self.page_absence[i]:
                self.tableWidget.setItem(i, int(self.data[1]) + 1, QTableWidgetItem(str(self.page_absence[i])))

    def text_align_center(self):
        for i in range(self.tableWidget.rowCount()):
            for j in range(self.tableWidget.columnCount()):
                if self.tableWidget.item(i, j):
                    self.tableWidget.item(i, j).setTextAlignment(0x0004 | 0x0080)

    def show_absence_rate(self):
        self.label_7.setText('페이지 부재율: {:.3}%'.format(self.page_absence.count(False)/(self.length - 1) * 100))


app = QApplication(sys.argv)
myWindow = MyWindow()
myWindow.set_table()
myWindow.text_align_center()

myWindow.show()
app.exec()

