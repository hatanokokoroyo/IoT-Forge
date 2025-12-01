import sys
from PySide6.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget, QMainWindow

class BasicTreeDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("教程 1: QTreeWidget 基础结构")
        self.resize(600, 400)

        # 主布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # 1. 创建 QTreeWidget
        self.tree = QTreeWidget()
        # 设置列数，这里我们只需要一列来展示自定义的复杂内容，
        # 但为了演示层级，QTreeWidget默认就是支持层级的。
        self.tree.setColumnCount(1)
        self.tree.setHeaderLabels(["设备列表"])
        
        layout.addWidget(self.tree)

        # 2. 初始化数据
        self.init_data()

    def init_data(self):
        """
        模拟添加网关和子设备数据
        """
        # 模拟数据
        devices = [
            {
                "name": "网关 A",
                "ip": "192.168.1.10",
                "status": "Online",
                "children": [
                    {"name": "传感器 A-1", "ip": "192.168.1.11", "status": "Online"},
                    {"name": "传感器 A-2", "ip": "192.168.1.12", "status": "Offline"},
                ]
            },
            {
                "name": "网关 B",
                "ip": "192.168.1.20",
                "status": "Offline",
                "children": [
                    {"name": "控制器 B-1", "ip": "192.168.1.21", "status": "Offline"},
                ]
            }
        ]

        for device_data in devices:
            # 创建父节点 (网关)
            gateway_item = QTreeWidgetItem(self.tree)
            gateway_item.setText(0, f"{device_data['name']} ({device_data['ip']})")
            
            # 存储原始数据，以便后续Delegate使用 (setData 是关键)
            # Qt.UserRole 是自定义数据的起始角色
            # 这里我们简单演示，后续教程会深入使用
            
            for child_data in device_data["children"]:
                # 创建子节点 (子设备)
                child_item = QTreeWidgetItem(gateway_item)
                child_item.setText(0, f"{child_data['name']} ({child_data['ip']})")

        # 展开所有节点
        self.tree.expandAll()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BasicTreeDemo()
    window.show()
    sys.exit(app.exec())
