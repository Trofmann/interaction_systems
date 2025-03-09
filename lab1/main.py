import sys
import time
from collections import OrderedDict

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
)

from button import DigitButton
from experiment import Experiment
from keyboard import (
    KeyBoard,
    Numpad,
)
from lab1.statistics import StatisticsRecord
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_experiments()
        self.setup_ui()
        self.show()
        self.experiment: Experiment | None = None

    def setup_ui(self):
        self.setWindowTitle('Lab1')
        self.setGeometry(500, 300, 800, 700)

        # Главный виджет и layout
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)

        self.top_panel = QWidget(self)
        self.top_panel_layout = QHBoxLayout(self.top_panel)
        self.layout.addWidget(self.top_panel)

        # Кнопка начала эксперимента
        self.start_experiment_button = QPushButton('Начать эксперимент', self)
        self.start_experiment_button.move(400, 10)
        self.start_experiment_button.setFixedWidth(200)
        self.start_experiment_button.setToolTip('Начать эксперимент')
        self.start_experiment_button.clicked.connect(self.setup_experiment)

        # Кнопка отрисовки графика
        self.draw_chart_button = QPushButton('График', self)
        self.draw_chart_button.move(600, 10)
        self.draw_chart_button.setFixedWidth(200)
        self.draw_chart_button.setToolTip('График')
        self.draw_chart_button.clicked.connect(self.redraw_chart)

        # Поле выбора эксперимента
        self.experiment_choices_box = QComboBox(self)
        self.experiment_choices_box.setFixedWidth(150)
        self.experiment_choices_box.move(50, 10)
        self.experiment_choices_box.addItems(self.experiments.keys())

        # Панель для таблицы и графика
        self.bottom_panel = QWidget(self)
        self.bottom_panel_layout = QHBoxLayout(self.bottom_panel)
        self.layout.addWidget(self.bottom_panel)

        # Таблица статистики
        self.statistics_table = QTableWidget(self)
        self.statistics_table.setColumnCount(2)
        self.statistics_table.setRowCount(0)
        self.statistics_table.move(400, 50)
        self.statistics_table.setFixedWidth(220)
        self.statistics_table.setFixedHeight(350)
        self.statistics_table.setHorizontalHeaderLabels(['Время реакции', 'Результат'])
        for i in range(2):
            self.statistics_table.setColumnWidth(i, 100)

        # График
        self.figure, self.ax = plt.subplots(figsize=(2, 1))
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setFixedWidth(300)  # Устанавливаем ширину canvas
        self.canvas.setFixedHeight(200)  # Устанавливаем высоту canvas
        self.bottom_panel_layout.addWidget(self.canvas)

    def init_experiments(self):
        self.numpad = Numpad(self)
        self.keyboard = KeyBoard(self)

        self.experiments = OrderedDict()
        self.experiments['Клавиатура (1 клавиша)'] = Experiment(
            button_sets=(self.keyboard,),
            description='Клавиатура (1 клавиша)',
            attempts_count=10,
            is_random_button=False,
        )
        self.experiments['Клавиатура'] = Experiment(
            button_sets=(self.keyboard,),
            description='Клавиатура',
            attempts_count=10,
        )
        self.experiments['Нумпад (1 клавиша)'] = Experiment(
            button_sets=(self.numpad,),
            description='Нумпад (1 клавиша)',
            attempts_count=10,
            is_random_button=False,
        )
        self.experiments['Нумпад'] = Experiment(
            button_sets=(self.numpad,),
            description='Нумпад',
            attempts_count=10,
        )
        self.experiments['Клавиатура + Нумпад'] = Experiment(
            button_sets=(self.numpad, self.keyboard),
            description='Клавиатура + Нумпад',
            attempts_count=10,
        )

    def setup_experiment(self):
        if self.experiment is None:
            self.experiment = self._extract_experiment()
        else:
            self.experiment.terminate()
            # Чтоб поток успел остановиться
            time.sleep(0.3)
            self.experiment.statistics_storage.statistics_changed.disconnect(self.redraw_statistics)
            self.experiment = None
        self.experiment = self._extract_experiment()
        self.experiment.statistics_storage.statistics_changed.connect(self.redraw_statistics)
        self.experiment.start()

    def _extract_experiment(self) -> Experiment:
        return self.experiments[self.experiment_choices_box.currentText()]

    def keyPressEvent(self, event) -> None:
        button = DigitButton(value=event.key(), is_numpad=bool(event.modifiers() & Qt.KeypadModifier))
        self.experiment.check_button(button=button)

    def redraw_statistics(self, statistics_records: list[StatisticsRecord]):
        # Обновление таблицы
        self.statistics_table.setRowCount(len(statistics_records))
        for row, record in enumerate(statistics_records):
            row_data = [
                str(record),
                record.result_verbose,
            ]
            for col, value in enumerate(row_data):
                self.statistics_table.setItem(row, col, QTableWidgetItem(value))

    def redraw_chart(self):
        """Обновление графика"""
        self.ax.clear()  # Очищаем предыдущий график
        if self.experiment is not None and self.experiment.statistics_storage.records:
            reaction_times = [record.reaction_time for record in self.experiment.statistics_storage.records]
            self.ax.plot(reaction_times, marker='o', linestyle='-', color='b')
            self.ax.set_title('Время реакции')
            self.ax.set_xlabel('Попытка')
            self.ax.set_ylabel('Время (мс)')
            self.canvas.draw()  # Перерисовываем canvas


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
