from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,String


Base=declarative_base()

class ServiceDefine(Base):
    __tablename__ = "SERVICE_DEFINITION"

    ID = Column(String(32), primary_key=True)
    DATA_ROUTER = Column(String(100))
    FILE_NAME = Column(String(128))
    FILE_PATH = Column(String(256))
    ONLINEVERS = Column(String(10))
    OPT_DATE = Column(String(20))
    OPT_USER = Column(String(10))
    PACKAGE_TYPE = Column(String(10))
    REMARK = Column(String(256))
    SERVICE_ID = Column(String(15))
    SERVICE_NAME = Column(String(150))
    STATUS = Column(String(1))
    SYSTEM_ID = Column(String(20))
    TRANSID = Column(String(50))
    VERSION_NO = Column(String(10))