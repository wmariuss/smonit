import os
import logging


logging.basicConfig(
    filename="/var/log/smonit.log",
    format="%(asctime)s - %(levelname)s, %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    level=os.environ.get("LOGLEVEL", "INFO"),
)

logging.getLogger(__name__)
