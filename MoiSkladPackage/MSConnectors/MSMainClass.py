from .MSPkgLogger import MSPkgLogger
from .MSReadJsonAsync import MSReadJsonAsync
import os


class MSMainClass(MSPkgLogger, MSReadJsonAsync):
    logger_name = f"{os.path.basename(__file__)}"

    def __init__(self):
        # print("test class")
        MSPkgLogger.__init__(self)
        MSReadJsonAsync.__init__(self)

    def python_version_checker(self):
        import sys
        print(sys.version_info[0:3])
        if sys.version_info[0:3] != (3, 10, 10):
            msg = f"Python version {sys.version_info[0]}.{ sys.version_info[1]}.{sys.version_info[2]} it is not 10, please use Python3v10.10"
            self.logger.debug(msg)




if __name__ == "__main__":
    connect = MSMainClass()
    connect.logger.info("testing MainClass")
    connect.python_version_checker()
