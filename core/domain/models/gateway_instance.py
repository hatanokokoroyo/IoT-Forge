from core.domain.models.gateway_model import GateWayProtocolType, ServerConfig, HeartbeatConfig, \
    RegistrationPacketConfig


class GatewayInstance:
    def __init__(self, id_: int, protocol: 'GateWayProtocolType', server_config: 'ServerConfig',
                 heartbeat_config: 'HeartbeatConfig', registration_packet_config: 'RegistrationPacketConfig', sn: str,
                 secret: str):
        self.id_ = id_
        self.protocol = protocol
        self.server_config = server_config
        self.heartbeat_config = heartbeat_config
        self.registration_packet_config = registration_packet_config
        self.sn = sn
        self.secret = secret
