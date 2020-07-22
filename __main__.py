from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
import main_window
import sys


class MainWindow(QtWidgets.QMainWindow, main_window.Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.lbl_image.setPixmap(QPixmap("c:/Users/evdok/Desktop/too_many_tomatoes_small.jpg"))

    app.exec_()
