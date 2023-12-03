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
           position: str, limit: int = 30, page: int = 1):    
  user = get_user(token)
  org = get_org(user)
  cols = ['id', 'first_name', 'last_name', 'organization'] + org['columns'] + ['status']
  status = [] if status_str == '' else status_str.split(',')

  return search_employee(
    cols=cols,
    params={
      'organization': org['name'],
      'status': status,
      'location': location,
      'company': company,
      'department': department,
      'position': position,
    },
    limit=limit,
    page=page
  )

def search_employee(cols: list[str],
                    params: dict,
                    limit: int = 30,
                    page: int = 1):

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

  if 'location' in params and params['location'] is not None:
    query = query.filter(Employee.location == params['location'])

  if 'company' in params and params['company'] is not None:
    query = query.filter(Employee.company == params['company'])

  if 'department' in params and params['department'] is not None:
    query = query.filter(Employee.department == params['department'])

  if 'position' in params and params['position'] is not None:
    query = query.filter(Employee.position == params['position'])

  results = query.limit(limit).all()
  return list(map(lambda result: dict(zip(cols, result)), results))