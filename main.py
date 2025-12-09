from sqlalchemy import create_engine
from repository.base import Base
import repository.device_model
import repository.device
import gui.main_window
from sqlalchemy.orm import sessionmaker


def main():
    db_init()

    app = gui.main_window.QApplication([])
    window = gui.main_window.MainWindow()
    window.show()
    app.exec()


def db_init():
    # echo=True 可以看到生成的 SQL 语句，方便调试
    engine = create_engine("sqlite:///iot-forge.db", echo=True)
    session = sessionmaker(bind=engine)

    # 这行代码会扫描所有继承自 Base 的类，并创建不存在的表
    Base.metadata.create_all(engine)
    print("Database initialized and tables checked/created.")


if __name__ == "__main__":
    main()
