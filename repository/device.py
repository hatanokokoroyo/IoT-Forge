from sqlalchemy import Column, Integer, String, Text, Enum as SAEnum
import enum
from repository.base import Base, DeviceType


class Device(Base):
    __tablename__ = "devices"
    # 自增id
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 设备名称
    name = Column(String(100), nullable=False)
    # 设备类型
    type = Column(SAEnum(DeviceType), nullable=False, default=DeviceType.GATEWAY)
    # 父设备id, 网关设备的id
    parent_id = Column(Integer, nullable=True)
    # 设备属性json字符串
    properties = Column(Text, nullable=True)

    def __repr__(self):
        return f"<DeviceModel(id={self.id}, name={self.name}, type={self.type})>"


# 查询所有设备数据
def get_all_devices(session) -> list[Device]:
    return session.query(Device).all()


# 根据ID删除设备, 如果删除的是网关设备, 需要级联删除其下属从设备
def delete_device_by_id(session, device_id: int) -> None:
    device = session.query(Device).filter(Device.id == device_id).first()
    if device:
        if device.type == DeviceType.GATEWAY:
            # 级联删除从设备
            slaves = session.query(Device).filter(Device.parent_id == device_id).all()
            for slave in slaves:
                session.delete(slave)
        session.delete(device)
        session.commit()
