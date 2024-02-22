from MoiSkladPackage.MSConnectors.MSMainClass import MSMainClass
import json
import os
import re


class MSReadJson(MSMainClass):
    """read and return data from json file"""
    logger_name = f"{os.path.basename(__file__)}"
    _dir_name = "../data"

    def get_config_json_data(self, file_name=None) -> dict:
        """ extract data from MS json file
        return dict """
        data = dict()
        if file_name:
            try:
                file_dir = os.path.dirname(__file__)
                if not re.search('json', file_name):
                    file_name += '.json'
                CONF_FILE_PATH = os.path.join(file_dir, self.dir_name, file_name)
                with open(CONF_FILE_PATH) as json_file:
                    data = json.load(json_file)
                self.logger.debug(f"{__class__.__name__} got data from json file")
            except Exception as e:
                # print(e)
                self.logger.error(f"{__class__.__name__} can't read json file!{e}")
        else:
            import errno
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT),
                                    "Please, declare existing json file name with 'file_name='")
        return data

if __name__ == '__main__':
    connector = MSReadJson()
    print(connector.get_config_json_data(file_name='url_money.json'))
