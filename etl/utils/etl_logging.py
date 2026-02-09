import logging
import sys
from datetime import datetime
from pathlib import Path


def setup_logger(name: str = "retail_lakehouse"):
    """Creates and returns a configured logger"""

    # project_root = Path(__file__).resolve().parent.parent.parent
    project_root = Path(__file__).resolve().parents[2]
    log_dir = project_root / "logs"

    log_dir.mkdir(exist_ok=True)

    log_file = log_dir / f"pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Prevent duplicate handlers if re-run
    if logger.hasHandlers():
        logger.handlers.clear()

    file_handler = logging.FileHandler(log_file)
    console_handler = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.info("Logging initialized")
    logger.info(f"Log file: {log_file}")

    return logger
