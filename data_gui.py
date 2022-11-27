!pip install pyqtgraph

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QComboBox, QMainWindow, QApplication, QWidget, QVBoxLayout
import pyqtgraph as pg
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


class Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent=None)
        self.combobox1 = QComboBox()
        self.combobox1.addItems(['A', 'B', 'C'])
        self.combobox2 = QComboBox()
        self.combobox2.addItems(['A', 'B', 'C'])
        self.combobox3 = QComboBox()
        self.combobox3.addItems(['A', 'B', 'C'])


        vLayout = QtWidgets.QVBoxLayout(self)
        hLayout = QtWidgets.QHBoxLayout()
        #self.pathLE = QtWidgets.QLineEdit(self)
        self.graphWidget = pg.PlotWidget()
        self.loadBtn = QtWidgets.QPushButton("Import CSV", self)
        self.pandasTv = QtWidgets.QTableView(self)
        self.table_btn = QtWidgets.QPushButton("Table View", self)
        self.plot_btn = QtWidgets.QPushButton("Plot", self)
        vLayout.addWidget(self.combobox1)
        vLayout.addWidget(self.combobox2)
        vLayout.addWidget(self.combobox3)
        hLayout.addWidget(self.loadBtn)
        vLayout.addLayout(hLayout)
        vLayout.addWidget(self.graphWidget)
        vLayout.addWidget(self.plot_btn)
        vLayout.addWidget(self.table_btn)
        vLayout.addWidget(self.pandasTv)
        self.loadBtn.clicked.connect(self.loadFile)
        self.table_btn.clicked.connect(self.table_view)
        self.plot_btn.clicked.connect(self.plot)


    def plot(self):
        hour = [1,2,3,4,5,6,7,8,9,10]
        temperature = [30,32,34,32,33,31,29,32,35,45]
        self.graphWidget.plot(hour, temperature)

    def table_view(self):
        self.pandasTv.setModel(self.model)
        self.pandasTv.setSortingEnabled(True)
        
    def loadFile(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open File", "", "CSV Files (*.csv)"
        )
        #self.pathLE.setText(fileName)
        if fileName:
            df = pd.read_csv(fileName)
            array = np.array(df.values)
            headers = df.columns.tolist()
            self.model = NumpyArrayModel(array, headers)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())
