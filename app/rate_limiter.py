import time

try:
  from .cache import get_cache, set_cache
except:
  from cache import get_cache, set_cache


REQUEST_RATE_LIMIT_COUNT = 5 # requests
REQUEST_RATE_LIMIT_WINDOW_SECONDS = 5 # seconds

def check_rate_limit(request):
  base_key = f"user:{request.scope['user']['id']}:method:{request.scope['method']}:path:{request.scope['path']}"
  count_key = f"{base_key}:count"
  expired_at_key = f"{base_key}:expired_at"
  count = get_cache(count_key)
  expired_at = get_cache(expired_at_key)

  print(f"count {count} | expired_at {expired_at} | {time.time()}")

  if count is None or expired_at is None:
    set_cache(count_key, 1)
    set_cache(expired_at_key, time.time() + REQUEST_RATE_LIMIT_WINDOW_SECONDS)
    return True

  if expired_at < time.time():
    set_cache(count_key, 1)
    set_cache(expired_at_key, time.time() + REQUEST_RATE_LIMIT_WINDOW_SECONDS)
    return True

  if count >= REQUEST_RATE_LIMIT_COUNT:
    return False

  set_cache(count_key, count + 1)
  return True
