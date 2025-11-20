from PySide6.QtGui import Qt
from PySide6.QtWidgets import (QHBoxLayout, QVBoxLayout, QLabel, QTreeView, QTableView,
                               QHeaderView,
                               QComboBox,
                               QPushButton,
                               QLineEdit
                               )


class DeviceLayout(QHBoxLayout):
    def __init__(self):
        super().__init__()

        self.addLayout(DeviceModelLayout())
        self.addLayout(DeviceListLayout())


class DeviceModelLayout(QVBoxLayout):
    def __init__(self):
        super().__init__()

        model_label = QLabel("设备模型列表")
        self.addWidget(model_label)

        model_tree_view = QTreeView()
        model_tree_view.setFixedWidth(250)
        self.addWidget(model_tree_view)


class DeviceListLayout(QVBoxLayout):
    def __init__(self):
        super().__init__()

        self.list_label = QLabel("设备列表")
        self.addWidget(self.list_label)

        # 搜索栏
        self.search_layout = QHBoxLayout()
        self.addLayout(self.search_layout)

        # 下拉框 设备分组
        self.device_group_combo_box = QComboBox()
        self.device_group_combo_box.addItem("设备分组")
        self.device_group_combo_box.setFixedWidth(100)
        self.search_layout.addWidget(self.device_group_combo_box)
        # 设备状态选择框
        self.device_status_combo_box = QComboBox()
        self.device_status_combo_box.addItem("设备状态")
        self.device_status_combo_box.setFixedWidth(100)
        self.search_layout.addWidget(self.device_status_combo_box)
        # 设备名称输入框
        self.device_name_input = QLineEdit("输入设备名称搜索")
        self.device_name_input.setFixedWidth(200)
        self.bind_device_name_input_method()

        self.search_layout.addWidget(self.device_name_input)
        # 添加一个弹性空间
        self.search_layout.addStretch()
        # 搜索按钮
        self.search_button = QPushButton("搜索")
        self.search_button.setFixedWidth(80)
        self.search_layout.addWidget(self.search_button)

        # 命令栏
        self.command_layout = QHBoxLayout()
        self.addLayout(self.command_layout)
        # 批量启动; 批量停止; 批量删除按钮
        self.start_button = QPushButton("批量启动")
        self.start_button.setFixedWidth(100)
        self.command_layout.addWidget(self.start_button)
        self.stop_button = QPushButton("批量停止")
        self.stop_button.setFixedWidth(100)
        self.command_layout.addWidget(self.stop_button)
        self.delete_button = QPushButton("批量删除")
        self.delete_button.setFixedWidth(100)
        self.command_layout.addWidget(self.delete_button)
        self.command_layout.addStretch()

        device_table_view = QTableView()
        self.addWidget(device_table_view)

    def bind_device_name_input_method(self):
        # 当用户点击输入框时，清空默认文本
        def clear_text():
            if self.device_name_input.text() == "输入设备名称搜索":
                self.device_name_input.clear()

        def reset_text():
            if self.device_name_input.text() == "":
                self.device_name_input.setText("输入设备名称搜索")

        self.device_name_input.mousePressEvent = lambda event: clear_text()
        self.device_name_input.focusOutEvent = lambda event: reset_text()
