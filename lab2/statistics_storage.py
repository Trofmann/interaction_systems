__all__ = [
    'FittsRecord',
    'StatisticsRecord',
    'StatisticsStorage',
]


class FittsRecord:
    def __init__(self, button_x: int, button_y: int, cursor_x: int, cursor_y: int):
        self.button_x = button_x
        self.button_y = button_y
        self.cursor_x = cursor_x
        self.cursor_y = cursor_y

    @property
    def reaction_time(self):
        raise NotImplementedError()


class StatisticsRecord:
    def __init__(self, pos_chose_time: float, button_pressed_time: float):
        self.pos_chose_time = pos_chose_time
        self.button_pressed_time = button_pressed_time

    @property
    def reaction_time(self) -> float:
        return self.button_pressed_time - self.pos_chose_time


class StatisticsStorage:
    def __init__(self):
        self._records: list[StatisticsRecord] = []

    def add_record(self, record: StatisticsRecord):
        self._records.append(record)
        print(record.reaction_time)

    @property
    def records(self) -> list[StatisticsRecord]:
        return self._records

    def __len__(self) -> int:
        return len(self._records)
