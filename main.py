import sys

from PyQt5 import QtWidgets, QtGui

from design import Ui_MainWindow
from utils import *
import xlsxwriter


class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.last_row = 0

        # signal connections
        self.ui.cb_p.currentTextChanged.connect(self.set_S)
        self.ui.cb_S.currentTextChanged.connect(self.set_N)
        self.ui.cb_S.currentTextChanged.connect(self.set_m)
        self.ui.cb_m.currentTextChanged.connect(self.set_n)
        self.ui.pushButton.clicked.connect(self.fill_r_col)
        self.ui.table.cellClicked.connect(self.fill_c_col)
        self.ui.saveButton.clicked.connect(self.saveTable)

        self.set_p()
        self.setup_table()


    def set_p(self):
        for i in [2, 3, 5, 7, 11, 13]:
            self.ui.cb_p.addItem(str(i))


    def set_S(self, p):
        S_arr = get_S(int(p))
        self.ui.cb_S.clear()
        for S in S_arr:
            self.ui.cb_S.addItem(str(S))


    def set_N(self, S):
        if not S:
            return

        N = get_N(int(self.ui.cb_p.currentText()), int(S))
        self.ui.N_placeholder.setText(str(N))


    def set_m(self, S):
        if not S:
            return

        m_arr = get_m(int(S))
        self.ui.cb_m.clear()
        for m in m_arr:
            self.ui.cb_m.addItem(str(m))


    def set_n(self, m):
        if not m:
            return

        n = int(self.ui.cb_S.currentText()) // int(m)
        self.ui.n_placeholder.setText(str(n))


    def setup_table(self):
        self.ui.table.setColumnCount(8)
        self.ui.table.setHorizontalHeaderLabels([
            'r',
            'r в p-ичной',
            'g(r)',
            'C1',
            # 'C1 в p-ичной',
            'g(C1)',
            'C2',
            'C3',
            'C3 в p-ичной'
            ])
        self.ui.table.verticalHeader().setVisible(False)
        self.ui.table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.ui.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)


    def calculateButtonClick(self):
        self.ui.pushButton.setText('Идет расчет данных')
        self.fill_r_col()

    def fill_r_col(self):
        if not self.ui.cb_m.currentText():
            return

        self.ui.table.clearContents()

        self.ui.table.setRowCount(0)

        m = int(self.ui.cb_m.currentText())
        p = int(self.ui.cb_p.currentText())
        r_arr = get_r(p, m)
        i = -1
        for i, (r, r_p, g_r_p) in enumerate(r_arr):
            self.ui.table.setRowCount(i + 1)
            self.ui.table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(r)))
            self.ui.table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(r_p)))
            self.ui.table.setItem(i, 2, QtWidgets.QTableWidgetItem(str(g_r_p)))



        if i > -1:
            self.last_row = max(i, self.last_row)

        self.ui.pushButton.setText('Рассчитать значения')




    def fill_c_col(self, x, y):
        gray_color = QtGui.QColor("#f0fcf2")
        if y != 0:
            print(x, y)
            return


        self.ui.table.removeColumn(7)
        self.ui.table.removeColumn(6)
        self.ui.table.removeColumn(5)
        self.ui.table.removeColumn(4)
        self.ui.table.removeColumn(3)

        self.ui.table.setRowCount(self.last_row + 1)

        self.ui.table.insertColumn(3)
        self.ui.table.insertColumn(4)
        self.ui.table.insertColumn(5)
        self.ui.table.insertColumn(6)
        self.ui.table.insertColumn(7)
        # self.ui.table.insertColumn(7)
        self.ui.table.setHorizontalHeaderItem(3, QtWidgets.QTableWidgetItem('C1'))
        # self.ui.table.setHorizontalHeaderItem(4, QtWidgets.QTableWidgetItem('C1 в p-ичной'))
        self.ui.table.setHorizontalHeaderItem(4, QtWidgets.QTableWidgetItem('g(C1)'))
        self.ui.table.setHorizontalHeaderItem(5, QtWidgets.QTableWidgetItem('C2'))
        self.ui.table.setHorizontalHeaderItem(6, QtWidgets.QTableWidgetItem('C3'))
        self.ui.table.setHorizontalHeaderItem(7, QtWidgets.QTableWidgetItem('C3 в p-ичной'))

        try:
            r = int(self.ui.table.item(x, y).text())
        except AttributeError:
            return

        p = int(self.ui.cb_p.currentText())
        s = int(self.ui.cb_S.currentText())
        m = int(self.ui.cb_m.currentText())

        c_arr = get_C1(r, p, s, m)
        i = -1
        for i, (c, c_p, g_c_p, c2) in enumerate(c_arr):
            if self.ui.table.rowCount() < i + 1:
                self.ui.table.setRowCount(i + 1)

            item = QtWidgets.QTableWidgetItem(str(c))
            self.ui.table.setItem(i, 3, item)

            # item = QtWidgets.QTableWidgetItem(str(c_p))
            # item.setBackground(gray_color)
            # self.ui.table.setItem(i, 4, item)

            item = QtWidgets.QTableWidgetItem(str(g_c_p))
            self.ui.table.setItem(i, 4, item)

            item = QtWidgets.QTableWidgetItem(str(c2))
            self.ui.table.setItem(i, 5, item)

        self.last_row = max(i, self.last_row)

        for i, val in enumerate(sorted(set(c2 for _, _, _, c2 in c_arr))):
            item = QtWidgets.QTableWidgetItem(str(val))
            item_p = QtWidgets.QTableWidgetItem(str(to_base(val, p)))
            self.ui.table.setItem(i, 6, item)
            self.ui.table.setItem(i, 7, item_p)

        self.ui.M_placeholder.setText(str(i + 1))

    def saveTable(self):
        self.ui.saveButton.setText('Идет сохранение таблицы')
        workbook = xlsxwriter.Workbook('table.xlsx')
        worksheet = workbook.add_worksheet('Table')
        bold = workbook.add_format({'bold': True})
        for col in range(self.ui.table.columnCount()):
            worksheet.write(0, col, self.ui.table.horizontalHeaderItem(col).text(), bold)
        for row in range(self.ui.table.rowCount()):
            for col in range(self.ui.table.columnCount()):
                if self.ui.table.item(row, col):
                    worksheet.write(row + 1, col, int(self.ui.table.item(row, col).text()))
                else:
                    worksheet.write(row + 1, col, '-')
        workbook.close()
        self.ui.saveButton.setText('Сохранить таблицу в table.xlsx')


app = QtWidgets.QApplication([])
application = mywindow()
application.show()

sys.exit(app.exec())