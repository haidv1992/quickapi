import logging

import uvicorn
from app.app import app

log_config = uvicorn.config.LOGGING_CONFIG
log_config["formatters"]["access"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
log_config["formatters"]["default"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,  # Change the logging level to DEBUG
)
if __name__ == "__main__":
    uvicorn.run(app, log_config=log_config, host="0.0.0.0", log_level="info")
