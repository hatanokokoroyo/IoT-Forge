from PySide6.QtWidgets import QVBoxLayout, QLabel, QTextEdit


class LogWidget(QVBoxLayout):
    def __init__(self):
        super().__init__()
        log_label = QLabel("日志输出栏")
        self.addWidget(log_label)
        log_text = QTextEdit()
        log_text.setReadOnly(True)
        self.addWidget(log_text)