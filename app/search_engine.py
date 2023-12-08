from sqlalchemy import or_

try:
  from .database import SessionLocal
  from .models import Employee, EmployeeStatus
  from .cache import timed_lru_cache
  from .users import get_user
  from .orgs import get_org
except:
  from database import SessionLocal
  from models import Employee, EmployeeStatus
  from cache import timed_lru_cache
  from users import get_user
  from orgs import get_org

@timed_lru_cache(5)
def search(token: str, status_str: str, location: str, company: str, department: str,
           position: str, limit: int = 10, last_seen_id: int | None = None):    
  user = get_user(token)
  org = get_org(user)
  cols = ['id', 'first_name', 'last_name', 'organization'] + org['columns'] + ['status']
  status = [] if status_str == '' else status_str.split(',')

  employees = search_employee(
    cols=cols,
    params={
      'organization': org['name'],
      'status': status,
      'location': location,
      'company': company,
      'department': department,
      'position': position,
    },
    limit=limit + 2,
    last_seen_id=last_seen_id
  )

  has_previous_page = False
  has_next_page = False
  if len(employees) == 0:
    return {
      'limit': limit,
      'has_next_page': has_next_page,
      'has_previous_page': has_previous_page,
      'employees': employees
    }

  if last_seen_id is not None and employees[0]['id'] == last_seen_id:
    has_previous_page = True
    employees.pop(0)
  
  if len(employees) > limit:
    has_next_page = True
    employees = employees[:limit]
  
  return {
    'limit': limit,
    'has_next_page': has_next_page,
    'has_previous_page': has_previous_page,
    'employees': employees
  }

def search_employee(cols: list[str],
                    params: dict,
                    limit: int = 30,
                    last_seen_id: int | None = None):

  session = SessionLocal()
  columns = list(map(lambda col: getattr(Employee, col), cols))
  query = session.query(*columns)

  if 'organization' in params and params['organization'] is not None:
    query = query.filter(Employee.organization == params['organization'])
  else:
    return []

  if 'status' in params and params['status'] is not None:
    if params['status'].__class__ is list and len(params['status']) > 0:
      status_conds = []
      for status in params['status']:
        if status.upper() in EmployeeStatus.__members__:
          status_conds.append(Employee.status == str(EmployeeStatus[status.upper()].value))
      query = query.filter(or_(*status_conds))

  for col in ['location', 'company', 'department', 'position']:
    if col in params and params[col] is not None:
      query = query.filter(getattr(Employee, col) == params[col])

  if last_seen_id is not None:
    query = query.filter(Employee.id <= last_seen_id)

  query = query.order_by(Employee.id.desc())
  results = query.limit(limit).all()
  return list(map(lambda result: dict(zip(cols, result)), results))