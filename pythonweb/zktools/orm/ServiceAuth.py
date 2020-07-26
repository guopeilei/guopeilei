from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String


Base=declarative_base()

class ServiceAuth(Base):
    __tablename__="SERVICE_AUTH"

    ID=Column(String(32), primary_key=True)
    CHANNEL_SYSTEM=Column(String(20))
    LAST_TIME=Column(String(20))
    PACKAGE_TYPE=Column(String(10))
    SERVICE_CODE=Column(String(15))
    SERVICE_SYSTEM=Column(String(20))
    STATUS=Column(String(10))
    TRANS_ID=Column(String(10))
    VERSION_NO=Column(String(10))





