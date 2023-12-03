try:
  from .cache import timed_lru_cache
except:
  from cache import timed_lru_cache

TOKEN_TO_USERS = {
  'token_a': { 'id': 'user_a' },
  'token_b': { 'id': 'user_b' },
  'token_c': { 'id': 'user_c' },
}

@timed_lru_cache(5)
def get_user(token: str):
  if token in TOKEN_TO_USERS:
    return TOKEN_TO_USERS[token]
