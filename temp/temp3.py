import sys
import random
from PySide6.QtWidgets import (QApplication, QTreeWidget, QTreeWidgetItem, 
                               QStyledItemDelegate, QVBoxLayout, QWidget, QHeaderView)
from PySide6.QtCore import Qt, QRect, QSize, Signal, QEvent, QPoint
from PySide6.QtGui import QColor, QPainter, QMouseEvent

# --- 数据角色定义 ---
STATUS_ROLE = Qt.UserRole + 1 

class ButtonDelegate(QStyledItemDelegate):
    # 定义两个信号，当“假按钮”被点击时触发，把被点击的 Item 传出去
    btn_start_clicked = Signal(QTreeWidgetItem)
    btn_stop_clicked = Signal(QTreeWidgetItem)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.bar_width = 4
        self.padding = 5
        # 定义按钮的大小
        self.btn_size = QSize(50, 20)
        self.btn_spacing = 5

    def get_buttons_rect(self, option_rect):
        """
        辅助函数：计算“启动”和“停止”按钮的区域坐标。
        这样 paint 和 editorEvent 可以共用这套坐标逻辑，保证点击位置准确。
        """
        # 按钮靠最右侧显示
        # 停止按钮 (最右)
        x_stop = option_rect.right() - self.btn_size.width() - 5
        y = option_rect.y() + (option_rect.height() - self.btn_size.height()) / 2
        rect_stop = QRect(int(x_stop), int(y), self.btn_size.width(), self.btn_size.height())

        # 启动按钮 (在停止按钮左边)
        x_start = x_stop - self.btn_size.width() - self.btn_spacing
        rect_start = QRect(int(x_start), int(y), self.btn_size.width(), self.btn_size.height())

        return rect_start, rect_stop

    def paint(self, painter, option, index):
        painter.save()

        # --- 1. 绘制原有的红绿竖条 (同上一版) ---
        is_online = index.data(STATUS_ROLE)
        status_color = QColor("#2ecc71") if is_online else QColor("#e74c3c")
        
        bar_rect = QRect(
            option.rect.x(), 
            option.rect.y() + 1, 
            self.bar_width, 
            option.rect.height() - 2
        )
        painter.fillRect(bar_rect, status_color)

        # --- 2. 绘制“假”按钮 ---
        # 只有当鼠标悬停这行，或者选中这行时才显示按钮？
        # 为了演示清晰，我们这里一直显示，或者你可以根据 option.state & QStyle.State_MouseOver 判断
        
        rect_start, rect_stop = self.get_buttons_rect(option.rect)

        # 绘制“启动”按钮背景 (简易扁平风)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor("#3498db")) # 蓝色
        painter.drawRoundedRect(rect_start, 3, 3)

        # 绘制“停止”按钮背景
        painter.setBrush(QColor("#e67e22")) # 橙色
        painter.drawRoundedRect(rect_stop, 3, 3)

        # 绘制按钮文字
        painter.setPen(Qt.white)
        painter.drawText(rect_start, Qt.AlignCenter, "启动")
        painter.drawText(rect_stop, Qt.AlignCenter, "停止")

        # --- 3. 调整文字绘制区域 ---
        # 避免原有文字遮挡住刚才画的按钮，把文字区域的右边界收缩一下
        # 同时也避开左边的红绿条
        new_rect = QRect(option.rect)
        new_rect.setLeft(new_rect.left() + self.bar_width + self.padding)
        new_rect.setRight(rect_start.left() - 10) # 文字不要碰到按钮
        
        option.rect = new_rect # 修改 option 传入父类
        
        super().paint(painter, option, index)
        painter.restore()

    def editorEvent(self, event, model, option, index):
        """
        核心交互逻辑：拦截鼠标事件
        """
        # 我们只关心鼠标松开事件 (MouseRelease)，类似 Click
        if event.type() == QEvent.MouseButtonRelease:
            mouse_event = event # 类型转换
            click_pos = mouse_event.position().toPoint() # 获取点击坐标

            # 获取按钮区域
            rect_start, rect_stop = self.get_buttons_rect(option.rect)

            # 命中测试 (Hit Test)
            if rect_start.contains(click_pos):
                # 获取当前行对应的 Item 对象
                item = self.parent().itemFromIndex(index)
                self.btn_start_clicked.emit(item)
                return True # 事件已处理，不再向下传递
            
            elif rect_stop.contains(click_pos):
                item = self.parent().itemFromIndex(index)
                self.btn_stop_clicked.emit(item)
                return True

        return super().editorEvent(event, model, option, index)

class DeviceTreeWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 高性能交互 Demo")
        self.resize(600, 600)
        layout = QVBoxLayout(self)

        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["设备列表"])
        self.tree.setUniformRowHeights(True) # 保持高性能
        
        # 实例化代理并设置
        self.delegate = ButtonDelegate(self.tree)
        self.tree.setItemDelegate(self.delegate)
        
        # --- 连接代理的信号 ---
        self.delegate.btn_start_clicked.connect(self.on_start_device)
        self.delegate.btn_stop_clicked.connect(self.on_stop_device)

        layout.addWidget(self.tree)
        self.load_data()

    def load_data(self):
        items = []
        for i in range(20): # 模拟数据
            gateway = QTreeWidgetItem([f"网关 Gateway_{i}"])
            gateway.setData(0, STATUS_ROLE, True)
            
            for j in range(10):
                child = QTreeWidgetItem([f"传感器 Sensor_{i}_{j}"])
                # 随机初始状态
                is_on = random.choice([True, False])
                child.setData(0, STATUS_ROLE, is_on)
                gateway.addChild(child)
            items.append(gateway)
        self.tree.addTopLevelItems(items)
        self.tree.expandAll()

    # --- 槽函数：处理业务逻辑 ---
    def on_start_device(self, item):
        name = item.text(0)
        print(f"指令：启动设备 -> {name}")
        # 修改数据状态
        item.setData(0, STATUS_ROLE, True)
        # 强制刷新该行显示 (否则颜色可能不会立即变)
        # 这里的 update 范围可以精确到 index，提高效率
        # 但为了简单，Qt 数据变动通常会自动触发重绘，如果没有触发，可以手动调用
        # item.treeWidget().viewport().update()

    def on_stop_device(self, item):
        name = item.text(0)
        print(f"指令：停止设备 -> {name}")
        item.setData(0, STATUS_ROLE, False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # 稍微调一点样式
    app.setStyleSheet("QTreeWidget { font-size: 14px; } QTreeWidget::item { height: 40px; }")
    win = DeviceTreeWidget()
    win.show()
    sys.exit(app.exec())