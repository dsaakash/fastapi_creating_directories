from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class Department(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

class Directory(Base):
    __tablename__ = "directories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    department_id = Column(Integer, ForeignKey("departments.id"))
    department = relationship("Department")

class Subdirectory(Base):
    __tablename__ = "subdirectories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    directory_id = Column(Integer, ForeignKey("directories.id"))
    directory = relationship("Directory")
