USER_ID_TO_ORGS = {
  'user_a': {
    'columns': ['contact_info', 'department', 'location', 'position'],
    'name': 'org-a',
  },
  'user_b': {
    'columns': ['department', 'location', 'position'],
    'name': 'org-b',
  },
  'user_c': {
    'columns': ['position'],
    'name': 'org-c',
  },
}

def get_org(user: dict):
  if user['id'] in USER_ID_TO_ORGS:
    return USER_ID_TO_ORGS[user['id']]
