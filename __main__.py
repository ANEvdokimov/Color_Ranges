from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap, QImage
import main_window
import sys
import cv2


class MainWindow(QtWidgets.QMainWindow, main_window.Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.sld_minH.valueChanged.connect(self.sld_min_h_handler)
        self.sld_minS.valueChanged.connect(self.sld_min_s_handler)
        self.sld_minV.valueChanged.connect(self.sld_min_v_handler)
        self.sld_maxH.valueChanged.connect(self.sld_max_h_handler)
        self.sld_maxS.valueChanged.connect(self.sld_max_s_handler)
        self.sld_maxV.valueChanged.connect(self.sld_max_v_handler)

        self.sld_minCircularity.valueChanged.connect(self.sld_min_circularity_handler)
        self.sld_maxCircularity.valueChanged.connect(self.sld_max_circularity_handler)
        self.sld_minConvexity.valueChanged.connect(self.sld_min_convexity_handler)
        self.sld_maxConvexity.valueChanged.connect(self.sld_max_convexity_handler)
        self.sld_minInertia.valueChanged.connect(self.sld_min_inertia_handler)
        self.sld_maxInertia.valueChanged.connect(self.sld_max_inertia_handler)

        self.sbx_minArea.valueChanged.connect(self.sbx_area_handler)
        self.sbx_maxArea.valueChanged.connect(self.sbx_area_handler)

    def sld_min_h_handler(self):
        self.lbl_minH.setText(str(self.sld_minH.value()))

    def sld_min_s_handler(self):
        self.lbl_minS.setText(str(self.sld_minS.value()))

    def sld_min_v_handler(self):
        self.lbl_minV.setText(str(self.sld_minV.value()))

    def sld_max_h_handler(self):
        self.lbl_maxH.setText(str(self.sld_maxH.value()))

    def sld_max_s_handler(self):
        self.lbl_maxS.setText(str(self.sld_maxS.value()))

    def sld_max_v_handler(self):
        self.lbl_maxV.setText(str(self.sld_maxV.value()))

    def sld_min_circularity_handler(self):
        self.lbl_minCircularity.setText(str(self.sld_minCircularity.value() / 20))

    def sld_max_circularity_handler(self):
        self.lbl_maxCircularity.setText(str(self.sld_maxCircularity.value() / 20))

    def sld_min_convexity_handler(self):
        self.lbl_minConvexity.setText(str(self.sld_minConvexity.value() / 20))

    def sld_max_convexity_handler(self):
        self.lbl_maxConvexity.setText(str(self.sld_maxConvexity.value() / 20))

    def sld_min_inertia_handler(self):
        self.lbl_minInertia.setText(str(self.sld_minInertia.value() / 20))

    def sld_max_inertia_handler(self):
        self.lbl_maxInertia.setText(str(self.sld_maxInertia.value() / 20))

    def sbx_area_handler(self):
        pass


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
    image_source = cv2.imread("c:/Users/evdok/Desktop/too_many_tomatoes_small.jpg")

    resized_image = resize_image_for_frame(image_source, window.lbl_image.width(), window.lbl_image.height())
    window.lbl_image.setPixmap(
        QPixmap.fromImage(
            QImage(resized_image.data, resized_image.shape[1], resized_image.shape[0], resized_image.strides[0],
                   QImage.Format_BGR888))
    )

    app.exec_()
