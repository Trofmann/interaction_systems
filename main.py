import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow

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
        self.setup_experiment()

    def setup_ui(self):
        self.setWindowTitle('Lab1')
        self.setGeometry(500, 300, 800, 700)

    def init_experiments(self):
        self.numpad = Numpad(self)
        self.keyboard = KeyBoard(self)

        self.experiment_1 = Experiment(button_sets=(self.numpad, self.keyboard))

    def setup_experiment(self):
        if self.experiment is None:
            self.experiment = self.experiment_1
        else:
            self.experiment.terminate()
        self.experiment.start()

    def keyPressEvent(self, event) -> None:
        button = DigitButton(value=event.key(), is_numpad=bool(event.modifiers() & Qt.KeypadModifier))
        self.experiment.check_button(button=button)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
