import sys

from PyQt5.QtWidgets import QApplication

from base_task import BaseTaskWindow


class Task1Window(BaseTaskWindow):
    pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = Task1Window()
    main_window.show()
    sys.exit(app.exec_())
