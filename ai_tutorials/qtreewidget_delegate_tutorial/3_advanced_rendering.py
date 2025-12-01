import sys
from PySide6.QtWidgets import (QApplication, QTreeWidget, QTreeWidgetItem, 
                               QVBoxLayout, QWidget, QMainWindow, QStyledItemDelegate, QStyle)
from PySide6.QtCore import Qt, QRect, QSize
from PySide6.QtGui import QPainter, QColor, QPen, QFont, QBrush

# 定义自定义数据角色
ROLE_DEVICE_NAME = Qt.UserRole + 1
ROLE_DEVICE_IP = Qt.UserRole + 2
ROLE_DEVICE_STATUS = Qt.UserRole + 3
ROLE_IS_GATEWAY = Qt.UserRole + 4

class DeviceDelegate(QStyledItemDelegate):
    def sizeHint(self, option, index):
        """
        告诉 View 每个 Item 需要多大的空间。
        """
        return QSize(option.rect.width(), 60) # 固定高度 60

    def paint(self, painter: QPainter, option, index):
        painter.save()
        
        # 获取数据
        name = index.data(ROLE_DEVICE_NAME)
        ip = index.data(ROLE_DEVICE_IP)
        status = index.data(ROLE_DEVICE_STATUS)
        is_gateway = index.data(ROLE_IS_GATEWAY)

        rect = option.rect
        
        # --- 背景绘制 ---
        bg_color = QColor("#ffffff")
        if option.state & QStyle.State_Selected:
            bg_color = QColor("#e6f7ff")
        elif option.state & QStyle.State_MouseOver: # 需要开启 setMouseTracking
            bg_color = QColor("#f5f5f5")
            
        painter.fillRect(rect, bg_color)

        # --- 内容布局计算 ---
        # 缩进：根据层级缩进，TreeWidget 会自动处理缩进，但在 Delegate 中我们需要手动处理内容偏移
        # 或者我们可以让 TreeWidget 画分支线，我们只画内容。
        # 这里我们简单处理：假设只有一列，我们自己控制缩进。
        # 实际上 QTreeWidget 的 indentation 属性控制缩进，但在 paint 中我们需要自己算 x 偏移
        # 简单的做法是利用 option.rect 的 x 坐标，通常 View 会传给我们正确的 x
        
        content_rect = QRect(rect)
        
        # 绘制图标 (左侧)
        icon_rect = QRect(content_rect.left() + 10, content_rect.top() + 15, 30, 30)
        icon_color = QColor("#4CAF50") if status == "Online" else QColor("#9E9E9E")
        painter.setBrush(QBrush(icon_color))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(icon_rect) # 画个圆圈代表图标
        
        # 绘制设备名称 (粗体)
        name_rect = QRect(icon_rect.right() + 15, content_rect.top() + 10, 200, 20)
        font_name = QFont()
        font_name.setBold(True)
        font_name.setPointSize(10)
        painter.setFont(font_name)
        painter.setPen(QColor("#333333"))
        painter.drawText(name_rect, Qt.AlignVCenter | Qt.AlignLeft, name)
        
        # 绘制 IP 地址 (灰色小字)
        ip_rect = QRect(icon_rect.right() + 15, name_rect.bottom() + 5, 200, 15)
        font_ip = QFont()
        font_ip.setPointSize(8)
        painter.setFont(font_ip)
        painter.setPen(QColor("#888888"))
        painter.drawText(ip_rect, Qt.AlignVCenter | Qt.AlignLeft, f"IP: {ip}")

        # 绘制状态标签 (右侧)
        status_rect = QRect(content_rect.right() - 80, content_rect.top() + 20, 60, 20)
        painter.setPen(icon_color)
        painter.drawText(status_rect, Qt.AlignVCenter | Qt.AlignRight, status)

        # 绘制分割线
        painter.setPen(QPen(QColor("#eeeeee")))
        painter.drawLine(rect.bottomLeft(), rect.bottomRight())

        painter.restore()

class AdvancedRenderDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("教程 3: 复杂内容绘制 (高性能列表核心)")
        self.resize(700, 500)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.tree = QTreeWidget()
        self.tree.setColumnCount(1)
        self.tree.setHeaderLabels(["设备详情"])
        self.tree.setIndentation(20) # 设置层级缩进
        
        # 开启鼠标追踪，以便 Delegate 感知 hover 状态 (如果需要)
        self.tree.setMouseTracking(True)

        self.delegate = DeviceDelegate()
        self.tree.setItemDelegate(self.delegate)

        layout.addWidget(self.tree)
        self.init_data()

    def init_data(self):
        devices = [
            {"name": "核心网关 A", "ip": "192.168.1.1", "status": "Online", "children": [
                {"name": "温湿度传感器 01", "ip": "192.168.1.101", "status": "Online"},
                {"name": "温湿度传感器 02", "ip": "192.168.1.102", "status": "Offline"},
            ]},
            {"name": "备用网关 B", "ip": "192.168.1.2", "status": "Online", "children": []},
            {"name": "旧网关 C", "ip": "192.168.1.3", "status": "Offline", "children": [
                {"name": "烟雾报警器", "ip": "192.168.1.201", "status": "Offline"},
            ]},
        ]

        for d in devices:
            item = QTreeWidgetItem(self.tree)
            # 存储数据到自定义角色
            item.setData(0, ROLE_DEVICE_NAME, d["name"])
            item.setData(0, ROLE_DEVICE_IP, d["ip"])
            item.setData(0, ROLE_DEVICE_STATUS, d["status"])
            item.setData(0, ROLE_IS_GATEWAY, True)
            
            for c in d["children"]:
                child = QTreeWidgetItem(item)
                child.setData(0, ROLE_DEVICE_NAME, c["name"])
                child.setData(0, ROLE_DEVICE_IP, c["ip"])
                child.setData(0, ROLE_DEVICE_STATUS, c["status"])
                child.setData(0, ROLE_IS_GATEWAY, False)

        self.tree.expandAll()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AdvancedRenderDemo()
    window.show()
    sys.exit(app.exec())
