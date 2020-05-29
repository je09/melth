# Logs
import logging
from logging import handlers

logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
file_handler = handlers.RotatingFileHandler('melth.log', mode='a', encoding='utf-8', maxBytes=10*1024*1024)
format_ = logging.Formatter('%(asctime)s (%(levelname)s) - %(message)s')

console_handler.setFormatter(format_)
file_handler.setFormatter(format_)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

logger.setLevel(logging.getLevelName(0))

logger.info('Started')
