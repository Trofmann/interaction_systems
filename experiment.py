from enum import Enum

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtCore import Qt


class ExperimentState(Enum):
    NOT_ACTIVE = 0
    WAIT_FOR_BUTTON_CHOICE = 1
    WAIT_FOR_BUTTON_PRESS = 2
    FAILED = 3
    COMPLETED = 4


class Experiment(QThread):
    button_chosen = pyqtSignal(int, bool)

    def __init__(self):
        super().__init__()
        self.state = ExperimentState.NOT_ACTIVE
        self.chosen_button = None
        self.is_numpad = False

    def run(self):
        while True:
            if self.state == ExperimentState.WAIT_FOR_BUTTON_CHOICE:
                self.chosen_button = Qt.Key_5
                self.button_chosen.emit(self.chosen_button, False)
                self.state = ExperimentState.WAIT_FOR_BUTTON_PRESS

    def check_button(self, button: int, is_numpad: bool) -> bool | None:
        if self.state != ExperimentState.WAIT_FOR_BUTTON_PRESS:
            return None
        result = button == self.chosen_button and is_numpad == self.is_numpad
        if result:
            self.state = ExperimentState.WAIT_FOR_BUTTON_PRESS
        else:
            self.state = ExperimentState.FAILED
        return result

    def start(self, *args, **kwargs):
        self.state = ExperimentState.WAIT_FOR_BUTTON_CHOICE
        super().start(*args, **kwargs)

    def terminate(self):
        self.state = ExperimentState.NOT_ACTIVE
        super().terminate()


experiment_1 = Experiment()
