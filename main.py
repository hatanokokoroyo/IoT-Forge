from sqlalchemy import create_engine
from repository.base import Base
import repository.device_model
import repository.device
import gui.main_window
from sqlalchemy.orm import sessionmaker


def main():
    db_init()

    app = gui.main_window.QApplication([])
    app.setStyleSheet(read_qss_file())
    window = gui.main_window.MainWindow()
    window.show()
    app.exec()


def db_init():
    # echo=True 可以看到生成的 SQL 语句，方便调试
    engine = create_engine("sqlite:///iot-forge.db", echo=False)
    # 这行代码会扫描所有继承自 Base 的类，并创建不存在的表
    Base.metadata.create_all(engine)


def read_qss_file() -> str:
    """读取 QSS 样式文件内容"""
    try:
        with open("./gui/style.qss", "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Error reading QSS file: {e}")
        return ""


if __name__ == "__main__":
    main()
