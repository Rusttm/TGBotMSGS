from MoiSkladPackage.MSConnectors.MSMainClass import MSMainClass
import requests
import re
import os

class MSRequester(MSMainClass):
    """ clas request to moisklad api"""
    logger_name = f"{os.path.basename(__file__)}"
    ms_urls_key = "ms_urls"
    ms_api_header = "ms_api_headers"
    offset = 1000
    __api_url = str()
    __api_header = dict()
    __api_param_line = "?"
    __to_file = False
    __file_name = "requested_data.json"

    def __init__(self):
        super().__init__()

    def set_config(self, url_conf_key=None):
        """it sets requested url and token in configuration """
        from MoiSkladPackage.archive.MSConfigFile import MSConfigFile
        try:
            conf_connector = MSConfigFile()
            configuration = conf_connector.get_ini_json_file()
            self.__file_name = url_conf_key
            self.set_api_url(configuration[self.ms_urls_key].get(url_conf_key))
            self.set_api_header(configuration[self.ms_api_header])

        except Exception as e:
            self.logger.error("Cant read configuration!", e)

    def set_api_config(self, api_url=None, api_header=None, api_param_line=None, to_file=False):
        self.__api_url = api_url
        self.__api_header = api_header
        self.__api_param_line = api_param_line
        self.__to_file = to_file

    def set_api_header(self, api_token=None):
        self.__api_header = api_token

    def set_api_url(self, api_url=None):
        self.__api_url = api_url

    def set_api_param_line(self, api_param_line=None):
        """ set new request parameters in url line """
        if api_param_line:
            if self.__api_param_line == "?":
                self.__api_param_line += api_param_line
            elif self.__api_param_line != "?":
                self.__api_param_line = "?" + api_param_line
        else:
            self.__api_param_line = "?"
        # self.__api_param_line = api_param_line

    def add_api_param_line(self, add_param_line=None):
        """ add request parameters in current url line"""
        if self.__api_param_line == "?":
            self.__api_param_line += add_param_line
        elif self.__api_param_line == "":
            self.__api_param_line += "?" + add_param_line
        elif self.__api_param_line != "?":
            # checking and exclude offset in request string
            x = re.split("&offset", self.__api_param_line)
            self.__api_param_line = x[0] + "&" + add_param_line
        else:
            self.__api_param_line = ""

    def get_single_req_data(self):
        """ api connect and get data in one request
        return dictionary!"""
        api_url = self.__api_url + self.__api_param_line
        try:
            # self.logger.info(f"{pathlib.PurePath(__file__).name} make request")
            self.logger.info(f"{__class__.__name__} make request")
            acc_req = requests.get(url=api_url, headers=self.__api_header)
            req_data = dict(acc_req.json())
            req_err = req_data.get('errors', False)
            if req_err:
                # check errors in request
                errors_request = acc_req.json()['errors']
                for error in errors_request:
                    self.logger.error(
                        # f"{pathlib.PurePath(__file__).name} requested information has errors: "
                        f"{__class__.__name__} requested information has errors: "
                        f"{error['error']} (code {error['code']}) ")
            else:
                # self.logger.info(f"{pathlib.PurePath(__file__).name} request successful - data has context ")
                self.logger.info(f"{__class__.__name__} request successful - data has context ")

            return dict(acc_req.json())
        except Exception as e:
            # print('Cant read account data', Exception)
            self.logger.critical(f"{__class__.__name__} cant connect to request data: {e}")
            return None

    def get_api_data(self, to_file=False):
        """ if there are more than 1000 positions
        needs to form request for getting full data"""
        self.__to_file = to_file
        # starts first request
        data = dict(self.get_single_req_data())
        delta = 0
        try:
            # check full length of data by data['meta']['size']
            delta = int(data['meta']['size']) - int(data['meta']['offset'])
        except Exception as e:
            # if there is no data in data['meta']['size']
            self.logger.warning(f"{__class__.__name__} cant find key {e} for data['meta']['size'] ")
        # if there is more than 1000 positions in row
        if delta > self.offset:
            # self.logger.info(f"{pathlib.PurePath(__file__).name} request contains more than 1000rows")
            self.logger.info(f"{__class__.__name__} request contains more than 1000rows")
            requests_num = delta // self.offset
            for i in range(requests_num):
                # .. request data until it ends
                self.add_api_param_line(f"offset={(i + 1) * 1000}")
                next_data = self.get_single_req_data()
                data['rows'] += next_data['rows']

        if self.__to_file:
            self.save_requested_data_2file(data_dict=data)
        return data

    def save_requested_data_2file(self, data_dict=None, file_name=None):
        """ method save dict data to file in class ConnMSSaveFile"""
        from MSSaveJson import MSSaveJson
        if file_name:
            self.__file_name = file_name
        self.logger.debug(f"{__name__} starts write request to file {self.__file_name}")
        result = False
        try:
            result = MSSaveJson().save_data_json_file(data_dict=data_dict, file_name=self.__file_name)
        except Exception as e:
            self.logger.error(f"{__class__.__name__} request wasn't wrote to file {self.__file_name} exception {e}")
        if result:
            self.logger.debug(f"request was wrote to file {self.__file_name}")
        else:
            self.logger.error(f"{__class__.__name__} request wasn't wrote to file {self.__file_name}")

if __name__ == "__main__":
    connect = MSRequester()
    connect.set_config("url_stock_all")
    connect.get_api_data(to_file=True)