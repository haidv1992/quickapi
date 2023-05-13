from pathlib import Path

log_dir = Path(__file__).parent.parent / "logs"
log_dir.mkdir(parents=True, exist_ok=True)

bind = "0.0.0.0:8000"
workers = 4
worker_class = "uvicorn.workers.UvicornWorker"
accesslog = (log_dir / "access.log").as_posix()
errorlog = (log_dir / "error.log").as_posix()
loglevel = "debug"
