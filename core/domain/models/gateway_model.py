import enum


class GateWayModel:
    """
    网关设备模型
    网关设备模型包含以下属性:
    - 协议类型 (protocol): 网关设备使用的协议类型，类型为 GateWayProtocolType 枚举。
    - 目标服务器地址 (server_address): 目标服务器的 IP 地址或域名，类型为字符串 (str)。
    - 目标服务器端口 (server_port): 目标服务器的端口号，类型为整数 (int)。
    - 心跳配置 (heartbeat_config): 心跳配置，类型为 HeartbeatConfig 对象。
    - 注册包配置 (registration_packet_config): 注册包配置，类型为 RegistrationPacketConfig 对象。
    """

    def __init__(self, id_: int, protocol: 'GateWayProtocolType', server_config: 'ServerConfig',
                 heartbeat_config: 'HeartbeatConfig', registration_packet_config: 'RegistrationPacketConfig'):
        self.id_ = id_
        self.protocol = protocol
        self.server_config = server_config
        self.heartbeat_config = heartbeat_config
        self.registration_packet_config = registration_packet_config


class GateWayProtocolType(enum.Enum):
    MODBUS_RTU = "Modbus RTU"
    MODBUS_TCP = "Modbus TCP"
    MQTT = "MQTT"
    HTTP = "HTTP"


class ServerConfig:
    """
    服务器配置模型
    服务器配置模型包含以下属性:
    - 服务器地址 (address): 服务器的 IP 地址或域名，类型为字符串 (str)。
    - 服务器端口 (port): 服务器的端口号，类型为整数 (int)。
    """

    def __init__(self, address: str, port: int):
        self.address = address
        self.port = port


class HeartbeatConfig:
    """
    心跳配置模型
    心跳配置模型包含以下属性:
    - 是否开启 (enabled): 心跳功能是否开启，类型为布尔值 (bool)。
    - 心跳间隔时间 (interval_ms): 心跳发送的时间间隔，单位为毫秒，类型为整数 (int)。
    - 心跳内容 (content): 心跳发送的内容，类型为字符串 (str)。
    """

    def __init__(self, enabled: bool, interval_ms: int, content: str):
        self.enabled = enabled
        self.interval_ms = interval_ms
        self.content = content


class RegistrationPacketConfig:
    """
    注册包配置模型
    注册包配置模型包含以下属性:
    - 是否开启 (enabled): 注册包功能是否开启，类型为布尔值 (bool)。
    - 发送方式 (send_mode): 注册包的发送方式，类型为字符串 (str)，支持 "单次" 和 "周期" 两种方式。
    - 发送间隔 (interval_ms): 注册包发送的时间间隔，单位为毫秒，类型为整数 (int)。
    - 发送内容 (content): 注册包发送的内容，类型为字符串 (str)。
    """

    def __init__(self, enabled: bool, send_mode: 'RegistrationPacketSendMode', interval_ms: int, content: str):
        self.enabled = enabled
        self.send_mode = send_mode
        self.interval_ms = interval_ms
        self.content = content


# 注册包发送模式枚举类
class RegistrationPacketSendMode(enum.Enum):
    SINGLE = "单次"
    PERIODIC = "周期"
