from typing import Union
from pydantic import BaseModel, field_serializer

STATUS_TO_TEXT = {
  '1': 'active',
  '2': 'not_started',
  '3': 'terminated'
}

class Employee(BaseModel):
  id: int
  first_name: str
  last_name: str
  contact_info: Union[str, None] = None
  organization: Union[str, None] = None
  company: Union[str, None] = None
  department: Union[str, None] = None
  position: Union[str, None] = None
  location: Union[str, None] = None
  status: Union[str, None] = None

  @field_serializer('status')
  def serialize_status(self, status: str, _info):
    return STATUS_TO_TEXT[status]
