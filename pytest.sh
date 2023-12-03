rm sql_app.db
alembic -c alembic.test.ini upgrade head
pytest app