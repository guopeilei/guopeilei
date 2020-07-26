from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,String


Base=declarative_base()

class ServiceReg(Base):
    __tablename__ = "SERVICE_INFO"

    SERVICE_ID=Column(String(15), primary_key=True)
    ADAPTERFLOW_ID=Column(String(100))
    ISGNS=Column(String(255))
    LAST_TIME=Column(String(20))
    PACKAGE_TYPE=Column(String(10))
    PROTOCOL_ID_IN=Column(String(50))
    PROTOCOL_ID_OUT=Column(String(50))
    SERVICE_CLASS=Column(String(128))
    SERVICE_DESC=Column(String(256))
    SERVICE_REGURL=Column(String(50))
    SERVICE_SYSTEM=Column(String(20))
    STATUS=Column(String(15))
    VERSION_NO=Column(String(10))
    ISOPENIPS = Column(String(10))
    IPS=Column(String(300))
    SERVICE_INFO=Column(String(300))