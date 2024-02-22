from MoiSkladPackage.MSConnectors.MSMainClass import MSMainClass
import os
import json
import re


class MSSaveJson(MSMainClass):
    """ connector: save dictionary data file to json """
    logger_name = f"{os.path.basename(__file__)}"
    _dir_name = "../data"
    file_name = "ms_requested_data.json"

    def save_data_json_file(self, data_dict=None, file_name=None, dir_name=None):
        """ save dictionary data file to json
        return True or False"""
        try:
            if file_name:
                self.file_name = self.corrected_file_name(file_name)
            # if dir_name == "config":
            if dir_name:
                self.dir_name = dir_name
            dir_file = os.path.dirname(__file__)
            dir_path = os.path.join(dir_file, self.dir_name)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            DATA_FILE_PATH = os.path.join(dir_path, f"{self.file_name}")
            if not os.path.exists(DATA_FILE_PATH):
                open(DATA_FILE_PATH, 'x')
            if os.path.exists(DATA_FILE_PATH) and data_dict:
                with open(DATA_FILE_PATH, 'w') as ff:
                    json.dump(data_dict, ff, ensure_ascii=False)
                self.logger.debug(f"{__class__.__name__} saved data to json file {DATA_FILE_PATH}")
                return True
            else:
                self.logger.error(f"{__class__.__name__} can't read json file, it doesnt exist!")
                # print(f"{__class__.__name__} can't write data to file {self.file_name}")
                return False
        except Exception as e:
            self.logger.error(f"{__class__.__name__} can't write to json file! {e}")
            # print(e)
        # finally:
        #     return False

    def corrected_file_name(self, file_name):
        """ return corrected file name in filename.json"""
        if re.search("json", file_name):
            return file_name
        else:
            return f"{file_name}.json"


if __name__ == '__main__':
    connector = MSSaveJson()
    print(connector.save_data_json_file(data_dict={"data": "some data"}, file_name="temporary_file"))
