import os
from PyQt5 import (
    QtWidgets,
    QtGui,
    QtCore
)
from PyQt5.QtWidgets import (
    QFileDialog,
    QTextEdit,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QApplication,
    QGridLayout,
    QMessageBox,
    QProgressBar,
    QMenuBar
)
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon

class View(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Setting up paths for icons and favicon
        current_path = os.path.dirname(os.path.abspath(__file__))
        icon_folder_path = os.path.join(current_path, "..", "resources", "icons")
        favicon_folder_path = os.path.join(current_path, "..", "resources", "favicon")
        favicon_path = os.path.join(favicon_folder_path, "favicon.ico")
        open_icon_path = os.path.join(icon_folder_path, "open.png")
        save_icon_path = os.path.join(icon_folder_path, "save.png")
        extract_icon_path = os.path.join(icon_folder_path, "extract.png")
        
        # Setting up timer for text extraction
        self.timer = QTimer()
        self.timer.setInterval(50)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.extract_text)
        
        # Setting up progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setVisible(False)
        
        # Setting up menu bar and actions
        self.menu_bar = QMenuBar(self)
        file_menu = self.menu_bar.addMenu("File")
        help_menu = self.menu_bar.addMenu("Help")
        open_action = file_menu.addAction("Open")
        open_action.setShortcut("Ctrl+O")
        save_action = file_menu.addAction("Save")
        save_action.setShortcut("Ctrl+S")
        extract_action = file_menu.addAction("Extract")
        extract_action.setShortcut("Ctrl+E")
        about_action = help_menu.addAction("About")
        
        # Setting up icons for actions
        open_icon = QIcon(open_icon_path)
        save_icon = QIcon(save_icon_path)
        extract_icon = QIcon(extract_icon_path)
        open_action.setIcon(open_icon)
        save_action.setIcon(save_icon)
        extract_action.setIcon(extract_icon)
        
        # Connecting actions to functions
        open_action.triggered.connect(self.select_image)
        save_action.triggered.connect(self.save_text)
        extract_action.triggered.connect(self.extract_text)
        
        # Setting up widgets for displaying image and text
        self.image_label = QLabel(self)
        self.btn_extract_text = QPushButton('Extract Text', self)
        self.text_edit = QTextEdit(self)
        self.btn_clear_text = QPushButton("Clear", self)
        self.btn_copy_text = QPushButton("Copy", self)
        
        # Connecting buttons to functions
        self.btn_extract_text.clicked.connect(self.extract_text)
        self.btn_clear_text.clicked.connect(self.clear_text)
        self.btn_copy_text.clicked.connect(self.copy_text)
        
        # Setting fixed size for buttons
        self.btn_extract_text.setFixedSize(100, 30)
        self.btn_clear_text.setFixedSize(100, 30)
        self.btn_copy_text.setFixedSize(100, 30)
        
        # Setting up layout for the widgets
        body_layout = QGridLayout()
        
        # Setting styles for image and text display widgets
        self.image_label.setStyleSheet('border: 1px solid black')
        self.image_label.setFixedSize(700, 700)
        self.text_edit.setStyleSheet('border: 1px solid black; border-radius: 3px;')
        self.text_edit.setFixedSize(700, 700)
        
        # Adding widgets to the layout
        body_layout.addWidget(self.image_label, 0, 0)  # column 1 row 1
        body_layout.addWidget(self.btn_extract_text, 0, 1)  # column 2 row 1
        body_layout.addWidget(self.text_edit, 0, 2)  # column 3 row 1
        body_layout.addWidget(self.btn_clear_text, 0, 2,
            QtCore.Qt.AlignBottom)# column 3 row 1
        body_layout.addWidget(self.btn_copy_text, 0, 2,
            QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight) # column 3 row 1
        body_layout.addWidget(self.progress_bar, 1, 0)  # column 1 row 2
        
        main_layout = QVBoxLayout()
        main_layout.addLayout(body_layout)
        main_layout.setMenuBar(self.menu_bar)

        self.setLayout(main_layout)
        self.setWindowTitle("Extract Text From Imager")
        self.setWindowIcon(QIcon(favicon_path))
        self.setGeometry(300, 300, 1000, 700)
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

    def clear_text(self):
        self.text_edit.clear()

    def copy_text(self):
        text = self.text_edit.toPlainText()
        if text:
            # Copy the text to the clipboard
            clipboard = QApplication.clipboard()
            clipboard.setText(text)
            # Show a message box to indicate that the text has been copied
            self.btn_copy_text.setText("Copied ✓")
            self.btn_copy_text.setStyleSheet("background-color: 87CEEB")
        else:
            QMessageBox.warning(self, 'Warning', 'Nothing to copy!')

    def save_text(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Text", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            text = self.text_edit.toPlainText()
            if text:
                with open(file_name, "w", encoding='utf8') as file:
                    file.write(text)
                QMessageBox.information(self, "Save Successful", "Text saved successfully.")
            else:
                QMessageBox.warning(self, "Nothing to save", "The text area is empty.")