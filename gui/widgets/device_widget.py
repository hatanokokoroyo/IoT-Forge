from PySide6.QtGui import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QVBoxLayout,
    QTreeWidget,
    QHeaderView,
    QComboBox,
    QPushButton,
    QLineEdit,
    QTreeWidgetItem,
)

from gui.widgets.add_model import AddGateWayModelWidget
from repository.device_model import DeviceModel


class DeviceLayout(QHBoxLayout):
    def __init__(self):
        super().__init__()

        self.device_model_layout = DeviceModelLayout()
        self.addLayout(self.device_model_layout)

        self.device_layout = DeviceListLayout()
        self.addLayout(self.device_layout)

    def update_data(self, devices, models):
        """统一更新数据入口"""
        self.device_layout.update_devices(devices)
        self.device_model_layout.update_models(models)


class DeviceModelLayout(QVBoxLayout):
    def __init__(self):
        super().__init__()

        # 设备模型列表
        self.model_tree_view = QTreeWidget()
        self.addWidget(self.model_tree_view)
        self.model_tree_view.setContentsMargins(0, 0, 0, 0)

        self.model_tree_view.setFixedWidth(250)
        # 设置表头 "模型列表", ""
        self.model_tree_view.setHeaderHidden(False)
        self.model_tree_view.setHeaderLabels(["模型列表", "操作"])
        # 第一列长度180, 第二列弹性
        self.model_tree_view.setColumnWidth(0, 180)
        self.model_tree_view.setColumnWidth(1, 40)

        # 固定添加两行: 网关模型, 从设备模型; 每行添加一个新增按钮
        self.gateway_item = QTreeWidgetItem(["网关模型"])
        self.model_tree_view.addTopLevelItem(self.gateway_item)
        self.add_gateway_model_button = QPushButton("新增")
        self.model_tree_view.setItemWidget(self.gateway_item, 1, self.add_gateway_model_button)

        # 当点击新增按钮时, 弹出添加网关模型窗口
        self.add_gateway_model_dialog = AddGateWayModelWidget()
        self.add_gateway_model_button.clicked.connect(self.add_gateway_model_dialog.show)

        self.slave_item = QTreeWidgetItem(["从设备模型"])
        self.model_tree_view.addTopLevelItem(self.slave_item)
        self.add_slave_model_button = QPushButton("新增")
        self.model_tree_view.setItemWidget(self.slave_item, 1, self.add_slave_model_button)
        # 默认展开所有
        self.model_tree_view.expandAll()

    def update_models(self, models: list[DeviceModel]):
        """刷新模型列表"""
        self.gateway_item.takeChildren()
        self.slave_item.takeChildren()
        for model in models:
            item = QTreeWidgetItem([model.name])
            item.setData(0, Qt.UserRole, model.id)
            if model.type.name == "GATEWAY":
                self.gateway_item.addChild(item)
            else:
                self.slave_item.addChild(item)


class DeviceListLayout(QVBoxLayout):
    def __init__(self):
        super().__init__()

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

        self.device_tree_widget = DeviceTreeWidget()
        self.addWidget(self.device_tree_widget)

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

    def update_devices(self, devices):
        """刷新设备列表"""
        self.device_tree_widget.update_data(devices)


class DeviceTreeWidget(QTreeWidget):
    def __init__(self):
        super().__init__()
        self.setHeaderHidden(False)
        self.header().setSectionResizeMode(QHeaderView.Stretch)
        self.setHeaderLabels(["设备名称", "类型", "ID"])

    def update_data(self, devices):
        """渲染设备树"""
        self.clear()
        for device in devices:
            # 这里简单展示，实际可能需要根据 device.type 转换枚举显示
            item = QTreeWidgetItem([device.name, str(device.type), str(device.id)])
            item.setData(0, Qt.UserRole, device.id)
            self.addTopLevelItem(item)
