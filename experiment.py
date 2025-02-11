from dataclasses import dataclass

from PyQt5.QtCore import QThread


class Experiment(QThread):
    def __init__(self):
        super().__init__()


exp_1 = Experiment(
)
