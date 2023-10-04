from db.base_class import Base
from sqlalchemy import Column, String


class Example(Base):
    __tablename__ = "examples"

    uuid = Column(String(36), nullable=False, primary_key=True)
    text = Column(String(100), nullable=False, index=True)
