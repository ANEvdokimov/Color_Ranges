from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap, QImage
import main_window
import sys
import cv2
from tomato_detector import color_filter, image_processor


class MainWindow(QtWidgets.QMainWindow, main_window.Ui_MainWindow):
    source_image_bgr = []

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

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
            except IOError as e:
                message_box = QtWidgets.QMessageBox()
                message_box.setText(str(e))
                message_box.setWindowTitle("IOError")
                message_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
                message_box.exec()

    def open_image(self, file_name):
        opened_image = cv2.imread(file_name)
        if opened_image is None:
            raise IOError("Ошибка при открытии изображения.")
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
        if len(self.source_image_bgr) != 0:
            image = self.source_image_bgr
            if self.chbx_whiteBalance.isChecked():
                image = image_processor.white_balance(image)

            if self.chbx_contrast.isChecked():
                image = image_processor.equalize_light(image)

            color_range = {"min": (self.sld_minH.value(), self.sld_minS.value(), self.sld_minV.value()),
                           "max": (self.sld_maxH.value(), self.sld_maxS.value(), self.sld_maxV.value())}
            image_mask = color_filter.find_tomatoes_by_color(image, color_range)
            new_image_bgr = cv2.bitwise_and(image, image, mask=image_mask)

            resized_image_bgr = self.resize_image_for_frame(new_image_bgr, self.lbl_image.width(),
                                                            self.lbl_image.height())
            self.lbl_image.setPixmap(QPixmap.fromImage(
                QImage(resized_image_bgr.data, resized_image_bgr.shape[1], resized_image_bgr.shape[0],
                       resized_image_bgr.strides[0], QImage.Format_BGR888)))

    @staticmethod
    def resize_image_for_frame(image, frame_width, frame_height):
        image_width = image.shape[1]
        image_height = image.shape[0]

        if image_height > frame_height or image_width > frame_width:
            width_diff = image_width / frame_width
            height_diff = image_height / frame_height
        else:
            width_diff = frame_width / image_width
            height_diff = frame_height / image_height

        if width_diff > height_diff:
            return cv2.resize(image, (round(image_width / width_diff), round(image_height / width_diff)))
        else:
            return cv2.resize(image, (round(image_width / height_diff), round(image_height / height_diff)))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()

    window.show()
    # image_source = cv2.imread("c:/Users/evdok/Desktop/too_many_tomatoes_small.jpg")
    #
    # resized_image2 = window.resize_image_for_frame(image_source, window.lbl_image.width(), window.lbl_image.height())
    # window.lbl_image.setPixmap(
    #     QPixmap.fromImage(
    #         QImage(resized_image2.data, resized_image2.shape[1], resized_image2.shape[0], resized_image2.strides[0],
    #                QImage.Format_BGR888))
    # )

    app.exec_()
