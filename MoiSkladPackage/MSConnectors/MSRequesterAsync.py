from MoiSkladPackage.MSConnectors.MSMainClass import MSMainClass
import requests
import asyncio
import os

class MSRequesterAsync(MSMainClass):
    """ clas request to moisklad api"""
    logger_name = f"{os.path.basename(__file__)}"
    ms_urls_key = "ms_urls"
    ms_api_header = "ms_api_headers"
    _module_conf_dir = "config"
    _module_conf_file = "ms_main_config.json"
    offset = 1000
    _module_config = None
    __api_url = str()
    __api_header = dict()
    __api_param_line = "?"
    __to_file = False
    __file_name = "requested_data.json"
    __dir_name = "data"

    def __init__(self):
        super().__init__()
        self._module_config = self.set_module_config_sync(self._module_conf_dir, self._module_conf_file)

    def set_api_param_line(self, api_param_line=None):
        """ set new request parameters in url line
        https://api.moysklad.ru/api/remap/1.2/entity/factureout?offset=2000
        """
        if api_param_line:
            if self.__api_param_line == "?":
                self.__api_param_line += api_param_line
            elif self.__api_param_line != "?":
                self.__api_param_line = "?" + api_param_line
        else:
            self.__api_param_line = "?"
        # self.__api_param_line = api_param_line

    def add_api_param_line(self, add_param_line: str = None):
        """ add request parameters in current url line example:
        https://api.moysklad.ru/api/remap/1.2/entity/factureout?offset=0&filter=moment%3C=2021-05-25
        """
        # if old line has '?'
        if self.__api_param_line == "?":
            # just add new param line
            self.__api_param_line += add_param_line
        # if param is empty
        elif self.__api_param_line == "":
            # just add '?' and new param line
            self.__api_param_line += "?" + add_param_line
        # if param line already with data ?offset=2000=filter=moment<=2022-02-22...
        elif (len(self.__api_param_line) > 1) and (add_param_line.find("ffset=")):
            first_splitter = self.__api_param_line[1:].split("&") # ['offset=0', 'filter=moment%3C=2021-05-25']
            for line in first_splitter:
                if line.find("ffset=") > 0:
                    # delete offset
                    first_splitter.remove(line)
                    break
            self.__api_param_line = "?" + "&".join(first_splitter) + "&" + add_param_line # ?filter=moment%3C=2021-05-25&offset=2000
        else:
            self.__api_param_line = ""

    async def get_single_req_data_async(self):
        """ api connect and get data in one request
        return dictionary!"""
        api_url = self.__api_url + self.__api_param_line
        try:
            # self.logger.info(f"{pathlib.PurePath(__file__).name} make request")
            self.logger.info(f"{__class__.__name__} make request")
            acc_req = await asyncio.to_thread(requests.get, url=api_url, headers=self.__api_header)
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

    async def get_api_data_async(self, url_conf_key: str, to_file=False):
        """ takes url_key ("url_stock_all")
        if there are more than 1000 positions
        needs to form request for getting full data"""
        if to_file:
            self.__file_name = url_conf_key
            self.__to_file = to_file
        try:
            # read configuration from file ms_main_config.json
            configuration = self._module_config
            test = configuration[self.ms_urls_key].get(url_conf_key)
            self.__api_url = configuration[self.ms_urls_key].get(url_conf_key)
            test2 = configuration[self.ms_api_header]
            self.__api_header = configuration[self.ms_api_header]
        except Exception as e:
            msg = f"{__class__.__name__} cant read configuration file"
            self.logger.error(msg)
        # starts first request
        data = dict(await self.get_single_req_data_async())
        delta = 0
        try:
            # check full length of data by data['meta']['size']
            delta = int(data.get('meta').get('size', 0)) - int(data.get('meta').get('offset', 0))
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
                next_data = await self.get_single_req_data_async()
                data['rows'] += next_data['rows']

        if self.__to_file:
            await self.save_requested_data_2file_async(data_dict=data)
        return data

    async def save_requested_data_2file_async(self, data_dict=None, file_name=None):
        """ method save dict data to file in class ConnMSSaveFile"""
        from MoiSkladPackage.MSConnectors.MSSaveJsonAsync import MSSaveJsonAsync
        saver = MSSaveJsonAsync()
        if file_name:
            self.__file_name = file_name
        self.logger.debug(f"{__name__} starts write request to file {self.__file_name}")
        result = False
        try:
            result = await saver.save_data_json_file_async(data_dict=data_dict, dir_name=self.__dir_name, file_name=self.__file_name)
        except Exception as e:
            self.logger.error(f"{__class__.__name__} request wasn't wrote to file {self.__file_name} exception {e}")
        if result:
            self.logger.debug(f"request was wrote to file {self.__file_name}")
        else:
            self.logger.error(f"{__class__.__name__} request wasn't wrote to file {self.__file_name}")

if __name__ == "__main__":
    connect = MSRequesterAsync()
    print(asyncio.run(connect.get_api_data_async(url_conf_key="url_money", to_file=True)))