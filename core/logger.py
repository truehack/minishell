import logging
import os

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler("logs/shell.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("MiniShell")

def log_command(command: str, success: bool, result: str = ""):
    status = "SUCCESS" if success else "ERROR"
    message = f"{command} [{status}: {result}]"
    logger.info(message)
