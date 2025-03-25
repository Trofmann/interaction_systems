import sys

from PyQt5.QtWidgets import (
    QMainWindow,
    QApplication,
    QTextEdit,
    QLineEdit,
)
from const import TEXT
from logic import process_search


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._setup_ui()
        self._init_info_text_area()
        self._init_search_input()

    def _setup_ui(self):
        self.setWindowTitle('Lab4')
        self.setGeometry(500, 300, 1000, 700)

    def _init_info_text_area(self):
        self.info_text_area = QTextEdit(self)
        self.info_text_area.setReadOnly(True)
        self.info_text_area.move(500, 100)
        self.info_text_area.setFixedWidth(400)
        self.info_text_area.setFixedHeight(450)
        self.info_text_area.setText(TEXT)

    def _init_search_input(self):
        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText('Введите текст...')
        self.search_input.move(100, 100)
        self.search_input.setFixedWidth(300)
        self.search_input.returnPressed.connect(self._on_search_input)

    def _on_search_input(self):
        term = self.search_input.text()
        self.info_text_area.setText(process_search(term))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
