import os
import cv2
import pytesseract
import sys
import numpy as np
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QFileDialog, QTextEdit, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QApplication, QGridLayout

class TextExtractor(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Create widgets and layouts 
        heading_layout = QHBoxLayout()
        self.btn_select_image = QPushButton('Upload', self)
        self.image_label = QLabel(self)
        self.btn_extract_text = QPushButton('Extract Text', self)
        self.text_edit = QTextEdit(self)
        self.btn_copy_text = QPushButton("Copy Text", self)
        
        # Add a stretch factor to the heading layout
        heading_layout.addStretch(0)
        
        # Connect buttons to respective method
        self.btn_select_image.clicked.connect(self.select_image)
        self.btn_extract_text.clicked.connect(self.extract_text)
        self.btn_copy_text.clicked.connect(self.copy_text)

        # Set the size of the buttons
        self.btn_select_image.setFixedSize(100, 30)
        self.btn_extract_text.setFixedSize(100, 30)
        self.btn_copy_text.setFixedSize(100, 30)

        # Add the buttons to the heading layout
        heading_layout.addWidget(self.btn_select_image)
        heading_layout.addStretch(1)

        # Create a layout to hold the image and text label
        body_layout = QGridLayout()

        self.image_label.setStyleSheet('border: 1px solid black')
        self.image_label.setFixedSize(700, 700)
        
        self.text_edit.setStyleSheet('border: 1px solid black')
        self.text_edit.setFixedSize(700, 700)

        # Add the label and extract button to the first and second columns of the first row
        # Add the text edit to the third columns of the first row
        # Add the copy button to the third columns of the second row
        body_layout.addWidget(self.image_label, 0, 0)
        body_layout.addWidget(self.btn_extract_text, 0, 1)
        body_layout.addWidget(self.text_edit, 0, 2)
        body_layout.addWidget(self.btn_copy_text, 1, 2)

        # Create a layout to hold the heading and body layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(heading_layout)
        main_layout.addLayout(body_layout)

        self.setLayout(main_layout)

        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Text Extractor')
        self.show()

    def select_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, 'Upload', '', 'Images (*.png *.xpm *.jpg *.bmp);;All Files (*)', options=options)
        if file_name:
            # Save the selected image file path
            self.image_path = file_name
            # Display the selected image file in the image label
            pixmap = QtGui.QPixmap(file_name)
             # Align the image to the center of the label
            self.image_label.setAlignment(QtCore.Qt.AlignCenter)
            # Set the label to not automatically adjust the size of the image according to the label size
            self.image_label.setScaledContents(True)
            self.image_label.setPixmap(pixmap)
            self.image_label.setFixedSize(700, 700)
            self.text_edit.setText('')
            # Display a notification message
            self.display_notification("Image uploaded successfully")

    def extract_text(self):
        # Check if an image has been uploaded
        if not hasattr(self, 'image_path'):
            self.display_notification("Please upload an image first")
            return

        # Read the image file
        image = cv2.imread(self.image_path)

        # Convert the image to grayscale
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Threshold the image to create a binary image
        threshold_img = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        # Pass the binary image to Tesseract to extract the text
        tesseract_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(threshold_img, config=tesseract_config, lang='Vietnamese')

        # Display the extracted text in the text label
        self.text_edit.setText(text)
        self.text_edit.setStyleSheet('border: 1px solid black')
        self.text_edit.setVisible(True)
        # Display a notification message
        self.display_notification("Complete image extraction to text")

    def copy_text(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.text_edit.toPlainText())
        # Display a notification message
        self.display_notification("Coppied")

    def display_notification(self, message):
        # Create a message box
        msg_box = QtWidgets.QMessageBox(self)
        # Set the message and the icon
        msg_box.setText(message)
        msg_box.setIcon(QtWidgets.QMessageBox.Information)
        # Display the message box
        msg_box.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TextExtractor()
    ex.setGeometry(200, 50, 1500, 800)
    ex.show()
    sys.exit(app.exec_())