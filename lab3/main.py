import sys

from PyQt5.QtWidgets import (
    QMainWindow,
    QApplication,
    QMenu,
    QAction,
    QMenuBar, QTextEdit,
)

from statistics_storage import StatisticsRecord
from menu import (
    menubar_description,
    MenuItem
)
from experiment import Experiment


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self._create_menu()
        self._init_experiment()
        self._init_statistics_text_area()
        self._init_task_text_area()

    def setup_ui(self):
        self.setWindowTitle('Lab3')
        self.setGeometry(500, 300, 800, 700)

    def _init_experiment(self):
        self.experiment = Experiment()
        self.experiment.start()
        self.experiment.statistics_storage.statistics_changed.connect(self._redraw_statistics)
        self.experiment.task_changed.connect(self._redraw_task_text)

    def _init_statistics_text_area(self):
        self.statistics_text_area = QTextEdit(self)
        self.statistics_text_area.setReadOnly(True)
        self.statistics_text_area.move(300, 100)
        self.statistics_text_area.setFixedWidth(400)
        self.statistics_text_area.setFixedHeight(150)

    def _init_task_text_area(self):
        self.task_text_area = QTextEdit(self)
        self.task_text_area.setReadOnly(True)
        self.task_text_area.move(300, 300)
        self.task_text_area.setFixedWidth(200)

    def _create_menu(self):
        menubar = self.menuBar()

        for menubar_item_descr in menubar_description.values():
            self._create_menu_items(parent=menubar, description=menubar_item_descr)

    def _create_menu_items(self, parent: QMenuBar | QAction | QMenu, description: MenuItem):
        if description.is_action:
            action = QAction(description.label, self)
            action.setData(description.full_code)
            action.triggered.connect(self._handle_action)
            parent.addAction(action)
        else:
            # Есть дочерние элементы, значит это меню
            menu_item = parent.addMenu(description.label)
            for child in description.children:
                self._create_menu_items(menu_item, child)

    def _handle_action(self):
        action = self.sender()

        action_data: str = action.data()
        self.experiment.check_action(action_data)

    def _redraw_statistics(self, statistics_records: list[StatisticsRecord]):
        self.statistics_text_area.clear()
        self.statistics_text_area.setText('\n'.join(map(str, statistics_records)))

    def _redraw_task_text(self, task: str):
        self.task_text_area.clear()
        self.task_text_area.setText(task)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
