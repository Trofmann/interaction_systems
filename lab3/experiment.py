from enum import Enum
import random
import time
from PyQt5.QtCore import QThread
from menu import (
    menu_actions,
    MenuItem,
)

__all__ = [
    'Experiment',
]


class ExperimentState(Enum):
    WAIT_FOR_ACTION_CHOICE = 1
    WAIT_FOR_ACTION_PRESSED = 2
    COMPLETED = 3


class Experiment(QThread):
    def __init__(self):
        super().__init__()
        # Все доступные для выбора действия
        self._actions: list[MenuItem] = menu_actions
        # Текущее состояние эксперимента
        self._state: ExperimentState = ExperimentState.WAIT_FOR_ACTION_CHOICE
        # Выбранное действие
        self._chosen_action: MenuItem | None = None
        # Время выбора действия
        self._action_choice_time: float | None = None

    def run(self):
        while True:
            if self._state == ExperimentState.WAIT_FOR_ACTION_CHOICE:
                self._chose_action()

    def _chose_action(self) -> None:
        self._chosen_action = random.choice(self._actions)
        # Запомним, когда выбрали кнопку
        self._action_choice_time = time.time()

        # TODO: Отправлять сигнал на ui, для отрисовки сообщения
        print(self._chosen_action)
        # Сразу изменяем состояние
        self._state = ExperimentState.WAIT_FOR_ACTION_PRESSED

    def check_action(self, code: str) -> None:
        # Сразу запомним время нажатия на действия
        action_pressed_time = time.time()

        # Интересует только одно состояние кнопки
        if self._state != ExperimentState.WAIT_FOR_ACTION_PRESSED:
            return
        result = code == self._chosen_action.full_code
        print(result)
        if result:
            # Нажали верно
            # Сбросим выбранную кнопку и время
            self._chosen_action = None
            self._action_choice_time = None

            # Перевод в следующее состояние
            self._state = ExperimentState.WAIT_FOR_ACTION_CHOICE
