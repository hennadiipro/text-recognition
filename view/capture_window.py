import cv2
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog, QLabel, QPushButton, QGridLayout
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap

class CaptureWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(600, 100, 700, 700)
        self.setWindowTitle('Webcam')

        # Add a label to the new window to display the captured image
        self.capture_label = QLabel(self)
        #self.capture_label.setStyleSheet('border: 1px solid black')
        self.capture_label.setFixedSize(700, 700)

        # Create a button for capturing the image
        capture_button = QPushButton('Capture', self)
        capture_button.setFixedSize(100, 30)
        capture_button.clicked.connect(self.take_screenshot)

        capture_layout = QGridLayout()
        capture_layout.addWidget(self.capture_label, 0, 0)
        capture_layout.addWidget(capture_button, 0, 0,
            QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)

        self.show()
        self.cap = cv2.VideoCapture(0)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            print("Error capturing frame")
            self.timer.stop()
            return

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (700, 700)) # resize the frame to 700x700
        image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image)
        self.capture_label.setPixmap(pixmap)

    def take_screenshot(self):
        self.timer.stop()
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        fileName, _ = QFileDialog.getSaveFileName(self, "Save Screenshot", "", "PNG (*.png);;JPEG (*.jpeg *.jpg);;BMP (*.bmp)", options=options)
        if fileName:
            ret, frame = self.cap.read()
            if not ret:
                print("Error capturing frame")
                return

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(image)
            pixmap.save(fileName)
            self.timer.start()
        else:
            self.timer.start()