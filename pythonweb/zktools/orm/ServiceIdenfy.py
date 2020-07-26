from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,String


Base=declarative_base()

class ServiceIdenfyInvoke(Base):
    __tablename__ = "SERVICE_IDENTIFY_INVOKE"

    EID=Column(String(32),primary_key=True)
    IDENTIFY_STATE=Column(String(1))
    INVOKE_ID=Column(String(32))
    IDENTIFY_KEY=Column(String(50))
    OPT_DATE=Column(String(20))
    OPT_USER=Column(String(20))
    REMARK=Column(String(256))
    IDENTIFY_VALUE=Column(String(20))
    IDENTIFY_VERSION=Column(String(10))

class ServiceIdenfy(Base):
    __tablename__ = "SERVICE_IDENTIFY"

    INVOKE_ID=Column(String(32),primary_key=True)
    IDENTIFY_CHARACTER=Column(String(20))
    IDENTIFY_EXPRESSION=Column(String(256))
    IDENTIFY_MODEL=Column(String(10))
    OPT_DATE=Column(String(20))
    OPT_USER=Column(String(20))
    PROTOCOL_NAME=Column(String(50))
    REMARK=Column(String(256))
    IDENTIFY_STATE=Column(String(1))



