from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QFileDialog, QTextEdit, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QApplication, QGridLayout, QMessageBox, QProgressBar, QMenuBar
from PyQt5.QtCore import QTimer

class View(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.timer = QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.extract_text)
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setVisible(False)

        # Create a menu bar
        self.menu_bar = QMenuBar(self)

        # Create menus
        file_menu = self.menu_bar.addMenu("File")
        help_menu = self.menu_bar.addMenu("Help")

        # Create actions for menus
        open_action = file_menu.addAction("Open")
        save_action = file_menu.addAction("Save")
        about_action = help_menu.addAction("About")

        # Connect actions to methods
        open_action.triggered.connect(self.select_image)
        save_action.triggered.connect(self.save_text)

        # Create widgets and layouts 
        self.image_label = QLabel(self)
        self.btn_extract_text = QPushButton('Extract Text', self)
        self.text_edit = QTextEdit(self)
        self.btn_copy_text = QPushButton("Copy Text", self)
        
        # Connect buttons to respective method
        self.btn_extract_text.clicked.connect(self.extract_text)
        self.btn_copy_text.clicked.connect(self.copy_text)

        # Set the size of the buttons
        self.btn_extract_text.setFixedSize(100, 30)
        self.btn_copy_text.setFixedSize(100, 30)

        # Create a layout to hold the image and text label
        body_layout = QGridLayout()

        self.image_label.setStyleSheet('border: 1px solid black')
        self.image_label.setFixedSize(700, 700)
        self.text_edit.setStyleSheet('border: 1px solid black')
        self.text_edit.setFixedSize(700, 700)

        body_layout.addWidget(self.image_label, 0, 0) #colomn 1 row 1
        body_layout.addWidget(self.btn_extract_text, 0, 1) #column 2 row 1
        body_layout.addWidget(self.progress_bar, 1, 0) #column 2 row 2
        body_layout.addWidget(self.text_edit, 0, 2) #column 3 row 1
        body_layout.addWidget(self.btn_copy_text, 1, 2) #column 3 row 2

        # Create a layout to hold the heading and body layout
        main_layout = QVBoxLayout()
        main_layout.setMenuBar(self.menu_bar)
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
            self.image_path = file_name
            pixmap = QtGui.QPixmap(file_name)
            self.image_label.setAlignment(QtCore.Qt.AlignCenter)
            self.image_label.setScaledContents(True)
            self.image_label.setPixmap(pixmap)
            self.image_label.setFixedSize(700, 700)
            self.btn_copy_text.setText("Copy Text")

    def extract_text(self):
        if not hasattr(self, 'image_path'):
            QMessageBox.warning(self, 'Warning', 'Please upload an image first!')
            return

        self.progress_bar.setVisible(True)
        self.progress_bar.setMaximum(100)

        from controller.text_extractor import extract_text_from_image
        text = extract_text_from_image(self.image_path, self.progress_bar)

        self.text_edit.setText(text)
        self.progress_bar.setVisible(False)
        self.btn_copy_text.setText("Copy Text")
        QMessageBox.information(self, 'Extracted information', 'Text extracted successfully...')

    def copy_text(self):
        text = self.text_edit.toPlainText()
        if text:
            # Copy the text to the clipboard
            clipboard = QApplication.clipboard()
            clipboard.setText(text)
            # Show a message box to indicate that the text has been copied
            self.btn_copy_text.setText("Copied ✓")
            self.btn_copy_text.setStyleSheet("background-color: blue")
        else:
            QMessageBox.warning(self, 'Warning', 'Nothing to copy!')

    def save_text(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getSaveFileName(self, 'Save', '', 'Text Files (*.txt);;All Files (*)', options=options)
        if file_name:
            with open(file_name, "w", encoding='utf8') as file:
                file.write(self.text_edit.toPlainText())