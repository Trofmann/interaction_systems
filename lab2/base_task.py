import random
import time
from abc import (
    ABC,
    abstractmethod,
)
from enum import Enum

import win32api
import win32con
import win32gui

from position import Position
from settings import (
    WindowSettings,
    ButtonSettings,
    TextAreaSettings,
)
from statistics_storage import (
    StatisticsStorage,
    StatisticsRecord,
    FittsRecord,
    TimeRecord,
)

__all__ = [
    'BaseTask'
]


class State(Enum):
    NOT_STARTED = -1
    WAITING_FOR_POSITION_SELECTION = 0
    WAITING_FOR_BUTTON_PRESS = 1
    COMPLETED = 2


class BaseTask(ABC):
    def __init__(self):
        self.wc = self._init_window_class()

        # Создание окна
        self.hwnd = win32gui.CreateWindow(
            self.wc.lpszClassName,
            WindowSettings.TITLE,
            win32con.WS_OVERLAPPEDWINDOW,
            win32con.CW_USEDEFAULT,
            win32con.CW_USEDEFAULT,
            WindowSettings.WIDTH,
            WindowSettings.HEIGHT,
            0,
            0,
            self.wc.hInstance,
            None
        )

        # Создание кнопки
        self.button_hwnd = win32gui.CreateWindow(
            'BUTTON',
            ButtonSettings.TITLE,
            win32con.WS_CHILD | win32con.WS_VISIBLE | win32con.BS_PUSHBUTTON,
            ButtonSettings.POSITION.x,
            ButtonSettings.POSITION.y,
            ButtonSettings.WIDTH,
            ButtonSettings.HEIGHT,
            self.hwnd,
            1,  # ID кнопки
            self.wc.hInstance,
            None
        )

        self.text_area_hwnd = win32gui.CreateWindow(
            "EDIT",  # Класс элемента Edit
            "",  # Начальный текст
            win32con.WS_CHILD | win32con.WS_VISIBLE | win32con.WS_VSCROLL | win32con.ES_MULTILINE | win32con.ES_READONLY,
            TextAreaSettings.POSITION.x,
            TextAreaSettings.POSITION.y,
            TextAreaSettings.WIDTH,
            TextAreaSettings.HEIGHT,
            self.hwnd,
            2,  # ID текстовой области
            self.wc.hInstance,
            None
        )

        self.state: State = State.NOT_STARTED
        self._position_chose_time: float | None = None  # Время выбора позиции курсора
        self._cursor_position: Position | None = None  # Позиция курсора
        self.statistics_storage: StatisticsStorage = StatisticsStorage()

    def _init_window_class(self):
        """Инициализация класса окна"""
        wc = win32gui.WNDCLASS()
        wc.hInstance = win32api.GetModuleHandle(None)
        wc.lpszClassName = "WindowClass"
        wc.lpfnWndProc = self._button_event_handler
        win32gui.RegisterClass(wc)
        return wc

    def _button_event_handler(self, hwnd, msg, wParam, lParam):
        """Обработка нажатия кнопки"""
        if msg == win32con.WM_COMMAND:
            if wParam == 1:  # ID кнопки
                self._process_button_pressed(hwnd)
        elif msg == win32con.WM_DESTROY:
            win32gui.PostQuitMessage(0)
        return win32gui.DefWindowProc(hwnd, msg, wParam, lParam)

    @abstractmethod
    def _get_cursor_x(self, left, top, right, bottom):
        """Получение координаты x курсора"""

    @abstractmethod
    def _get_cursor_y(self, left, top, right, bottom):
        """Получение координаты y курсора"""

    def _process_button_pressed(self, hwnd) -> None:
        """Обработка нажатия кнопки мыши"""
        # Сразу запомним время нажатия кнопки
        button_pressed_time = time.time()
        if self.state not in {State.NOT_STARTED, State.WAITING_FOR_BUTTON_PRESS}:
            # Обрабатываем нажатие только если ещё не начали, или ожидаем нажатие кнопки
            return
        if self.state == State.WAITING_FOR_BUTTON_PRESS:
            # Ожидали нажатия кнопки
            # Запоминаем статистические данные
            self.statistics_storage.add_record(StatisticsRecord(
                time_record=TimeRecord(
                    pos_chose_time=self._position_chose_time,
                    button_pressed_time=button_pressed_time,
                ),
                fitts_record=FittsRecord(
                    button_position=ButtonSettings.get_center_position(),
                    cursor_position=self._cursor_position,
                )
            ))
            win32gui.SetWindowText(self.text_area_hwnd, str(self.statistics_storage))
            if len(self.statistics_storage) == 10:
                # Эксперимент завершён
                self.state = State.COMPLETED
                win32gui.SetWindowText(self.text_area_hwnd, f'{str(self.statistics_storage)}\r\nЗавершено', )
                return
            win32gui.SetWindowText(self.text_area_hwnd, str(self.statistics_storage))

        # Ожидаем случайное время
        self.state = State.WAITING_FOR_POSITION_SELECTION
        time.sleep(random.randint(1, 300) / 100)
        # Перемещаем курсор
        self._move_cursor(hwnd)
        # Запоминаем время, когда переместили курсор
        self._position_chose_time = time.time()

        # Позиция выбрана, ожидаем нажатия
        self.state = State.WAITING_FOR_BUTTON_PRESS

    # Функция для перемещения курсора в случайное место внутри окна
    def _move_cursor(self, hwnd):
        """Перемещение курсора"""
        rect = win32gui.GetWindowRect(hwnd)
        x = self._get_cursor_x(*rect)
        y = self._get_cursor_y(*rect)
        # Запоминаем позицию курсора
        self._cursor_position = Position(x, y)
        # Переместить курсор
        win32api.SetCursorPos((self._cursor_position.x, self._cursor_position.y))

    def run(self):
        """Запуск лабораторной работы"""

        # Показать окно
        win32gui.ShowWindow(self.hwnd, win32con.SW_SHOW)
        win32gui.UpdateWindow(self.hwnd)

        # Цикл обработки сообщений
        win32gui.PumpMessages()
