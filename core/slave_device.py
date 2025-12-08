from enums import RegisterType, DataType, ValueGenerateType
from typing import Dict, Tuple, List


class Property:
    def __init__(self, property_json):
        self.property_name: str = property_json["property_name"]
        self.type: RegisterType = RegisterType(property_json["register_type"])
        self.address: int = property_json["register_address"]
        self.data_type: DataType = DataType(property_json["data_type"])
        self.data_generate_type: ValueGenerateType = ValueGenerateType(
            property_json["value_generate_type"]
        )
        self.data_assign = property_json.get("value_assign", None)
        # TODO 增加校验
        self.data_random_range = property_json.get("value_random_range", None)
        self.endianess = property_json.get("endianness", "big")
        self.desc = property_json.get("desc", "")


class SlaveDevice:
    def __init__(self, config_json):
        self.property_list: list = self.construct_property_list(config_json)
        register_dict, random_register_address_dict = self.construct_register_dict()
        # 寄存器字典, 用于存储寄存器的值
        # RegisterType -> List, 每种寄存器类型对应一个列表, 列表长度根据属性中寄存器的最大地址和数据类型计算得到
        self.register_dict = register_dict
        # 随机数寄存器字典, (RegisterType, address) -> Property, 随机属性对应寄存器的地址->属性对象的映射, 用于在寄存器读取后刷新属性对应寄存器的值
        #
        self.random_register_address_dict = random_register_address_dict

    def construct_property_list(self, config_json) -> list:
        property_list = []
        for property_json in config_json:
            property_obj = Property(property_json)
            property_list.append(property_obj)
        return property_list

    def construct_register_dict(
        self,
    ) -> Tuple[Dict[RegisterType, List], Dict[Tuple[RegisterType, int], Property]]:
        register_dict = {
            RegisterType.COIL: [],
            RegisterType.DISCRETE_INPUT: [],
            RegisterType.HOLDING_REGISTER: [],
            RegisterType.INPUT_REGISTER: [],
        }
        random_register_address_dict: Dict[Tuple[RegisterType, int], Property] = {}
        return register_dict, random_register_address_dict
