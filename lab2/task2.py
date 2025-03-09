import random

from base_task import BaseTask


class Task2(BaseTask):
    def _get_cursor_x(self, left, top, right, bottom):
        return random.randint(left, right)

    def _get_cursor_y(self, left, top, right, bottom):
        return top + (bottom - top) // 2


Task2().run()