from fastapi.testclient import TestClient

try:
  from .main import app
  from .rate_limiter import REQUEST_RATE_LIMIT_COUNT
except:
  from main import app

def test_read_root():
  client = TestClient(app)
  response = client.get("/")
  assert response.status_code == 200
  assert response.json() == {"Hello": "World"}

# def test_search():
#   # TODO
#   client = TestClient(app)
#   response = client.get("/search", params={})
#   assert response.status_code == 200

# def test_search_reach_rate_limit():
#   client = TestClient(app)
#   for i in range(REQUEST_RATE_LIMIT_COUNT):
#     client.get("/search", params={})
#   response = client.get("/search", params={})
#   assert response.status_code == 403