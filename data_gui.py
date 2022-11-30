!pip install pyqtgraph
import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QComboBox, QMainWindow, QApplication, QWidget, QVBoxLayout
import pyqtgraph as pg
import pyqtgraph.exporters
from pyqtgraph import PlotWidget, plot
import pandas as pd
import numpy as np

class NumpyArrayModel(QtCore.QAbstractTableModel):
    def __init__(self, array, headers, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent=parent)

        self._array = array
        self._headers = headers
        self.r, self.c = np.shape(self.array)

    @property
    def array(self):
        return self._array

    @property
    def headers(self):
        return self._headers

    def rowCount(self, parent=QtCore.QModelIndex()):
        return self.r

    def columnCount(self, parent=QtCore.QModelIndex()):
        return self.c

    def headerData(self, p_int, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                if p_int < len(self.headers):
                    return self.headers[p_int]
            elif orientation == QtCore.Qt.Vertical:
                return p_int + 1
        return

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        row = index.row()
        column = index.column()
        if row < 0 or row >= self.rowCount():
            return None
        if column < 0 or column >= self.columnCount():
            return None
        if role == QtCore.Qt.DisplayRole:
            return self.array[row, column]
        return None

    def setData(self, index, value, role):
        if not index.isValid():
            return False
        if role != QtCore.Qt.EditRole:
            return False
        row = index.row()
        column = index.column()
        if row < 0 or row >= self.rowCount():
            return False
        if column < 0 or column >= self.columnCount():
            return False
        self.array.values[row][column] = value
        self.dataChanged.emit(index, index)
        return True

    def sort(self, column, order):
        self.layoutAboutToBeChanged.emit()
        argsort = self.array[:, column].argsort()
        if order == QtCore.Qt.DescendingOrder:
            argsort = argsort[::-1]
        self._array = self.array[argsort]
        self.layoutChanged.emit()


class Window(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent=None)

        self.combo_box1 = QComboBox()
        self.combo_box1.addItems(['A', 'B', 'C'])
        self.combo_box2 = QComboBox()
        self.combo_box2.addItems(['A', 'B', 'C'])
        self.combo_box3 = QComboBox()
        self.combo_box3.addItems(['A', 'B', 'C'])
        self.pd_table = QtWidgets.QTableView(self)

        self.import_button = QtWidgets.QPushButton("Import CSV", self)
        self.table_button = QtWidgets.QPushButton("View Table", self)
        self.plot_button = QtWidgets.QPushButton("Plot", self)
        self.run_button = QtWidgets.QPushButton("Run", self)
        self.import_button.setCheckable(True)

        self.import_button.clicked.connect(self.import_file)
        self.table_button.clicked.connect(self.table_view)
        self.plot_button.clicked.connect(self.plot)
        self.run_button.clicked.connect(self.run)

        vert_layout = QtWidgets.QVBoxLayout(self)
        horiz_layout = QtWidgets.QHBoxLayout()
        horiz1_layout = QtWidgets.QHBoxLayout()
        horiz_layout.addWidget(self.combo_box1)
        horiz_layout.addWidget(self.combo_box2)
        horiz_layout.addWidget(self.combo_box3)
        vert_layout.addLayout(horiz_layout)
        horiz1_layout.addWidget(self.import_button)
        horiz1_layout.addWidget(self.plot_button)
        horiz1_layout.addWidget(self.table_button)
        horiz1_layout.addWidget(self.run_button)
        vert_layout.addLayout(horiz1_layout)
        vert_layout.addWidget(self.pd_table)

    def run(self):
        if self.import_button.isChecked():
            print(self.model)
        else:
            print("No file has been imported!")

    def plot(self):
        hour = [1,2,3,4,5,6,7,8,9,10]
        temperature = [30,32,34,32,33,31,29,32,35,45]
        plt = pg.plot(hour, temperature)
        plt.showGrid(x=True,y=True)

    def table_view(self):
        self.pd_table.setModel(self.model)
        self.pd_table.setSortingEnabled(True)

    def import_file(self):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open File", "", "CSV Files (*.csv)")
        if file_name:
            df = pd.read_csv(file_name)
            array = np.array(df.values)
            headers = df.columns.tolist()
            self.model = NumpyArrayModel(array, headers)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
