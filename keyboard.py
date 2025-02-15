from abc import ABC, abstractmethod

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QMainWindow,
    QLabel,
)

from button import DigitButton

BUTTON_WIDTH = 20
BUTTON_HEIGHT = 20
BUTTON_BORDER = 'border: 1px solid black'

__all__ = [
    'ButtonLabel',
    'ButtonsSet',
    'KeyBoard',
    'Numpad',
]


class ButtonLabel(QLabel):
    def highlight(self) -> None:
        self.setStyleSheet(f'background-color:red;{BUTTON_BORDER}')

    def unhighlight(self) -> None:
        self.setStyleSheet(BUTTON_BORDER)

    def reset_style_sheet(self) -> None:
        self.setStyleSheet(BUTTON_BORDER)


class ButtonsSet(ABC):
    def __init__(self, window: QMainWindow):
        self.window = window
        self.buttons: tuple[DigitButton, ...] = self._get_buttons()
        self.button_label_dict: dict[DigitButton, ButtonLabel] = self._get_button_label_dict()

    @abstractmethod
    def _get_buttons(self) -> tuple[DigitButton, ...]:
        pass

    @abstractmethod
    def _get_button_label_dict(self) -> dict[DigitButton, ButtonLabel]:
        pass

    def _generate_button(
            self,
            label: str,
            x_pos: int,
            y_pos: int,
            width: int = BUTTON_WIDTH,
            height: int = BUTTON_HEIGHT
    ) -> ButtonLabel:
        label = ButtonLabel(label, self.window)
        label.setStyleSheet(BUTTON_BORDER)
        label.setGeometry(x_pos, y_pos, width, height)
        label.setVisible(False)  # Используется при инициализации
        return label

    def set_visibility(self, visible: bool) -> None:
        for label in self.button_label_dict.values():
            label.setVisible(visible)
            if not visible:
                label.reset_style_sheet()


class KeyBoard(ButtonsSet):
    def _get_buttons(self) -> tuple[DigitButton, ...]:
        return tuple([
            DigitButton(key, False)
            for key in range(Qt.Key_0, Qt.Key_9 + 1)
        ])

    def _get_button_label_dict(self) -> dict[DigitButton, ButtonLabel]:
        x_pos = 50
        y_pos = 50

        return {
            button: self._generate_button(
                str(button.value - Qt.Key_0),
                x_pos + (BUTTON_WIDTH + 5) * (button.value - Qt.Key_0),
                y_pos,
            )
            for button in self.buttons
        }


class Numpad(ButtonsSet):
    def _get_buttons(self) -> tuple[DigitButton, ...]:
        return tuple([
            DigitButton(key, True)
            for key in range(Qt.Key_0, Qt.Key_9 + 1)
        ])

    def _get_button_label_dict(self) -> dict[DigitButton, ButtonLabel]:
        x_pos = 50
        y_pos = 350

        common_buttons = dict()
        for button in self.buttons[1::]:
            value = button.value
            row = (value - 1) // 3 - 16
            column = (value - 1 - 3 * row) % 3
            btn_x_pos = x_pos + (BUTTON_WIDTH + 5) * column
            # Минус потому что движемся вверх
            btn_y_pos = y_pos - (BUTTON_HEIGHT + 5) * row
            common_buttons[button] = self._generate_button(
                str(value - Qt.Key_0),
                x_pos=btn_x_pos,
                y_pos=btn_y_pos,
            )
        return common_buttons
