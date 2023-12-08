from fastapi.testclient import TestClient
import sqlalchemy
import time

try:
  from .main import app
  from .rate_limiter import REQUEST_RATE_LIMIT_COUNT, REQUEST_RATE_LIMIT_WINDOW_SECONDS
  from .database import SessionLocal
  from .data_generator import generate_employee
  from .models import EmployeeStatus
  from .cache import reset_cache
  from .orgs import USER_ID_TO_ORGS
except:
  from main import app
  from rate_limiter import REQUEST_RATE_LIMIT_COUNT, REQUEST_RATE_LIMIT_WINDOW_SECONDS
  from database import SessionLocal
  from data_generator import generate_employee
  from models import EmployeeStatus
  from cache import reset_cache
  from orgs import USER_ID_TO_ORGS

def truncate_tables():
  session = SessionLocal()
  session.execute(sqlalchemy.text('delete table employees;'))
  session.commit()
  session.close()

def insert_employees():
  session = SessionLocal()
  objects = [
      generate_employee({'organization': 'org-a', 'status': EmployeeStatus.ACTIVE.value, 'department': 'dep-1', 'company': 'com-2', 'position': 'pos-3', 'location': 'loc-4'}),
      generate_employee({'organization': 'org-a', 'status': EmployeeStatus.ACTIVE.value, 'company': 'com-2', 'location': 'loc-4'}),
      generate_employee({'organization': 'org-a', 'status': EmployeeStatus.ACTIVE.value, 'position': 'pos-3'}),
      generate_employee({'organization': 'org-a', 'status': EmployeeStatus.NOT_STARTED.value, 'company': 'com-2', 'location': 'loc-4'}),
      generate_employee({'organization': 'org-a', 'status': EmployeeStatus.NOT_STARTED.value, 'position': 'pos-3', 'location': 'loc-4'}),
      generate_employee({'organization': 'org-a', 'status': EmployeeStatus.TERMINATED.value, 'company': 'com-2', 'position': 'pos-3'}),

      generate_employee({'organization': 'org-b', 'status': EmployeeStatus.ACTIVE.value, 'department': 'dep-1'}),
      generate_employee({'organization': 'org-b', 'status': EmployeeStatus.ACTIVE.value, 'position': 'pos-3', 'location': 'loc-4'}),
      generate_employee({'organization': 'org-b', 'status': EmployeeStatus.NOT_STARTED.value}),

      generate_employee({'organization': 'org-c', 'status': EmployeeStatus.ACTIVE.value, 'department': 'dep-1'}),
  ]
  session.bulk_save_objects(objects)
  session.commit()
  session.close()

def check_organization(expected_org, data):
  for employee in data['employees']:
    assert employee['organization'] == expected_org

def check_columns(user_id, cols):
  cols = set(cols) - set(['id', 'first_name', 'last_name', 'organization', 'status'])
  expected_cols = set(USER_ID_TO_ORGS[user_id]['columns'])
  assert expected_cols == cols

def check_last_seen_id(last_seen_id, data):
  for employee in data['employees']:
    assert employee['id'] < last_seen_id

insert_employees()
client = TestClient(app)

def test_read_root():
  reset_cache()
  response = client.get("/")
  assert response.status_code == 200
  assert response.json() == {"Hello": "World"}

def test_search_without_token():
  reset_cache()
  response = client.get("/search", params={})
  assert response.status_code == 401

def test_search_with_token():
  reset_cache()
  response = client.get("/search", headers={'Access-Token': 'token_a'}, params={})
  assert response.status_code == 200

def test_search_with_token_and_rate_limit():
  reset_cache()
  for i in range(REQUEST_RATE_LIMIT_COUNT):
    response = client.get("/search", headers={'Access-Token': 'token_a'}, params={})
    assert response.status_code == 200

  for i in range(3):
    response = client.get("/search", headers={'Access-Token': 'token_a'}, params={})
    assert response.status_code == 429

  time.sleep(REQUEST_RATE_LIMIT_WINDOW_SECONDS)

  for i in range(REQUEST_RATE_LIMIT_COUNT):
    response = client.get("/search", headers={'Access-Token': 'token_a'}, params={})
    assert response.status_code == 200

  for i in range(3):
    response = client.get("/search", headers={'Access-Token': 'token_a'}, params={})
    assert response.status_code == 429

def test_search_with_token_a():
  reset_cache()
  response = client.get("/search", headers={'Access-Token': 'token_a'}, params={})
  assert response.status_code == 200
  data = response.json()
  assert len(data['employees']) == 6
  check_organization('org-a', data)
  check_columns('user_a', list(data['employees'][0].keys()))

  response = client.get("/search", headers={'Access-Token': 'token_a'}, params={'status': 'active'})
  assert response.status_code == 200
  data = response.json()
  assert len(data['employees']) == 3
  check_organization('org-a', data)

  response = client.get("/search", headers={'Access-Token': 'token_a'}, params={'status': 'active,terminated'})
  assert response.status_code == 200
  data = response.json()
  assert len(data['employees']) == 4
  check_organization('org-a', data)

  response = client.get("/search", headers={'Access-Token': 'token_a'}, params={'status': 'active,not_started,terminated'})
  assert response.status_code == 200
  data = response.json()
  assert len(data['employees']) == 6
  check_organization('org-a', data)

  response = client.get("/search", headers={'Access-Token': 'token_a'}, params={'status': 'active,not_started,terminated', 'location': 'loc-4'})
  assert response.status_code == 200
  data = response.json()
  assert len(data['employees']) == 4
  check_organization('org-a', data)

def test_search_with_token_b():
  reset_cache()
  response = client.get("/search", headers={'Access-Token': 'token_b'}, params={})
  assert response.status_code == 200
  data = response.json()
  assert len(data['employees']) == 3
  check_organization('org-b', data)
  check_columns('user_b', list(data['employees'][0].keys()))

  response = client.get("/search", headers={'Access-Token': 'token_b'}, params={'status': 'active'})
  assert response.status_code == 200
  data = response.json()
  assert len(data['employees']) == 2
  check_organization('org-b', data)

  response = client.get("/search", headers={'Access-Token': 'token_b'}, params={'status': 'terminated'})
  assert response.status_code == 200
  data = response.json()
  assert len(data['employees']) == 0

  response = client.get("/search", headers={'Access-Token': 'token_b'}, params={'status': 'active,not_started,terminated'})
  assert response.status_code == 200
  data = response.json()
  assert len(data['employees']) == 3
  check_organization('org-b', data)

def test_search_with_token_c():
  reset_cache()
  response = client.get("/search", headers={'Access-Token': 'token_c'}, params={})
  assert response.status_code == 200
  data = response.json()
  assert len(data['employees']) == 1
  check_organization('org-c', data)
  check_columns('user_c', list(data['employees'][0].keys()))

  response = client.get("/search", headers={'Access-Token': 'token_c'}, params={'status': 'active'})
  assert response.status_code == 200
  data = response.json()
  assert len(data['employees']) == 1
  check_organization('org-c', data)

  response = client.get("/search", headers={'Access-Token': 'token_c'}, params={'status': 'not_started'})
  assert response.status_code == 200
  data = response.json()
  assert len(data['employees']) == 0
  check_organization('org-c', data)

  response = client.get("/search", headers={'Access-Token': 'token_c'}, params={'status': 'active', 'position': 'pos-3', 'location': 'loc-4'})
  assert response.status_code == 200
  data = response.json()
  assert len(data['employees']) == 0
  check_organization('org-c', data)


def test_search_with_token_a_and_paging():
  reset_cache()
  limit = 2

  response = client.get("/search", headers={'Access-Token': 'token_a'}, params={'limit': limit})
  assert response.status_code == 200
  data = response.json()
  assert len(data['employees']) == limit
  assert data['limit'] == limit
  assert data['has_next_page'] == True
  assert data['has_previous_page'] == False

  last_seen_id = data['employees'][-1]['id']
  response = client.get("/search", headers={'Access-Token': 'token_a'}, params={'limit': limit, 'last_seen_id': last_seen_id})
  assert response.status_code == 200
  data = response.json()
  assert len(data['employees']) == limit
  check_last_seen_id(last_seen_id, data)
  assert data['limit'] == limit
  assert data['has_next_page'] == True
  assert data['has_previous_page'] == True
  
  last_seen_id = data['employees'][-1]['id']
  response = client.get("/search", headers={'Access-Token': 'token_a'}, params={'limit': limit, 'last_seen_id': last_seen_id})
  assert response.status_code == 200
  data = response.json()
  assert len(data['employees']) == limit
  check_last_seen_id(last_seen_id, data)
  assert data['limit'] == limit
  assert data['has_next_page'] == False
  assert data['has_previous_page'] == True

  response = client.get("/search", headers={'Access-Token': 'token_a'}, params={'limit': limit + 1, 'last_seen_id': last_seen_id})
  assert response.status_code == 200
  data = response.json()
  assert len(data['employees']) < limit + 1
  check_last_seen_id(last_seen_id, data)
  assert data['limit'] == limit + 1
  assert data['has_next_page'] == False
  assert data['has_previous_page'] == True

  last_seen_id = data['employees'][-1]['id']
  response = client.get("/search", headers={'Access-Token': 'token_a'}, params={'limit': limit, 'last_seen_id': last_seen_id})
  assert response.status_code == 200
  data = response.json()
  assert len(data['employees']) == 0
  assert data['limit'] == limit
  assert data['has_next_page'] == False
  assert data['has_previous_page'] == True