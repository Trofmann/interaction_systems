import math

from position import Position
from settings import ButtonSettings

__all__ = [
    'FittsRecord',
    'TimeRecord',
    'StatisticsRecord',
    'StatisticsStorage',
]


class FittsRecord:
    def __init__(self, button_position: Position, cursor_position: Position):
        self.button_position = button_position
        self.cursor_position = cursor_position

        self.hardware_start_time: float = 0  # a
        self.hardware_speed: float = 1  # b
        self.button_width = ButtonSettings.WIDTH  # W

    @property
    def _distance(self) -> float:
        # D
        return math.sqrt(
            (self.button_position.x - self.cursor_position.x) ** 2
            + (self.button_position.y - self.cursor_position.y) ** 2
        )

    @property
    def reaction_time(self) -> float:
        # a + blog2(D/W + 1)
        return (
                self.hardware_start_time
                + self.hardware_speed
                * (
                    math.log(
                        ((self._distance / self.button_width) + 1),
                        2
                    )
                )
        )


class TimeRecord:
    def __init__(self, pos_chose_time: float, button_pressed_time: float):
        self.pos_chose_time = pos_chose_time
        self.button_pressed_time = button_pressed_time

    @property
    def reaction_time(self) -> float:
        return self.button_pressed_time - self.pos_chose_time


class StatisticsRecord:
    def __init__(self, time_record: TimeRecord, fitts_record: FittsRecord):
        self.time_record = time_record
        self.fitts_record = fitts_record

    def __str__(self):
        fitts = f'Фиттс: {round(self.fitts_record.reaction_time, 2)}'
        real_time = f'Реальное время: {round(self.time_record.reaction_time, 2)}'
        return f'{fitts}; {real_time}'


class StatisticsStorage:
    def __init__(self):
        self._records: list[StatisticsRecord] = []

    def add_record(self, record: StatisticsRecord):
        self._records.append(record)

    @property
    def records(self) -> list[StatisticsRecord]:
        return self._records

    def __len__(self) -> int:
        return len(self._records)

    def __str__(self):
        return '\r\n'.join(map(str, self._records))
