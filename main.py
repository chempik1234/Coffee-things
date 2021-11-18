import sys
import sqlite3
from PyQt5 import uic
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem,\
    QComboBox, QFormLayout, QHBoxLayout, QVBoxLayout, QSpinBox, QLabel


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.con = sqlite3.connect('coffee.sqlite')
        self.cur = self.con.cursor()
        self.second = None
        self.drawTable()
        self.pushButton.clicked.connect(self.addForm)
        self.pushButton_2.clicked.connect(self.addForm)

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

    def addForm(self):
        if self.second is None or (self.second and self.second.isHidden()):
            if self.sender().text() == 'Добавить':
                self.second = SecondForm(self)
            else:
                rows = list(set([i.row() for i in self.tableWidget.selectedItems()]))
                if len(rows) != 1:
                    self.label.setText('Нужно выбрать ровно одну строку')
                    return
                rows = rows[0]
                row = [self.tableWidget.item(rows, i) for i in range(8)]
                self.second = SecondForm(self, row)
            self.second.show()


class SecondForm(QWidget):
    def __init__(self, parent, row=None):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.con = sqlite3.connect('coffee.sqlite')
        self.cur = self.con.cursor()
        self.parent = parent
        if row:
            self.id = int(row[0].text())
        else:
            self.id = None
        self.roast = {i[1]: i[0] for i in list(self.cur.execute("SELECT * FROM roastings").fetchall())}
        self.taste = {i[1]: i[0] for i in list(self.cur.execute("SELECT * FROM tastes").fetchall())}
        self.groundGrain = {i[1]: i[0] for i in list(self.cur.execute("SELECT * FROM groundOrGrain").fetchall())}
        self.comboBox.clear()
        self.comboBox_2.clear()
        self.comboBox_3.clear()
        self.comboBox.addItems(self.roast.keys())
        self.comboBox_2.addItems(self.groundGrain.keys())
        self.comboBox_3.addItems(self.taste.keys())
        if row:
            self.lineEdit.setText(row[1].text())
            self.comboBox.setCurrentText(row[2].text())
            self.comboBox_2.setCurrentText(row[4].text())
            self.comboBox_3.setCurrentText(row[3].text())
            self.spinBox.setValue(int(row[5].text()))
            self.spinBox_2.setValue(int(row[6].text()))
            self.pushButton.setText('Изменить')
        self.pushButton.clicked.connect(self.add)


    def add(self):
        if self.lineEdit.text() == '':
            self.label_7.setText('Название не может быть пустым')
            return
        if self.id:
            self.cur.execute(f"""UPDATE info
                                SET name = "{self.lineEdit.text()}",
                                roastingID = {self.roast[self.comboBox.currentText()]},
                                groundOrGrain = {self.groundGrain[self.comboBox_2.currentText()]},
                                taste = {self.taste[self.comboBox_3.currentText()]},
                                price = {self.spinBox.value()},
                                volume = {self.spinBox_2.value()}
                                WHERE id == {self.id}""")
        else:
            self.cur.execute(f"""INSERT INTO info(name, roastingID, groundOrGrain, taste,
                            price, volume) VALUES{(self.lineEdit.text(),
                                                   self.roast[self.comboBox.currentText()],
                                                   self.groundGrain[self.comboBox_2.currentText()],
                                                   self.taste[self.comboBox_3.currentText()],
                                                   self.spinBox.value(),
                                                   self.spinBox_2.value())}""")
        self.con.commit()
        self.parent.drawTable()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MyWidget()
    form.show()
    sys.exit(app.exec())