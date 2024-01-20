import logging
import os
from pathlib import Path


logger = logging.getLogger(__name__)


def setup_logger(log_path):
    log_file = log_path / "curious_bot.log"
    if Path(log_file).is_file():
        os.rename(log_file, log_path / f'curious_bot_{ datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S") }.log')
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(filename=log_file, encoding='utf-8', mode='w')
    logger.addHandler(handler)
    return handler


