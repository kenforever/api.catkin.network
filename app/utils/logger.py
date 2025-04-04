import logging
import os
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# create log folder if not exists
if not os.path.exists("app/logs"):
    os.makedirs("app/logs")

stream = logging.StreamHandler()
file = logging.FileHandler(
    filename=f'app/logs/{datetime.now().strftime("%Y-%m-%d")}.log'
)

formatter = logging.Formatter(
    fmt="%(name)-8s | %(levelname)s | %(asctime)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

stream.setFormatter(formatter)
file.setFormatter(formatter)
logger.addHandler(stream)
logger.addHandler(file)
