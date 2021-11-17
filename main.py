import sys
import sqlite3
from PyQt5 import uic
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.con = sqlite3.connect('coffee.sqlite')
        self.cur = self.con.cursor()
        self.drawTable()

    def drawTable(self):
        self.tableWidget.setRowCount(0)
        result = list(self.cur.execute('SELECT * FROM info').fetchall())
        headings = [i[0] for i in self.cur.description]
        roastings = {i[0]: i[1] for i in list(self.cur.execute('SELECT * FROM roastings').fetchall())}
        tastes = {i[0]: i[1] for i in list(self.cur.execute('SELECT * FROM tastes').fetchall())}
        groundOrGrain = {i[0]: i[1] for i in list(self.cur.execute('SELECT * FROM groundOrGrain').fetchall())}
        result = [list(i[: 2]) + [roastings[i[2]], groundOrGrain[i[3]], tastes[i[4]]] + list(i[5:]) for i in result]
        self.tableWidget.setColumnCount(len(headings))
        self.tableWidget.setHorizontalHeaderLabels(['ID', 'Название', 'Степень обжарки', 'Молотый/в зёрнах',
                                                    'Вкус', 'Цена', 'Объём упаковки'])
        for row, i in enumerate(result):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for col, j in enumerate(i):
                self.tableWidget.setItem(row, col, QTableWidgetItem(str(j)))
        self.tableWidget.resizeColumnsToContents()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MyWidget()
    form.show()
    sys.exit(app.exec())