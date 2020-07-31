from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import main_window
import sys
import cv2
from tomato_detector import color_filter, image_processor


class MainWindow(QtWidgets.QMainWindow, main_window.Ui_MainWindow):
    source_image_bgr = None

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setFixedSize(672, 645)

        self.sld_minH.valueChanged.connect(self.sld_min_h_handler)
        self.sld_minS.valueChanged.connect(self.sld_min_s_handler)
        self.sld_minV.valueChanged.connect(self.sld_min_v_handler)
        self.sld_maxH.valueChanged.connect(self.sld_max_h_handler)
        self.sld_maxS.valueChanged.connect(self.sld_max_s_handler)
        self.sld_maxV.valueChanged.connect(self.sld_max_v_handler)

        self.chbx_whiteBalance.stateChanged.connect(self.chbx_white_balance_handler)
        self.chbx_contrast.stateChanged.connect(self.chbx_contrast_handler)

        self.btn_open.clicked.connect(self.btn_open_handler)

    def btn_open_handler(self):
        file_name = QtWidgets.QFileDialog.getOpenFileName(self, "Открыть")[0]
        if file_name:
            try:
                self.open_image(file_name)
                self.lbl_fileName.setText(file_name)
            except (IOError, cv2.error) as e:
                message_box = QtWidgets.QMessageBox()
                message_box.setText(str(e))
                message_box.setWindowTitle("IOError")
                message_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
                message_box.exec()

    def open_image(self, file_name):
        opened_image = cv2.imread(file_name)
        if opened_image is None:
            raise IOError("Ошибка при открытии файла \"" + file_name + "\".")
        self.source_image_bgr = opened_image
        self.redraw_image()

    def sld_min_h_handler(self):
        self.lbl_minH.setText(str(self.sld_minH.value()))
        self.redraw_image()

    def sld_min_s_handler(self):
        self.lbl_minS.setText(str(self.sld_minS.value()))
        self.redraw_image()

    def sld_min_v_handler(self):
        self.lbl_minV.setText(str(self.sld_minV.value()))
        self.redraw_image()

    def sld_max_h_handler(self):
        self.lbl_maxH.setText(str(self.sld_maxH.value()))
        self.redraw_image()

    def sld_max_s_handler(self):
        self.lbl_maxS.setText(str(self.sld_maxS.value()))
        self.redraw_image()

    def sld_max_v_handler(self):
        self.lbl_maxV.setText(str(self.sld_maxV.value()))
        self.redraw_image()

    def chbx_white_balance_handler(self):
        self.redraw_image()

    def chbx_contrast_handler(self):
        self.redraw_image()

    def redraw_image(self):
        if self.source_image_bgr is not None:
            image = self.source_image_bgr
            if self.chbx_whiteBalance.isChecked():
                image = image_processor.white_balance(image)

            if self.chbx_contrast.isChecked():
                image = image_processor.equalize_light(image)

            color_range = {"min": (self.sld_minH.value(), self.sld_minS.value(), self.sld_minV.value()),
                           "max": (self.sld_maxH.value(), self.sld_maxS.value(), self.sld_maxV.value())}
            image_mask = color_filter.find_tomatoes_by_color(image, color_range)
            new_image_bgr = cv2.bitwise_and(image, image, mask=image_mask)

            pix_map = QPixmap.fromImage(
                QImage(new_image_bgr.data, new_image_bgr.shape[1], new_image_bgr.shape[0], new_image_bgr.strides[0],
                       QImage.Format_BGR888))

            self.lbl_image.setPixmap(
                pix_map.scaled(self.lbl_image.width(), self.lbl_image.height(), Qt.KeepAspectRatio))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
