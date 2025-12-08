from enum import Enum


class RegisterType(Enum):
    COIL = (0,)
    DISCRETE_INPUT = (1,)
    HOLDING_REGISTER = (2,)
    INPUT_REGISTER = (3,)


class Endianness(Enum):
    BIG = "big"
    LITTLE = "little"


class DataType(Enum):
    """
    数据类型枚举
    描述数据类型和寄存器数量的对应关系
    一个寄存器占用2个字节
    """

    BOOL = 1
    INT16 = 1
    UINT16 = 1
    INT32 = 2
    UINT32 = 2
    INT64 = 4
    UINT64 = 4
    FLOAT32 = 2
    FLOAT64 = 4
    
class ValueGenerateType(Enum):
    RANDOM = "random"
    ASSIGN = "assign"
