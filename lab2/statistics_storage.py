from position import Position

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

    @property
    def reaction_time(self):
        return 0


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


class StatisticsStorage:
    def __init__(self):
        self._records: list[StatisticsRecord] = []

    def add_record(self, record: StatisticsRecord):
        self._records.append(record)
        print(record.time_record.reaction_time)
        print(record.fitts_record.reaction_time)

    @property
    def records(self) -> list[StatisticsRecord]:
        return self._records

    def __len__(self) -> int:
        return len(self._records)
