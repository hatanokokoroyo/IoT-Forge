# QTreeWidget + QStyledItemDelegate 教程

本教程旨在帮助你掌握如何使用 PySide6 的 `QTreeWidget` 和 `QStyledItemDelegate` 来创建高性能、自定义的设备列表。

## 教程文件说明

请按照以下顺序阅读和运行代码：

1.  **`1_basic_structure.py` (基础结构)**
    *   **目标**: 学习如何创建一个基本的 `QTreeWidget` 并填充层级数据（网关和子设备）。
    *   **核心**: `QTreeWidget`, `QTreeWidgetItem`。

2.  **`2_simple_delegate.py` (简单的 Delegate)**
    *   **目标**: 初步了解 `QStyledItemDelegate`，学习如何接管绘制过程。
    *   **核心**: `paint()` 方法, `QPainter`, `option.rect`。
    *   **效果**: 自定义背景色和简单的文本绘制。

3.  **`3_advanced_rendering.py` (复杂内容绘制)**
    *   **目标**: 绘制一个完整的“设备卡片”，包含图标、粗体名称、IP地址、状态指示灯等。
    *   **核心**: `drawText`, `drawEllipse`, `QFont`, 自定义数据角色 (`Qt.UserRole`)。
    *   **效果**: 看起来像一个专业的设备列表。

4.  **`4_interaction.py` (交互处理)**
    *   **目标**: 在 Delegate 中处理鼠标点击事件（例如点击列表项中的“查看”按钮）。
    *   **核心**: `editorEvent()`, `QEvent`, 坐标判断。
    *   **效果**: 点击列表项内部的特定区域触发特定动作。

## 如何运行

确保你已经安装了 PySide6：
```bash
pip install PySide6
```

然后在终端中运行对应的 Python 文件：
```bash
python 1_basic_structure.py
python 2_simple_delegate.py
# ... 以此类推
```
