import sys
from PySide6.QtWidgets import (QApplication, QTreeWidget, QTreeWidgetItem, 
                               QVBoxLayout, QWidget, QMainWindow, QStyledItemDelegate, QStyle, QMessageBox)
from PySide6.QtCore import Qt, QRect, QSize, QEvent, QPoint
from PySide6.QtGui import QPainter, QColor, QPen, QFont, QBrush, QMouseEvent

ROLE_DEVICE_NAME = Qt.UserRole + 1
ROLE_DEVICE_IP = Qt.UserRole + 2
ROLE_DEVICE_STATUS = Qt.UserRole + 3

class InteractiveDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 用于记录鼠标按下的位置，判断点击
        self._pressed_point = None

    def sizeHint(self, option, index):
        return QSize(option.rect.width(), 60)

    def paint(self, painter: QPainter, option, index):
        painter.save()
        
        name = index.data(ROLE_DEVICE_NAME)
        status = index.data(ROLE_DEVICE_STATUS)
        rect = option.rect

        # 背景
        if option.state & QStyle.State_Selected:
            painter.fillRect(rect, QColor("#e6f7ff"))
        else:
            painter.fillRect(rect, QColor("#ffffff"))

        # 文本
        painter.setPen(Qt.black)
        painter.drawText(rect.adjusted(60, 0, 0, 0), Qt.AlignVCenter | Qt.AlignLeft, name)

        # --- 绘制按钮 ---
        # 我们在右侧画一个 "操作" 按钮
        # 按钮区域
        btn_rect = self.get_button_rect(rect)
        
        # 简单的按钮样式
        btn_color = QColor("#2196F3")
        # 如果鼠标在按钮上按下 (这里简化处理，只画静态)
        
        painter.setBrush(QBrush(btn_color))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(btn_rect, 4, 4)
        
        painter.setPen(Qt.white)
        painter.drawText(btn_rect, Qt.AlignCenter, "查看")

        painter.restore()

    def get_button_rect(self, item_rect):
        """计算按钮在 Item 中的位置"""
        btn_width = 60
        btn_height = 30
        x = item_rect.right() - btn_width - 10
        y = item_rect.top() + (item_rect.height() - btn_height) / 2
        return QRect(x, y, btn_width, btn_height)

    def editorEvent(self, event, model, option, index):
        """
        处理交互事件 (鼠标点击等)
        """
        if event.type() == QEvent.MouseButtonPress:
            # 记录按下位置
            self._pressed_point = event.pos()
            return True # 消耗事件
            
        elif event.type() == QEvent.MouseButtonRelease:
            if self._pressed_point:
                # 检查释放位置是否在按钮内
                btn_rect = self.get_button_rect(option.rect)
                if btn_rect.contains(event.pos()) and btn_rect.contains(self._pressed_point):
                    # 触发点击逻辑
                    device_name = index.data(ROLE_DEVICE_NAME)
                    print(f"点击了设备: {device_name} 的查看按钮")
                    
                    # 也可以发送自定义信号，或者调用外部回调
                    # 这里简单弹窗演示 (注意：在 paint/event 中弹窗会阻塞，实际项目建议用信号)
                    # 为了演示方便，我们直接打印，并在主窗口里看效果
                    
                    # 更好的方式：通过 model 或者 tree 获取主窗口处理
                    # 这里我们发送一个自定义事件或者直接调用 tree 的方法(如果耦合允许)
                    # 最标准做法：emit signal (Delegate 需要定义信号)
                    
                    # 这里为了演示简单，我们直接修改数据状态来触发重绘，或者打印
                    pass
                
                self._pressed_point = None
                return True
                
        return super().editorEvent(event, model, option, index)

class InteractionDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("教程 4: 交互处理 (按钮点击)")
        self.resize(600, 400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.tree = QTreeWidget()
        self.tree.setColumnCount(1)
        self.tree.setHeaderLabels(["设备操作"])
        
        self.delegate = InteractiveDelegate()
        self.tree.setItemDelegate(self.delegate)

        layout.addWidget(self.tree)
        self.init_data()

    def init_data(self):
        for i in range(5):
            item = QTreeWidgetItem(self.tree)
            item.setData(0, ROLE_DEVICE_NAME, f"智能设备 {i+1}")
            item.setData(0, ROLE_DEVICE_STATUS, "Online")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InteractionDemo()
    window.show()
    sys.exit(app.exec())
