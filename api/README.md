# Development
## Dependencies
* python 3.9
* poetry
* poetry-dotenv-plugin
* npm

## Run
```
poetry run weblog
```

## Database
Create a new revision:
```
alembic revision --autogenerate -m "summary of changes"
```

Implement revisions:
```
alembic upgrade head
```
