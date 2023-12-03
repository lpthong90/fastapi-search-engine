from sqlalchemy import Column, Integer, String
import enum

try:
  from .database import Base
except:
  from database import Base

EmployeeStatus = enum.Enum('EmployeeStatus', ['ACTIVE', 'NOT_STARTED', 'TERMINATED'])

class Employee(Base):
  __tablename__ = "employees"

  id = Column(Integer, primary_key=True, index=True)
  first_name = Column(String, nullable=False)
  last_name = Column(String, nullable=False)
  contact_info = Column(String, nullable=False)
  organization = Column(String, nullable=False)
  company = Column(String, nullable=False)
  department = Column(String, nullable=False)
  position = Column(String, nullable=False)
  location = Column(String, nullable=False)
  status = Column(String, nullable=False)
