import sys
import time

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QComboBox,
    QTableWidget,
)

from button import DigitButton
from experiment import Experiment
from keyboard import (
    KeyBoard,
    Numpad,
)
from collections import OrderedDict


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_experiments()
        self.setup_ui()
        self.show()
        self.experiment = None

    def setup_ui(self):
        self.setWindowTitle('Lab1')
        self.setGeometry(500, 300, 800, 700)

        self.start_experiment_button = QPushButton('Начать эксперимент', self)
        self.start_experiment_button.move(400, 10)
        self.start_experiment_button.setFixedWidth(200)
        self.start_experiment_button.setToolTip('Начать эксперимент')
        self.start_experiment_button.clicked.connect(self.setup_experiment)

        self.experiment_choices_box = QComboBox(self)
        self.experiment_choices_box.setFixedWidth(150)
        self.experiment_choices_box.move(50, 10)
        self.experiment_choices_box.addItems(self.experiments.keys())

        self.statistics_table = QTableWidget(self)
        self.statistics_table.setColumnCount(3)
        self.statistics_table.setRowCount(0)
        self.statistics_table.move(400, 50)
        self.statistics_table.setFixedWidth(300)
        self.statistics_table.setFixedHeight(200)
        self.statistics_table.setHorizontalHeaderLabels(['№', 'Время реакции', 'Результат'])
        for i in range(3):
            self.statistics_table.setColumnWidth(i, 100)

    def init_experiments(self):
        self.numpad = Numpad(self)
        self.keyboard = KeyBoard(self)

        self.experiments = OrderedDict()
        self.experiments['Клавиатура'] = Experiment(
            button_sets=(self.keyboard,),
            description='Клавиатура'
        )
        self.experiments['Нумпад'] = Experiment(
            button_sets=(self.numpad,),
            description='Нумпад',
        )
        self.experiments['Клавиатура + Нумпад'] = Experiment(
            button_sets=(self.numpad, self.keyboard),
            description='Клавиатура + Нумпад'
        )

    def setup_experiment(self):
        if self.experiment is None:
            self.experiment = self._extract_experiment()
        else:
            self.experiment.terminate()
            # Чтоб поток успел остановиться
            time.sleep(0.3)
            self.experiment = None
        self.experiment = self._extract_experiment()
        self.experiment.start()

    def _extract_experiment(self) -> Experiment:
        return self.experiments[self.experiment_choices_box.currentText()]

    def keyPressEvent(self, event) -> None:
        button = DigitButton(value=event.key(), is_numpad=bool(event.modifiers() & Qt.KeypadModifier))
        self.experiment.check_button(button=button)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
