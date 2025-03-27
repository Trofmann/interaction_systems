import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QCompleter,
)

from base_task import BaseTaskWindow
from const import WORDS
from logic import process_search


class Task2Window(BaseTaskWindow):

    def _init_search_input(self):
        super()._init_search_input()

        self.completer = QCompleter(sorted(WORDS))
        self.completer.setFilterMode(Qt.MatchStartsWith)  # Фильтр по началу слова
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)  # Без учёта регистра
        self.search_input.setCompleter(self.completer)

    def _on_search_input(self):
        term = self.search_input.text()
        self.info_text_area.setText(process_search(term))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = Task2Window()
    main_window.show()
    sys.exit(app.exec_())
