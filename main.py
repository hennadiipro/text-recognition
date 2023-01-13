import sys
from PyQt5.QtWidgets import QApplication
from view.main_window import View

if __name__ == '__main__':
    # Initialize QApplication, which manages the main event loop and
    # starts the application
    app = QApplication(sys.argv)
    # Initialize the TextExtractor widget
    ex = View()
    # Set the size and position of the TextExtractor widget on the screen
    ex.setGeometry(200, 50, 1500, 800)
    # Show the TextExtractor widget
    ex.show()
    # Run the event loop, exiting when the application is closed
    sys.exit(app.exec_())