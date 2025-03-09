from position import Position


class WindowSettings:
    HEIGHT = 400
    WIDTH = 600
    TITLE = 'Окно'


class ButtonSettings:
    TITLE = 'Кнопка'
    POSITION = Position(80, 150)
    WIDTH = 100
    HEIGHT = 30

    @classmethod
    def get_center_position(cls) -> Position:
        return Position(cls.POSITION.x + cls.WIDTH // 2, cls.POSITION.y + cls.HEIGHT // 2)


class TextAreaSettings:
    POSITION = Position(200, 200)
    WIDTH = 360
    HEIGHT = 150
