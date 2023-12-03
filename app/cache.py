from functools import lru_cache, wraps
from datetime import datetime, timedelta

global_cache = {}

def set_cache(key, value):
  global global_cache
  global_cache[key] = value

def get_cache(key):
  global global_cache
  if key in global_cache:
    return global_cache[key]

def reset_cache():
  global global_cache
  global_cache = {}

def timed_lru_cache(seconds: int, maxsize: int = 128):
  def wrapper_cache(func):
    func = lru_cache(maxsize=maxsize)(func)
    func.lifetime = timedelta(seconds=seconds)
    func.expiration = datetime.utcnow() + func.lifetime

    @wraps(func)
    def wrapped_func(*args, **kwargs):
      if datetime.utcnow() >= func.expiration:
        func.cache_clear()
        print('cache_clear...')
        func.expiration = datetime.utcnow() + func.lifetime

      return func(*args, **kwargs)

    return wrapped_func

  return wrapper_cache
