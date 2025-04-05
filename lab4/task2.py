import sys

from PyQt5.QtCore import Qt, QStringListModel
from PyQt5.QtGui import QTextDocument, QAbstractTextDocumentLayout
from PyQt5.QtWidgets import (
    QApplication,
    QCompleter,
    QStyledItemDelegate, QStyle
)

from base_task import BaseTaskWindow
from const import WORDS
from logic import process_search


class HighlightDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlight_color = "#FFFF00"  # Жёлтый фон

    def paint(self, painter, option, index):
        # Получаем текст из модели
        text = index.data(Qt.DisplayRole)
        input_text = self.parent().completionPrefix()

        # Если нет введённого текста, рисуем стандартным способом
        if not input_text:
            super().paint(painter, option, index)
            return

        # Подсвечиваем совпадения (без учёта регистра)
        text_lower = text.lower()
        input_lower = input_text.lower()
        highlighted_html = self.highlight_text(text, text_lower, input_lower)

        # Рисуем HTML
        doc = QTextDocument()
        doc.setHtml(highlighted_html)

        # Настройки отрисовки
        painter.save()
        options = option
        options.text = ""
        style = options.widget.style() if options.widget else QApplication.style()
        style.drawControl(QStyle.CE_ItemViewItem, options, painter)

        # Позиционируем текст
        painter.translate(options.rect.left(), options.rect.top())
        doc.documentLayout().draw(painter, QAbstractTextDocumentLayout.PaintContext())
        painter.restore()

    def highlight_text(self, text, text_lower, input_lower):
        """Возвращает текст с HTML-разметкой для подсветки"""
        idx = text_lower.find(input_lower)
        if idx == -1:
            return text

        return (
            text[:idx] +
            f"<span style='background-color: {self.highlight_color};'>" +
            text[idx:idx + len(input_lower)] +
            "</span>" +
            text[idx + len(input_lower):]
        )


class HighlightCompleter(QCompleter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCaseSensitivity(Qt.CaseInsensitive) # Без учёта регистра
        self.setFilterMode(Qt.MatchStartsWith) # Фильтр по началу слова


class Task2Window(BaseTaskWindow):

    def _init_search_input(self):
        super()._init_search_input()

        self.completer = HighlightCompleter(sorted(WORDS))
        self.completer.setModel(QStringListModel(WORDS))


        delegate = HighlightDelegate(self.completer)
        self.completer.popup().setItemDelegate(delegate)

        self.search_input.setCompleter(self.completer)

    def _on_search_input(self):
        term = self.search_input.text()
        self.info_text_area.setText(process_search(term))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = Task2Window()
    main_window.show()
    sys.exit(app.exec_())
