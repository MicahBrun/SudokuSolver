from PyQt5 import QtCore, QtGui, QtWidgets

import numpy as np

import SolveSudoku as SS


class Ui_MainWindow(object):
    def createSudokuGrid(self, grid, minigridArr):

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(30)
        font.setBold(False)
        font.setWeight(50)

        minigridArr = [[] for i in range(3)]
        for i in range(3):
            for j in range(3):
                minigrid = QtWidgets.QGridLayout()
                minigrid.setObjectName("minigrid" + str(i) + str(j))
                grid.addLayout(minigrid, i + 1, j + 1, 1, 1)

                minigridArr[i].append(minigrid)

        self.sudokuGrid = []
        for i in range(9):
            self.sudokuGrid.append([])
            for j in range(9):
                miniIdx = [i // 3, j // 3]

                spinbox = QtWidgets.QSpinBox()

                spinbox.setFont(font)
                spinbox.setMinimum(0)
                spinbox.setMaximum(9)
                spinbox.setObjectName("spinBox" + str(i) + str(j))
                minigridArr[miniIdx[0]][miniIdx[1]].addWidget(
                    spinbox, i % 3 + 1, j % 3 + 1, 1, 1
                )

                sizePolicy = QtWidgets.QSizePolicy(
                    QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
                )
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(spinbox.sizePolicy().hasHeightForWidth())
                spinbox.setSizePolicy(sizePolicy)

                self.sudokuGrid[i].append(spinbox)

    def getSudokuMatrix(self):
        self.sudokuMatrix = np.zeros((9, 9), dtype=int)
        for i, row in enumerate(self.sudokuGrid):
            for j, spinbox in enumerate(row):
                self.sudokuMatrix[i, j] = spinbox.value()

    def updateSudokuGrid(self):
        for i, row in enumerate(self.sudokuGrid):
            for j, spinbox in enumerate(row):
                spinbox.setValue(self.sudokuMatrix[i, j])

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(60, 40, 500, 500))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setVerticalSpacing(8)

        self.minigrid = []
        self.createSudokuGrid(self.gridLayout, self.minigrid)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.button = QtWidgets.QPushButton(MainWindow)
        self.button.setText("Find Solution")
        self.button.move(600, 40)

        self.resetB = QtWidgets.QPushButton(MainWindow)
        self.resetB.setText("reset")
        self.resetB.move(600, 80)

        self.error_dialog = QtWidgets.QErrorMessage()

        self.button.clicked.connect(self.clicked)
        self.resetB.clicked.connect(self.resetSudoku)
        self.getSudokuMatrix()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Sudoku Solver"))

    def clicked(self):
        self.getSudokuMatrix()
        if np.count_nonzero(self.sudokuMatrix) == 9 ** 2:
            return

        try:
            self.sudokuMatrix = SS.SolveSudoku(self.sudokuMatrix)
        except:
            self.error_dialog.showMessage("This puzzle is not solvable!")
            self.error_dialog.setWindowTitle("Error")
            self.error_dialog.exec_()
        self.updateSudokuGrid()

    def resetSudoku(self):
        self.sudokuMatrix = np.zeros((9, 9), dtype=int)
        self.updateSudokuGrid()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
