from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,String


Base = declarative_base()

class ServiceConfig(Base):
    __tablename__ = "CP_CONFIG"

    ID=Column(String(32),primary_key=True)
    FILE_NAME = Column(String(128))
    FILE_PATH = Column(String(256))
    FILE_PATH2 = Column(String(256))
    LASTVERS = Column(String(10))
    MODEL = Column(String(20))
    OPT_DATE = Column(String(20))
    OPT_USER = Column(String(20))
    REMARK = Column(String(256))
    SERVICE_ID = Column(String(15))
    STATUS = Column(String(1))
    SYSTEM_ID = Column(String(20))
    TRANSID = Column(String(10))
    TYPE = Column(String(10))
    ON_VERSION_NO = Column(String(10))


