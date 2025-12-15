from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QMessageBox
from repository.device_model import DeviceModel
from repository.base import get_session


class AddGateWayModelWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Gateway Model")
        self.layout = QVBoxLayout()

        self.name_label = QLabel("网关模型名称:")
        self.name_input = QLineEdit()
        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.name_input)

        self.protocol_type_label = QLabel("协议类型:")
        self.protocol_type_input = QComboBox()
        self.protocol_type_input.addItems(["Modbus RTU"])
        self.layout.addWidget(self.protocol_type_label)
        self.layout.addWidget(self.protocol_type_input)

        self.add_button = QPushButton("添加")
        self.add_button.clicked.connect(self.add_model)
        self.layout.addWidget(self.add_button)

        self.setLayout(self.layout)

    def add_model(self):
        model_name = self.name_input.text()
        protocol_type = self.protocol_type_input.currentText()
        if model_name:
            QMessageBox.information(self, "Success", f"网关模型 '{model_name}'添加成功, 协议类型: {protocol_type}")
            self.name_input.clear()
        else:
            QMessageBox.warning(self, "Input Error", "请输入模型名称.")

        new_device_model = DeviceModel(
            name=model_name,
            type="GATEWAY",
            properties=f'{{"protocol_type": "{protocol_type}"}}',
        )
        # 保存
        session = get_session()
        session.add(new_device_model)
        session.commit()
