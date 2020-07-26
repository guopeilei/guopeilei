from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String

Base = declarative_base()


class TerminateInfo(Base):
    __tablename__ = "TERMINAL_INFO"

    TERMINAL_ID = Column(String(50), primary_key=True)
    AGENT_PORT = Column(String(5))
    TERMINAL_ADDRESS = Column(String(50))
    TERMINAL_DEPLOY = Column(String(10))
    TERMINAL_ENCODING = Column(String(10))
    TERMINAL_MAC = Column(String(30))
    TERMINAL_PORT = Column(String(5))
    TERMINAL_STATUS = Column(String(30))
    TERMINAL_SYSTEM = Column(String(20))
    TERMINAL_TEMPLATE = Column(String(50))
    USE_VERSIONNO = Column(String(10))
    VERSION_PORT = Column(String(5))
    AGENT_VER = Column(String(30))
    ISSUED_STATUS = Column(String(20))
