import random

from base_task import BaseTask


class Task3(BaseTask):
    
    def _get_cursor_x(self, left, top, right, bottom):
        """Получение координаты x курсора"""
        return random.randint(left, right)

    def _get_cursor_y(self, left, top, right, bottom):
        """Получение координты y курсора"""
        return random.randint(top, bottom)


Task3().run()
