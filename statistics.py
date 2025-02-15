from PyQt5.QtCore import (
    pyqtSignal,
    QObject,
)

__all__ = [
    'StatisticsRecord',
    'StatisticsStorage',
]


class StatisticsRecord:
    """Запись статистики"""

    def __init__(self, chose_time: float, pressed_time: float, is_success: bool):
        self.chose_time = chose_time
        self.pressed_time = pressed_time
        self.is_success = is_success

    def __str__(self):
        return str(round(self.reaction_time, 2))

    @property
    def reaction_time(self) -> float:
        return self.pressed_time - self.chose_time

    @property
    def result_verbose(self) -> str:
        return 'Успешно' if self.is_success else 'Ошибка'


class StatisticsStorage(QObject):
    statistics_changed = pyqtSignal(list)  # Дженерики нельзя

    def __init__(self):
        super().__init__()
        self._records: list['StatisticsRecord'] = []

    def _emit_signal(self):
        self.statistics_changed.emit(self._records)

    def add_record(self, record: StatisticsRecord) -> None:
        self._records.append(record)
        self._emit_signal()

    def flush(self) -> None:
        self._records = []
        self._emit_signal()

    def __len__(self):
        return len(self._records)
