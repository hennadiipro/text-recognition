from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QFileDialog, QTextEdit, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QApplication, QGridLayout

class View(QtWidgets.QWidget):
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
        from controller.text_extractor import extract_text_from_image
        try:
            # Check if an image has been uploaded
            if not hasattr(self, 'image_path'):
                self.display_notification("Please upload an image first")
                return
            # Extract text from the image
            text = extract_text_from_image(self.image_path)
            # Display the extracted text in the text edit
            self.text_edit.setText(text)
            self.display_notification("Text extracted successfully...")
        except Exception as e:
            self.display_notification("Failed to extract text. Please try again.")
            print("Error:", e)

    def copy_text(self):
        # Get the system clipboard
        clipboard = QApplication.clipboard()
        # Copy the text in the text edit to the clipboard
        clipboard.setText(self.text_edit.toPlainText())
        # Display a notification message that the text has been copied
        self.display_notification("Text copied to clipboard!")

    def display_notification(self, message):
        # Create a message box
        notification = QtWidgets.QMessageBox()
        # Set the message
        notification.setText(message)
        # Set the title of the notification window to "Notification"
        notification.setWindowTitle("Notification")
        # Display the message box
        notification.exec_()