import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog, \
    QFileDialog, QErrorMessage, QLabel
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QPoint
from interface import Ui_MainWindow  # Импортируем интерфейс


class ImageApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.loaded_image = None
        self.image_path = None
        self.current_image = None

        self.loadButton.clicked.connect(self.load_image)
        self.captureButton.clicked.connect(self.capture_image)
        self.showRedChanelButton.clicked.connect(lambda: self.show_channel(2))
        self.showGreenChanelButton.clicked.connect(
            lambda: self.show_channel(1))
        self.showBlueChanelButton.clicked.connect(lambda: self.show_channel(0))
        self.showNegativeButton.clicked.connect(self.show_negative)
        self.rotateButton.clicked.connect(self.rotate_image)
        self.drowCircleButton.clicked.connect(self.draw_circle)
        self.resetButton.clicked.connect(self.reset_image)
        self.saveButton.clicked.connect(self.save_image)
        self.saveAsButton.clicked.connect(self.save_image_as)

    def load_image(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self,
                                                  "Загрузить изображение", "",
                                                  "Images (*.png *.jpg *.jpeg)",
                                                  options=options)
        if fileName:
            self.current_image = cv2.imread(fileName)
            self.loaded_image = cv2.imread(fileName)
            self.image_path = fileName
            self.display_image()

    def capture_image(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            self.show_error("Не удалось подключиться к веб-камере.")
            return
        ret, frame = cap.read()
        cap.release()
        if ret:
            self.loaded_image = frame
            self.current_image = frame
            self.image_path = None
            self.display_image()
        else:
            self.show_error("Не удалось сделать снимок с веб-камеры.")

    def display_image(self):
        if self.current_image is not None:
            rgb_image = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line,
                              QImage.Format_RGB888)
            self.image.setPixmap(
                QPixmap.fromImage(qt_image).scaled(self.image.size(),
                                                   Qt.KeepAspectRatio))
            self.image.setAlignment(Qt.AlignCenter)
            self.shapeLabel.setAlignment(Qt.AlignCenter)
            self.shapeLabel.setText("{}×{}".format(*self.current_image.shape[:2]))

    def show_channel(self, channel):
        if self.current_image is None:
            self.show_error("Пожалуйста, загрузите изображение.")
            return
        channel_image = np.zeros_like(self.current_image)
        channel_image[..., channel] = self.current_image[..., channel]
        self.current_image = channel_image
        self.display_image()

    def reset_image(self):
        if self.current_image is None:
            self.show_error("Пожалуйста, загрузите изображение.")
            return
        self.current_image = self.loaded_image
        self.display_image()

    def show_negative(self):
        if self.current_image is None:
            self.show_error("Пожалуйста, загрузите изображение.")
            return
        self.current_image = 255 - self.current_image
        self.display_image()

    def rotate_image(self):
        if self.current_image is None:
            self.show_error("Пожалуйста, загрузите изображение.")
            return
        angle, ok = QInputDialog.getDouble(self, "Ввод угла",
                                           "Введите угол вращения:", 0, -360,
                                           360, 1)
        if ok:
            (h, w) = self.current_image[:2]
            center = (w // 2, h // 2)

            cos = np.abs(np.cos(np.radians(angle)))
            sin = np.abs(np.sin(np.radians(angle)))

            new_w = int((h * sin) + (w * cos))
            new_h = int((h * cos) + (w * sin))

            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            M[0, 2] += (new_w / 2) - center[0]
            M[1, 2] += (new_h / 2) - center[1]

            # Выполнение поворота с новыми размерами
            self.current_image = cv2.warpAffine(self.current_image, M, (new_w, new_h))

            self.display_image()

    def draw_circle(self):
        if self.loaded_image is None:
            self.show_error("Пожалуйста, загрузите изображение.")
            return
        x, ok_x = QInputDialog.getInt(self, "Ввод координаты X",
                                      "Введите координату X центра круга:", 0,
                                      0, self.current_image.shape[1])
        if not ok_x:
            return
        y, ok_y = QInputDialog.getInt(self, "Ввод координаты Y",
                                      "Введите координату Y центра круга:", 0,
                                      0, self.current_image.shape[0])
        if not ok_y:
            return
        radius, ok_r = QInputDialog.getInt(self, "Ввод радиуса",
                                           "Введите радиус круга:", 0, 0,
                                           min(self.current_image.shape[
                                               :2]) // 2)
        if not ok_r:
            return
        cv2.circle(self.current_image, (x, y), radius, (0, 0, 255), -1)
        self.display_image()

    def save_image(self):
        if self.loaded_image is not None:
            if self.image_path:
                self.loaded_image = self.current_image
                cv2.imwrite(self.image_path, self.current_image)
            else:
                self.save_image_as()
        else:
            self.show_error(
                "Пожалуйста, загрузите или создайте изображение перед сохранением.")

    def save_image_as(self):
        if self.loaded_image is not None:
            options = QFileDialog.Options()
            fileName, _ = QFileDialog.getSaveFileName(self, "Сохранить как",
                                                      "",
                                                      "Images (*.png *.jpg *.jpeg)",
                                                      options=options)
            if fileName:
                self.loaded_image = self.current_image
                cv2.imwrite(fileName, self.current_image)
                self.image_path = fileName
        else:
            self.show_error(
                "Пожалуйста, загрузите или создайте изображение перед сохранением.")

    def show_error(self, message):
        error_dialog = QErrorMessage(self)
        error_dialog.showMessage(message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageApp()
    window.show()
    sys.exit(app.exec_())
