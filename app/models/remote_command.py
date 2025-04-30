from sqlalchemy import Column, Integer, String, DateTime
from app.core.database import Base

class RemoteCommand(Base):
    __tablename__ = "remote_commands"

    id = Column(Integer, primary_key=True, index=True)
    kiosk_id = Column(String(50), index=True)
    command = Column(String(255))
    status = Column(String(20), default="pending")
    received_at = Column(String, nullable=True)
