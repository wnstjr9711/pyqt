import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

form_class = uic.loadUiType("VPM.ui")[0]
MAX_MEMORY = 100


class MyWindow(QDialog, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('VPM')
        self.pid = 65
        self.process = dict()
        self.empty = [(MAX_MEMORY, 0)]
        self.pushButton.clicked.connect(self.btn_create)
        self.pushButton_2.clicked.connect(self.btn_release)
        self.pushButton_3.clicked.connect(self.integrate_adj)
        self.pushButton_4.clicked.connect(self.integrate_mem)

    def err_msg(self):
        err = QMessageBox(self)
        err.setWindowTitle('Error')
        err.setText('ValueError')
        err.show()

    def btn_create(self):
        try:
            m = int(self.textEdit.toPlainText())
            fit = False
            self.empty.sort(key=lambda x: x[1])
            for i in range(len(self.empty)):
                if self.empty[i][0] >= m:
                    fit = True
                    self.process[(m, self.empty[i][1])] = chr(self.pid)
                    if self.empty[i][0] - m != 0:
                        self.empty[i] = (self.empty[i][0] - m, self.empty[i][1] + m)
                    else:
                        self.empty.pop(i)
                    self.pid += 1
                    break
            if not fit:
                raise ValueError
            self.update_table()
        except ValueError:
            self.err_msg()
        finally:
            self.textEdit.clear()
        return

    def btn_release(self):
        try:
            pid = self.textEdit_2.toPlainText()
            if pid not in self.process.values():
                raise ValueError
            idx = [self.tableWidget.item(i, 3).text() for i in range(len(self.process) + len(self.empty))].index(pid)
            self.tableWidget.setItem(idx, 3, QTableWidgetItem('none'))
            temp = [k for k, v in self.process.items() if v == pid][0]
            self.empty.append(temp)
            self.process.pop(temp)
        except ValueError:
            self.err_msg()
        finally:
            self.textEdit_2.clear()
        return

    def set_ui(self):
        # 테이블 정보
        self.tableWidget.setColumnCount(5)
        col_header = ['partition', 'start address', 'size', 'current process ID', 'other field']
        self.tableWidget.setHorizontalHeaderLabels(col_header)
        self.update_table()
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()

    def update_table(self):
        self.tableWidget.setRowCount(len(self.process) + len(self.empty))
        for i in range(len(self.process) + len(self.empty)):
            self.tableWidget.setItem(i, 0, QTableWidgetItem('{}'.format(i + 1)))
            self.tableWidget.item(i, 0).setTextAlignment(0x0004 | 0x0080)
        for i, j in enumerate(sorted(list(self.process.items()) + [(i, 'none') for i in self.empty], key=lambda x: x[0][1])):
            self.tableWidget.setItem(i, 1, QTableWidgetItem('u + {}'.format(str(j[0][1]))))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(str(j[0][0])))
            self.tableWidget.setItem(i, 3, QTableWidgetItem(j[1]))

    def integrate_adj(self):
        self.empty.sort(key=lambda x: x[1])
        while {sum(i) for i in self.empty}.intersection({i[1] for i in self.empty}):
            for i in range(len(self.empty) - 1):
                if sum(self.empty[i]) == self.empty[i + 1][1]:
                    self.empty[i: i + 2] = [(self.empty[i][0] + self.empty[i + 1][0], self.empty[i][1])]
                    break
        self.update_table()

    def integrate_mem(self):
        start = 0
        process = sorted(self.process.items(), key=lambda x: x[0][1])
        for i in process:
            pid = self.process.pop(i[0])
            self.process[(i[0][0], start)] = pid
            start += i[0][0]
        self.empty = [(MAX_MEMORY - start, start)]
        self.update_table()


app = QApplication(sys.argv)
myWindow = MyWindow()
myWindow.set_ui()

myWindow.show()
app.exec()

