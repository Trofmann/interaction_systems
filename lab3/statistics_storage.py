from PyQt5.QtCore import (
    QObject,
    pyqtSignal,
)
import math
from menu import MenuItem, menubar_description

__all__ = [
    'TimeRecord',
    'HikRecord',
    'StatisticsRecord',
    'StatisticsStorage',
]


class HikRecord:
    def __init__(self, menu_item: MenuItem):
        self.menu_item = menu_item
        self.a = 50
        self.b = 100

    def _calc(self, menu_item: MenuItem) -> float:
        if parent := menu_item.parent:
            count_ = len(parent.children)
            return (self.a + self.b * math.log(count_ + 1, 2)) / 1000 + self._calc(parent)
        else:
            count_ = len(menubar_description)
            return (self.a + self.b * math.log(count_ + 1, 2)) / 1000

    @property
    def reaction_time(self) -> float:
        return self._calc(self.menu_item)


class TimeRecord:
    def __init__(self, chose_time: float, pressed_time: float):
        self.chose_time = chose_time
        self.pressed_time = pressed_time

    @property
    def reaction_time(self) -> float:
        return self.pressed_time - self.chose_time


class StatisticsRecord:
    def __init__(self, time_record: TimeRecord, hik_record: HikRecord):
        self.time_record = time_record
        self.hik_record = hik_record

    def __str__(self):
        hik = f'Хик: {round(self.hik_record.reaction_time, 2)}'
        real_time = f'Реальное время: {round(self.time_record.reaction_time, 2)}'
        return f'{hik}; {real_time}'


class StatisticsStorage(QObject):
    statistics_changed = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self._records: list[StatisticsRecord] = []

    def add_record(self, record: StatisticsRecord):
        self._records.append(record)
        self.statistics_changed.emit(self._records)

    @property
    def records(self) -> list[StatisticsRecord]:
        return self._records

    def __len__(self) -> int:
        return len(self._records)

    def __str__(self):
        return '\r\n'.join(map(str, self._records))
