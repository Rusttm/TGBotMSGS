import asyncio

import aiofiles

from MSMainClass import MSMainClass

import os
import json


class MSConfigFileAsync(MSMainClass):
    """ json configfile connector"""
    logger_name = f"{os.path.basename(__file__)}"
    _dir_name = ["config"]
    file_name = "ms_main_config.json"
    file_path = os.path
    headers_key = "ms_api_headers"

    async def _check_json_config_file(self):
        """ extract data from json config file """
        try:
            pkg_dir = os.path.dirname(__file__)
            dirs_path = pkg_dir
            for d in self.dir_name:
                dirs_path = os.path.join(dirs_path, d)
            self.file_path = os.path.join(dirs_path, self.file_name)
            if not os.path.isfile(self.file_path):
                raise FileNotFoundError(f"file {self.file_path} not found")
            # self.logger.debug(f"module {__class__.__name__} read config from {self.file_path}")
            return True
        except Exception as e:
            self.logger.error(f"{__class__.__name__} can't find config file")
            return False

    async def get_ini_json_file_async(self) -> dict:
        d = dict()
        try:
            file_exists = await self._check_json_config_file()
            if file_exists:
                async with aiofiles.open(self.file_path, 'r') as json_file:
                    json_data = await json_file.read()
                d = json.loads(json_data)
        except Exception as e:
            self.logger.debug(f"module {__class__.__name__} can't read data from config file")
        else:
            self.header_dict = d.get(self.headers_key)
        return d

    def get_ini_json_file_sync(self) -> dict:
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(self.get_ini_json_file_async())
        # result = asyncio.run(self.get_ini_json_file_async())
        return result

    async def get_req_headers_async(self) -> dict:
        return self.header_dict


if __name__ == '__main__':
    connector = MSConfigFileAsync()
    print(asyncio.run(connector.get_ini_json_file_async()))
    # print(connector.get_req_headers_async())
