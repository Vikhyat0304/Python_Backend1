import uuid
from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from database import Base

class File(Base):
    __tablename__ = "files"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(String, nullable=False)
    status = Column(String, default="uploading")  # uploading, processing, ready, failed
    progress = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    content = Column(String)  # parsed JSON data stored as string
