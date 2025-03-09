from abc import ABC, abstractmethod
from enum import Enum

import win32api
import win32gui
import win32con
from settings import (
    WindowSettings,
    ButtonSettings,
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
            ButtonSettings.POS_X,
            ButtonSettings.POS_Y,
            ButtonSettings.WIDTH,
            ButtonSettings.HEIGHT,
            self.hwnd,
            1,  # ID кнопки
            self.wc.hInstance,
            None
        )
        self.state = State.NOT_STARTED

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
        if self.state not in {State.NOT_STARTED, State.WAITING_FOR_BUTTON_PRESS}:
            # Обрабатываем нажатие только если ещё не начали, или ожидаем нажатие кнопки
            return None
        self._move_cursor(hwnd)

    # Функция для перемещения курсора в случайное место внутри окна
    def _move_cursor(self, hwnd):
        """Перемещение курсора"""
        rect = win32gui.GetWindowRect(hwnd)
        x = self._get_cursor_x(*rect)
        y = self._get_cursor_y(*rect)
        # Переместить курсор
        win32api.SetCursorPos((x, y))

    def run(self):
        """Запуск лабораторной работы"""

        # Показать окно
        win32gui.ShowWindow(self.hwnd, win32con.SW_SHOW)
        win32gui.UpdateWindow(self.hwnd)

        # Цикл обработки сообщений
        win32gui.PumpMessages()
