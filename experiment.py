from enum import Enum

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtCore import Qt

from button import DigitButton
from keyboard import ButtonsSet


class ExperimentState(Enum):
    NOT_ACTIVE = 0
    WAIT_FOR_BUTTON_CHOICE = 1
    WAIT_FOR_BUTTON_PRESS = 2
    FAILED = 3
    COMPLETED = 4


class Experiment(QThread):
    button_chosen = pyqtSignal(DigitButton)

    def __init__(self, button_sets: tuple[ButtonsSet, ...]):
        super().__init__()
        self.state = ExperimentState.NOT_ACTIVE
        self.chosen_button: DigitButton | None = None
        self._button_sets: tuple[ButtonsSet, ...] = button_sets

    def run(self):
        while True:
            if self.state == ExperimentState.WAIT_FOR_BUTTON_CHOICE:
                self.chosen_button = DigitButton(Qt.Key_5, False)
                self.button_chosen.emit(self.chosen_button)
                print(f'Выбрана кнопка {self.chosen_button}')
                self.state = ExperimentState.WAIT_FOR_BUTTON_PRESS

    def check_button(self, button: DigitButton) -> bool | None:
        if self.state != ExperimentState.WAIT_FOR_BUTTON_PRESS:
            return None
        result = button == self.chosen_button
        if result:
            self.state = ExperimentState.WAIT_FOR_BUTTON_CHOICE
            print('Success')
        else:
            self.state = ExperimentState.FAILED
            print('Failed')
        return result

    def start(self, *args, **kwargs):
        for button_set in self._button_sets:
            button_set.set_visibility(True)
        self.state = ExperimentState.WAIT_FOR_BUTTON_CHOICE
        super().start(*args, **kwargs)

    def terminate(self):
        self.state = ExperimentState.NOT_ACTIVE
        for button_set in self._button_sets:
            button_set.set_visibility(False)
        super().terminate()
