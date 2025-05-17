import os
import logging
from datetime import datetime

LOG_DIR="logs"

os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE=os.path.join(LOG_DIR, f"log_{datetime.now().strftime('%Y-%m-%d')}.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def get_logger(name):
    logger=logging.getLogger(name)
    logger.setLevel(logging.INFO)

    
    return logger


