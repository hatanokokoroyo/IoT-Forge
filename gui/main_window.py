from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout

from gui.widgets.log_widget import LogWidget
from gui.widgets.menu_widget import MenuWidget
from gui.widgets.device_widget import DeviceLayout

from repository.device import get_all_devices
from repository.device_model import get_all_device_models
from repository.base import get_session


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("物联网虚拟设备管理器")
        self.resize(1200, 900)

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # 第一行 菜单栏
        self.menu_layout = MenuWidget()
        self.main_layout.addLayout(self.menu_layout, 1)

        # 第二行 左侧树形列表, 右侧设备列表
        self.device_layout = DeviceLayout()
        self.main_layout.addLayout(self.device_layout, 6)

        # 第三行 底部日志输出栏
        self.log_layout = LogWidget()
        self.main_layout.addLayout(self.log_layout, 3)

        # 初始化加载数据
        self.refresh_data()

    def refresh_data(self):
        """查询数据库并刷新 UI"""
        session = get_session()
        try:
            devices = get_all_devices(session)
            models = get_all_device_models(session)

            # 将数据传递给 UI 组件
            self.device_layout.update_data(devices, models)
        except Exception as e:
            print(f"Error loading data: {e}")
        finally:
            session.close()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
