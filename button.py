__all__ = [
    'DigitButton',
]


class DigitButton:
    def __init__(self, value: int, is_numpad: bool):
        self.value = value
        self.is_numpad = is_numpad

    def __hash__(self):
        return hash((self.value, self.is_numpad))
