import datetime
from sqlalchemy import create_engine
from sqlalchemy import Column, Date, Integer, String,DateTime,Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import contextlib

# 连接数据库
engine = create_engine('sqlite:///database.sqlite',echo=True)

# 基本类
Base = declarative_base()

# 表要继承基本类
class Use(Base):
    __tablename__ = 'use_info' # 表的名字

    # 定义各字段
    id = Column(Integer, autoincrement=True,primary_key=True)
    teacherName = Column(String,nullable=False) # 教师名字
    className = Column(String) # 班级名字
    projectName = Column(String)
    studentNumber = Column(Integer) # 计划学生数
    studentNum = Column(Integer) # 实际学生数
    userTime = Column(Date) # 使用日期
    classTime = Column(String) # 使用字符串记录第几课的次数，用、拼接
    createTime = Column(DateTime,default=datetime.datetime.now())
    status = Column(Text)

    def __str__(self):
        return self.id


@contextlib.contextmanager
def DBConnection():
    DBSession = sessionmaker(bind=engine)()
    yield DBSession
    DBSession.close()
    return

if __name__ == '__main__':
    # 创建表
    Base.metadata.create_all(engine)