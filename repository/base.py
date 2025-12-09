from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import enum

# 创建共享的基类，所有模型都必须继承它
Base = declarative_base()

engine = create_engine("sqlite:///iot-forge.db", echo=False)
session = sessionmaker(bind=engine)


def get_session():
    return session()


class DeviceType(enum.Enum):
    GATEWAY = 0
    SLAVE = 1
