from sqlalchemy import Column, Integer, String, Boolean
from database import Base


class Doctor(Base):

    __tablename__ = "doctors"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(String(100), nullable=False)

    specialization = Column(String(100))

    experience = Column(Integer)

    available = Column(Boolean, default=True)