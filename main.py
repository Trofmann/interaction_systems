import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
)

from button import DigitButton
from experiment import Experiment
from keyboard import (
    KeyBoard,
    Numpad,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.show()
        self.experiment = None
        self.init_experiments()

    def setup_ui(self):
        self.setWindowTitle('Lab1')
        self.setGeometry(500, 300, 800, 700)

        self.start_experiment_button = QPushButton('Начать эксперимент', self)
        self.start_experiment_button.move(400, 500)
        self.start_experiment_button.setFixedWidth(200)
        self.start_experiment_button.setToolTip('Начать эксперимент')
        self.start_experiment_button.clicked.connect(self.setup_experiment)

    def init_experiments(self):
        self.numpad = Numpad(self)
        self.keyboard = KeyBoard(self)

        self.experiment_1 = Experiment(
            button_sets=(self.keyboard,),
            description='Клавиатура'
        )
        self.experiment_2 = Experiment(
            button_sets=(self.numpad,),
            description='Нумпад',
        )
        self.experiment_3 = Experiment(
            button_sets=(self.numpad, self.keyboard),
            description='Клавиатура + Нумпад'
        )

    def setup_experiment(self):
        if self.experiment is None:
            self.experiment = self._extract_experiment()
        else:
            self.experiment.terminate()
            self.experiment = None
        self.experiment = self._extract_experiment()
        self.experiment.start()

    def _extract_experiment(self) -> Experiment:
        return self.experiment_1

    def keyPressEvent(self, event) -> None:
        button = DigitButton(value=event.key(), is_numpad=bool(event.modifiers() & Qt.KeypadModifier))
        self.experiment.check_button(button=button)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
