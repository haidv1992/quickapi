QuickApi.

install and upgrade

```bash
pip install -r requirements.txt --upgrade
```

run for dev
```bash
uvicorn main:app --reload --reload-exclude '*/alembic/versions/*' --reload-exclude '*/core/permissions.py'
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

sync add package to required
```bash
pip freeze > requirements.txt
```

unimstall
```bash
pip uninstall -r requirements.txt -y
```


unimstall
```bash
pip install -r requirements.txt
```

