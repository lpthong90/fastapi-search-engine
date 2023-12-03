import random

try:
  from .models import Employee
except:
  from models import Employee


def generate_hex(n):
  return hex(int(random.random() * (2**(n*4) - 1)))[2:]

def generate_employee(params: dict = {}):
  first_name = params.get('first_name') or f"first_name-{generate_hex(5)}"
  last_name = params.get('last_name') or f"last_name-{generate_hex(5)}"
  contact_info = params.get('contact_info') or f"contact_info-{generate_hex(5)}"
  organization = params.get('organization') or f"org-{random.choice(['a', 'b', 'c'])}"
  department = params.get('department') or f"department-{generate_hex(1)}"
  company = params.get('company') or f"company-{generate_hex(5)}"
  position = params.get('position') or f"position-{generate_hex(2)}"
  location = params.get('location') or f"location-{generate_hex(2)}"
  status = params.get('status') or random.choice(['1', '2', '3'])
  return Employee(
    first_name=first_name,
    last_name=last_name,
    contact_info=contact_info,
    organization=organization,
    company=company,
    department=department,
    position=position,
    location=location,
    status=status
  )
