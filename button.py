__all__ = [
    'DigitButton',
]


class DigitButton:
    def __init__(self, value: int, is_numpad: bool):
        self.value = value
        self.is_numpad = is_numpad

    def __str__(self):
        return f'{self.value} {self.is_numpad}'

    def __eq__(self, other) -> bool:
        if isinstance(other, DigitButton):
            return self.value == other.value and self.is_numpad == other.is_numpad
        return False

    def __hash__(self):
        return hash((self.value, self.is_numpad))
