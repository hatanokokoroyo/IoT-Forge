from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout

from presentation.gui.widgets.log_widget import LogWidget
from presentation.gui.widgets.menu_widget import MenuWidget
from presentation.gui.widgets.device_widget import DeviceLayout


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("物联网虚拟设备管理器")
        self.resize(1200, 900)

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # 第一行 菜单栏
        menu_layout = MenuWidget()
        main_layout.addLayout(menu_layout, 1)

        # 第二行 左侧树形列表, 右侧设备列表
        main_layout.addLayout(DeviceLayout(), 6)

        # 第三行 底部日志输出栏
        log_layout = LogWidget()
        main_layout.addLayout(log_layout, 3)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()