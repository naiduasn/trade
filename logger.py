import logging
import sys

# Create a logger
logger = logging.getLogger("my_logger")
logger.setLevel(logging.INFO)

# Create a file handler to write logs to a file
file_handler = logging.FileHandler("logs.log")
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Redirect stdout and stderr to the logger and file
class StreamToLogger:
    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())

    def flush(self):
        pass

sys.stdout = StreamToLogger(logger)
sys.stderr = StreamToLogger(logger, logging.ERROR)
