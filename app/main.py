from typing import Annotated, Union, List

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi import Query, Header

try:
  from .rate_limiter import check_rate_limit
  from .users import get_user
  from . import search_engine
  from . import schemas
except:
  from rate_limiter import check_rate_limit
  from users import get_user
  import search_engine
  import schemas

app = FastAPI(
  title="Search Engine - FastAPI",
  openapi_url="/openapi.json",
  docs_url="/docs",
)

@app.middleware("http")
async def check_rate_limit_middleware(request: Request, call_next):
    if 'user' in request.scope:
      if check_rate_limit(request) is False:
        return JSONResponse(
            None,
            429,
            { 'error': 'You sent too many requests. Please wait a while then try again'}
          )

    return await call_next(request)

@app.middleware("http")
async def authenticate_middleware(request: Request, call_next):
    if request.scope['path'] != '/search':
       return await call_next(request)

    token = request.headers.get('Access-Token')        
    user = get_user(token)

    if user is None:
        return JSONResponse(None, 401, {"error": "Permission is required."})

    request.scope['user'] = user
    return await call_next(request)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/search", response_model=schemas.EmployeePage, response_model_exclude_none=True)
def search(
    status: List[str] = Query(None),
    location: str | None = None,
    company: str | None = None,
    department: str | None = None,
    position: str | None = None,
    limit: int | None = 10,
    last_seen_id: int | None = None,
    access_token: Annotated[Union[str, None], Header(alias='Access-Token')] = None
  ):
  status_str = '' if status is None else ','.join(sorted(status))
  return search_engine.search(
    token=access_token, 
    status_str=status_str, 
    location=location, 
    company=company, 
    department=department, 
    position=position, 
    limit=limit, 
    last_seen_id=last_seen_id,
  )
