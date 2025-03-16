from PyQt5.QtWidgets import QMainWindow, QApplication
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle('Lab3')
        self.setGeometry(500, 300, 800, 700)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
