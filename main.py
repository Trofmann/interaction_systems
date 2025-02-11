import sys

from experiment import experiment_1
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtCore import Qt

BUTTON_WIDTH = 20
BUTTON_HEIGHT = 20


def _generate_button(
        window: QMainWindow,
        label: str,
        x_pos: int,
        y_pos: int,
        width: int = BUTTON_WIDTH,
        height: int = BUTTON_HEIGHT
) -> QLabel:
    label = QLabel(label, window)
    label.setStyleSheet('border: 1px solid black;')
    label.setGeometry(x_pos, y_pos, width, height)
    return label


def _generate_keyboard(window: QMainWindow) -> dict[tuple[int, bool], QLabel]:
    x_pos = 50
    y_pos = 50

    return {
        (key, False): _generate_button(
            window,
            str(key - Qt.Key_0),
            x_pos + (BUTTON_WIDTH + 5) * (key - Qt.Key_0),
            y_pos,
        )
        for key in range(Qt.Key_0, Qt.Key_9 + 1)
    }


def _generate_numpad(window: QMainWindow) -> dict[tuple[int, bool], QLabel]:
    x_pos = 50
    y_pos = 350

    common_buttons = dict()
    for key in range(Qt.Key_1, Qt.Key_9 + 1):
        row = (key - 1) // 3 - 16
        column = (key - 1 - 3 * row) % 3
        btn_x_pos = x_pos + (BUTTON_WIDTH + 5) * column
        # Минус потому что движемся вверх
        btn_y_pos = y_pos - (BUTTON_HEIGHT + 5) * row
        common_buttons[(key, True)] = _generate_button(
            window,
            str(key - Qt.Key_0),
            x_pos=btn_x_pos,
            y_pos=btn_y_pos,
        )
    return common_buttons


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

        self.keyboard = _generate_keyboard(self)
        self.numpad = _generate_numpad(self)

    def setup_experiment(self):
        if self.experiment is None:
            self.experiment = experiment_1
        else:
            self.experiment.button_chosen.disconnect()
        self.experiment.start()
        self.experiment.button_chosen.connect(self.highlight_key)

    def highlight_key(self, button: int, is_numpad: bool):
        print(button, is_numpad)

    def keyPressEvent(self, event) -> None:
        self.experiment.check_button(
            button=event.key(),
            is_numpad=bool(event.modifiers() & Qt.KeypadModifier)
        )


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
