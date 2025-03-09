from base_task import BaseTask


class Task1(BaseTask):
    def _get_cursor_x(self, left, top, right, bottom):
        return left + (right - left) // 2

    def _get_cursor_y(self, left, top, right, bottom):
        return top + (bottom - top) // 2


Task1().run()
