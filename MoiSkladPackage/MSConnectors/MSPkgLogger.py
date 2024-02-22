import logging
from logging.handlers import RotatingFileHandler
import os


class MSPkgLogger(object):
    logger_name = f"{os.path.basename(__file__)}"
    _logger_dir = "logs"
    logger = None

    def __init__(self):
        self.logger = logging.getLogger(self.logger_name)
        self.logger.setLevel(logging.DEBUG)
        if self.logger.hasHandlers(): self.logger.handlers.clear()
        up_file_path = os.path.dirname(os.path.dirname(__file__))
        log_file_path = os.path.join(up_file_path, self._logger_dir, self.logger_name)
        logger_handler = RotatingFileHandler(f"{log_file_path}.log", mode="a", backupCount=0, maxBytes=2 * 1024 * 1024, delay=False)
        # logger_handler = logging.FileHandler("controller.log", mode="w")
        logger_formatter = logging.Formatter("%(asctime)s,%(msecs)d %(name)s %(levelname)s msg: %(message)s")
        logger_handler.setFormatter(logger_formatter)
        self.logger.addHandler(logger_handler)


if __name__ == '__main__':
    connector = MSPkgLogger()
    connector.logger.info("resting")
