import PySide6
from PySide6.QtWidgets import QHBoxLayout, QPushButton


class MenuWidget(QHBoxLayout):
    def __init__(self):
        super().__init__()
        empty_button = QPushButton("菜单栏(未实现)")
        empty_button.setEnabled(False)
        empty_button.setFixedWidth(200)
        self.addWidget(empty_button)
        self.addStretch()
