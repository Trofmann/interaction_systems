import random
import time
from enum import Enum

from PyQt5.QtCore import QThread

from button import DigitButton
from keyboard import (
    ButtonsSet,
    ButtonLabel,
)
from statistics import StatisticsRecord


class ExperimentState(Enum):
    NOT_ACTIVE = 0
    WAIT_FOR_BUTTON_CHOICE = 1
    WAIT_FOR_BUTTON_PRESS = 2
    FAILED = 3
    COMPLETED = 4


class Experiment(QThread):
    def __init__(self, button_sets: tuple[ButtonsSet, ...], description: str):
        super().__init__()
        self._state = ExperimentState.NOT_ACTIVE

        self._chosen_button: DigitButton | None = None
        self._button_chose_time: float | None = None  # Время выбора кнопки
        self._button_sets: tuple[ButtonsSet, ...] = button_sets
        self._available_buttons: dict[DigitButton, ButtonLabel] = dict()
        for bs in self._button_sets:
            self._available_buttons.update(bs.button_label_dict)

        self.description = description

        self.statistics: list[StatisticsRecord] = []  # Статистика

    def run(self):
        while True:
            if self._state == ExperimentState.WAIT_FOR_BUTTON_CHOICE:
                self._chose_button()

    def _chose_button(self):
        """Выбор кнопки"""
        button, button_label = random.choice(list(self._available_buttons.items()))  # type: DigitButton, ButtonLabel
        self._chosen_button = button
        button_label.highlight()
        # Запомним, когда выбрали кнопку
        self._button_chose_time = time.time()
        # Сразу меняем состояние
        self._state = ExperimentState.WAIT_FOR_BUTTON_PRESS

    def check_button(self, button: DigitButton) -> bool | None:
        # Время нажатия кнопки
        button_pressed_time = time.time()
        if self._state != ExperimentState.WAIT_FOR_BUTTON_PRESS:
            return None
        result = button == self._chosen_button
        if result:
            # Нажали верно
            # Отключаем выделение
            self._available_buttons[self._chosen_button].unhighlight()
            # Нужно, чтоб успело отрисоваться
            time.sleep(0.3)
            self.statistics.append(StatisticsRecord(
                chose_time=self._button_chose_time,
                pressed_time=button_pressed_time,
                is_success=True
            ))
            print(self.statistics[-1])
            # Сбрасываем выбранную кнопку
            self._chosen_button = None
            self._button_chose_time = None
            # Изменяем состояние
            self._state = ExperimentState.WAIT_FOR_BUTTON_CHOICE
        else:
            # Ошиблись
            self._state = ExperimentState.FAILED
            self.statistics.append(StatisticsRecord(
                chose_time=self._button_chose_time,
                pressed_time=button_pressed_time,
                is_success=False
            ))
            print(self.statistics[-1])
            print('Failed')
        return result

    def start(self, *args, **kwargs):
        for button_set in self._button_sets:
            button_set.set_visibility(True)
        self._state = ExperimentState.WAIT_FOR_BUTTON_CHOICE
        super().start(*args, **kwargs)

    def terminate(self):
        self._state = ExperimentState.NOT_ACTIVE
        self._chosen_button = None
        self.statistics = []
        for button_set in self._button_sets:
            button_set.set_visibility(False)
        super().terminate()
