import sys
from PySide6.QtWidgets import (QApplication, QTreeWidget, QTreeWidgetItem, 
                               QVBoxLayout, QWidget, QMainWindow, QStyledItemDelegate, QStyle)
from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QPainter, QColor, QPen

# --- 教程说明 ---
# QStyledItemDelegate 允许我们完全接管 Item 的绘制过程。
# 核心方法是 paint()。
# 在 paint() 中，我们可以使用 QPainter 在给定的矩形区域 (option.rect) 内绘制任何我们想要的内容。

class SimpleDelegate(QStyledItemDelegate):
    def paint(self, painter: QPainter, option, index):
        """
        painter: 用于绘制的画笔
        option: 包含了 Item 的状态信息（如 rect, state 等）
        index: 当前 Item 的索引，用于获取数据
        """
        # 1. 保存 painter 状态 (这是一个好习惯，防止污染后续绘制)
        painter.save()

        # 2. 获取绘制区域
        rect = option.rect

        # 3. 获取数据
        # index.data() 默认获取 Qt.DisplayRole 的数据 (即 setText 设置的文本)
        text = index.data(Qt.DisplayRole)

        # 4. 自定义绘制背景
        # 如果被选中
        if option.state & QStyle.State_Selected:
            painter.fillRect(rect, QColor("#e6f7ff")) # 浅蓝色背景
        else:
            painter.fillRect(rect, QColor("#ffffff")) # 白色背景

        # 5. 自定义绘制文本
        # 我们把文本画在矩形中间，稍微偏移一点
        pen = QPen(Qt.black)
        painter.setPen(pen)
        
        # 这里的 rect.adjusted(10, 0, 0, 0) 表示左边距 10 像素
        painter.drawText(rect.adjusted(10, 0, 0, 0), Qt.AlignVCenter | Qt.AlignLeft, f"[自定义] {text}")

        # 6. 绘制一条底部分割线
        painter.setPen(QPen(QColor("#eeeeee")))
        painter.drawLine(rect.bottomLeft(), rect.bottomRight())

        # 7. 恢复 painter 状态
        painter.restore()

class SimpleDelegateDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("教程 2: 简单的 Delegate 绘制")
        self.resize(600, 400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.tree = QTreeWidget()
        self.tree.setColumnCount(1)
        self.tree.setHeaderLabels(["设备列表"])
        
        # --- 关键点：设置 Delegate ---
        self.delegate = SimpleDelegate()
        self.tree.setItemDelegate(self.delegate)
        
        # 设置行高稍微大一点，方便看效果 (虽然Delegate可以控制高度，但TreeWidget默认行高较小)
        # 更好的方式是在 Delegate 中实现 sizeHint()，下个教程会讲
        self.tree.setStyleSheet("QTreeWidget::item { height: 40px; }") 

        layout.addWidget(self.tree)
        self.init_data()

    def init_data(self):
        # 简单添加几个节点
        for i in range(5):
            item = QTreeWidgetItem(self.tree)
            item.setText(0, f"测试设备 {i+1}")
            for j in range(2):
                child = QTreeWidgetItem(item)
                child.setText(0, f"子设备 {i+1}-{j+1}")
        self.tree.expandAll()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimpleDelegateDemo()
    window.show()
    sys.exit(app.exec())
