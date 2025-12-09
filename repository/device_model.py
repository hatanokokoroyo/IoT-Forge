from sqlalchemy import Column, Integer, String, Text, Enum as SAEnum
from repository.base import Base, DeviceType


class DeviceModel(Base):
    __tablename__ = "device_models"

    # 自增id
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 设备模型名称
    name = Column(String(100), nullable=False)
    # 设备模型类型
    type = Column(SAEnum(DeviceType), nullable=False, default=DeviceType.GATEWAY)
    # 设备模型属性，JSON格式字符串
    properties = Column(Text, nullable=True)

    def __repr__(self):
        return f"<DeviceModel(id={self.id}, name={self.name}, type={self.type})>"


# 查询所有设备模型数据
def get_all_device_models(session) -> list[DeviceModel]:
    return session.query(DeviceModel).all()


# 根据ID删除设备模型
def delete_device_model_by_id(session, model_id: int) -> None:
    model = session.query(DeviceModel).filter(DeviceModel.id == model_id).first()
    if model:
        session.delete(model)
        session.commit()
