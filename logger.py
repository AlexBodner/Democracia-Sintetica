import logging


logger = logging.getLogger("debate_logger")
logger.setLevel(logging.DEBUG) 

formatter = logging.Formatter(
    '[%(asctime)s] [%(levelname)s] %(name)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

file_handler = logging.FileHandler("debate_system.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
