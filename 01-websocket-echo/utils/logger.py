import os
import logging

os.makedirs("logs", exist_ok=True)

logger = logging.getLogger("WEBSOCKET-ECHO")
logger.setLevel(logging.INFO)

if not logger.handlers:
    file_handler = logging.FileHandler("logs/WEBSOCKET-ECHO.log")
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)