import random
import time
from enum import Enum

from PyQt5.QtCore import QThread

from button import DigitButton
from keyboard import (
    ButtonsSet,
    ButtonLabel,
)


class ExperimentState(Enum):
    NOT_ACTIVE = 0
    WAIT_FOR_BUTTON_CHOICE = 1
    WAIT_FOR_BUTTON_PRESS = 2
    FAILED = 3
    COMPLETED = 4


class Experiment(QThread):
    def __init__(self, button_sets: tuple[ButtonsSet, ...]):
        super().__init__()
        self.state = ExperimentState.NOT_ACTIVE

        self.chosen_button: DigitButton | None = None
        self._button_sets: tuple[ButtonsSet, ...] = button_sets
        self.available_buttons: dict[DigitButton, ButtonLabel] = dict()
        for bs in self._button_sets:
            self.available_buttons.update(bs.button_label_dict)

    def run(self):
        while True:
            if self.state == ExperimentState.WAIT_FOR_BUTTON_CHOICE:
                self._chose_button()

    def _chose_button(self):
        """Выбор кнопки"""
        button, button_label = random.choice(list(self.available_buttons.items()))  # type: DigitButton, ButtonLabel
        self.chosen_button = button
        button_label.highlight()
        # Сразу меняем состояние
        self.state = ExperimentState.WAIT_FOR_BUTTON_PRESS
        print(f'Выбрана кнопка {self.chosen_button}')

    def check_button(self, button: DigitButton) -> bool | None:
        if self.state != ExperimentState.WAIT_FOR_BUTTON_PRESS:
            return None
        result = button == self.chosen_button
        if result:
            # Нажали верно
            # Отключаем выделение
            self.available_buttons[self.chosen_button].unhighlight()
            # Нужно, чтоб успело отрисоваться
            time.sleep(0.3)
            # Сбрасываем выбранную кнопку
            self.chosen_button = None
            # Изменяем состояние
            self.state = ExperimentState.WAIT_FOR_BUTTON_CHOICE
            print('Success')
        else:
            # Ошиблись
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
