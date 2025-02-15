__all__ = [
    'StatisticsRecord',
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
