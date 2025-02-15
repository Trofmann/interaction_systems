import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow

from button import DigitButton
from experiment import experiment_1
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
        self.setup_experiment()

    def setup_ui(self):
        self.setWindowTitle('Lab1')
        self.setGeometry(500, 300, 800, 700)

        self.keyboard = KeyBoard(self)
        self.keyboard.draw()
        self.numpad = Numpad(self)
        self.numpad.draw()

    def setup_experiment(self):
        if self.experiment is None:
            self.experiment = experiment_1
        else:
            self.experiment.button_chosen.disconnect()
        self.experiment.start()
        self.experiment.button_chosen.connect(self.highlight_key)

    def highlight_key(self, button: DigitButton):
        print(f'Подсвечена кнопка {button}')

    def keyPressEvent(self, event) -> None:
        button = DigitButton(value=event.key(), is_numpad=bool(event.modifiers() & Qt.KeypadModifier))
        self.experiment.check_button(button=button)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
