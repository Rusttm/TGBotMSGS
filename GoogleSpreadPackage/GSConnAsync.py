# -*- coding: utf-8 -*-
# from https://gspread-asyncio.readthedocs.io/en/latest/
import gspread_asyncio
from GoogleSpreadPackage.GSMainClass import GSMainClass
import asyncio
import os
from google.oauth2.service_account import Credentials
# from https://stackoverflow.com/questions/46827007/runtimeerror-this-event-loop-is-already-running-in-python
import nest_asyncio

nest_asyncio.apply()


class GSConnAsync(GSMainClass):
    """ google sheet asynchronous connector it creates google_spread_client 'async_gc'
    that used in other classes"""
    logger_name = f"{os.path.basename(__file__)}"
    _config_dir_name = "config"
    _data_dir_name = "data"
    _config_file_name = "gs_main_config.json"
    _gs_json_credentials_key = "gs_json_credentials"
    _gs_scopes_key = "gs_scopes"
    _async_gc = None

    def __init__(self):
        super().__init__()

    def get_credentials(self):
        local_path = os.path.dirname(__file__)
        credentials_file_name = self._config_data.get(self._gs_json_credentials_key)
        CREDENTIALS_FILE_PATH = os.path.join(local_path, self._config_dir_name, credentials_file_name)
        scopes = self._config_data.get(self._gs_scopes_key)
        credentials = Credentials.from_service_account_file(CREDENTIALS_FILE_PATH)
        scoped_cred = credentials.with_scopes(scopes)
        return scoped_cred

    def __create_gs_client_manager(self):
        self.__async_gspread_client_manager = gspread_asyncio.AsyncioGspreadClientManager(self.get_credentials)

    async def create_gs_client_async(self):
        self.__create_gs_client_manager()
        self._async_gc = await self.__async_gspread_client_manager.authorize()
        return self._async_gc


if __name__ == "__main__":
    import time

    start_time = time.time()
    print(f"report starts at {time.strftime('%H:%M:%S', time.localtime())}")
    connect = GSConnAsync()
    # loop = asyncio.get_event_loop()
    # result = loop.run_until_complete(self.get_api_data_async(to_file=to_file))
    # print(connect.load_conf_data())

    print(asyncio.run(connect.create_gs_client_async()))
    print(connect._async_gc)
    print(f"report done in {int(time.time() - start_time)}sec at {time.strftime('%H:%M:%S', time.localtime())}")
