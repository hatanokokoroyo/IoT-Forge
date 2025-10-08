import enum


class Sensor:
    """
    传感器模型
    传感器模型包含以下属性:
    - 从站ID (slave_id): 传感器的从站ID，类型为整数 (int)。
    - 寄存器列表 (registers): 传感器的寄存器列表，类型为 Register 对象的列表 (list[Register])。
    """

    def __init__(self, slave_id: int, registers: list['Register']):
        self.slave_id = slave_id
        self.registers = registers


class Register:
    """
    寄存器模型
    寄存器模型包含以下属性:
    - 地址 (address): 寄存器的地址，类型为整数 (int)。
    - 数据类型 (data_type): 寄存器的数据类型，使用枚举 (DataType) 表示，支持整数 (int)、浮点数 (float)、字符串 (string) 和布尔值 (bool)。
    - 长度 (length): 寄存器的数据长度，类型为整数 (int)。
    - 读写权限 (read_write): 寄存器的读写权限，使用字符串表示，支持 "只读" 和 "读写" 两种权限。
    - 单位 (unit): 寄存器数据的单位，类型为字符串 (str)。
    - 描述 (description): 寄存器的描述信息，类型为字符串 (str)。
    """

    def __init__(self, address: int, data_type: 'RegisterDataType', length: int, read_write: str, unit: str,
                 description: str):
        self.address = address
        self.data_type = data_type
        self.length = length
        self.read_write = read_write
        self.unit = unit
        self.description = description


class RegisterDataType(enum.Enum):
    INT = "int"
    FLOAT = "float"
    STRING = "string"
    BOOL = "bool"
