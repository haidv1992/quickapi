QuickApi.

run for dev
```bash
uvicorn main:app --reload --reload-exclude '*/alembic/versions/*'
```

run for prod
```bash
gunicorn -c gunicorn_conf.py main:app
```

migrate
```bash
alembic revision --autogenerate 
```
run migrate
```bash
alembic upgrade head
```

upgrade

```bash
pip install -r requirements.txt --upgrade
```