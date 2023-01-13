import sys
from PyQt5.QtWidgets import QApplication
from view.main_window import View

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = View()
    # Set the size and position of the TextExtractor widget on the screen
    ex.setGeometry(200, 50, 1500, 800)
    sys.exit(app.exec_())