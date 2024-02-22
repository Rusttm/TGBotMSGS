# -*- coding: utf-8 -*-
import os
from GSGetDataAsync import GSGetDataAsync
import asyncio


class GSContGetDataAsync(GSGetDataAsync):
    """ controller for dataget from google spreads"""
    logger_name = f"{os.path.basename(__file__)}"
    _config_dir_name = "config"
    _data_dir_name = "data"

    def __init__(self):
        super().__init__()

    async def get_ws_data_from_row_async(self, spread_sheet_id: str, ws_name: str, row_num: int) -> list:
        """ return list of data in row number"""
        values_list = list()
        try:
            all_data = await self.get_all_ws_data_async(spread_sheet_id, ws_name)
        except AttributeError:
            msg = f"{__class__.__name__} worksheet {ws_name} not in spreadsheet {spread_sheet_id} "
            self.logger.warning(msg)
            print(msg)
        except Exception as e:
            msg = f"{__class__.__name__} cant get spreadsheet row list, Error: \n {e} "
            self.logger.warning(msg)
            print(msg)
        else:
            values_list = list(all_data.T[row_num])
        return values_list

    async def get_ws_data_from_col_async(self, spread_sheet_id: str, ws_name: str, col_num: int) -> list:
        """ return list of data in col"""
        values_list = list()
        try:
            all_data = await self.get_all_ws_data_async(spread_sheet_id, ws_name)
        except AttributeError:
            msg = f"{__class__.__name__} worksheet {ws_name} not in spreadsheet {spread_sheet_id} "
            self.logger.warning(msg)
            print(msg)
        except Exception as e:
            msg = f"{__class__.__name__} cant get spreadsheet row list, Error: \n {e} "
            self.logger.warning(msg)
            print(msg)
        else:
            values_list = list(all_data[col_num])
        return values_list


if __name__ == "__main__":
    import time

    start_time = time.time()
    print(f"report starts at {time.strftime('%H:%M:%S', time.localtime())}")
    connect = GSContGetDataAsync()
    row = asyncio.run(
        connect.get_ws_data_from_row_async(spread_sheet_id="1YtCslaQVP06Mqxr4I2xYn3w62teS5qd6ndN_MEU_jeE",
                                           ws_name="My new sheet",
                                           row_num=2))
    print(row)
    col = asyncio.run(
        connect.get_ws_data_from_col_async(spread_sheet_id="1YtCslaQVP06Mqxr4I2xYn3w62teS5qd6ndN_MEU_jeE",
                                           ws_name="My new sheet",
                                           col_num=2))
    print(col)

    # print(asyncio.run(
    #     connect.get_all_ws_data_async(spread_sheet_id="1YtCslaQVP06Mqxr4I2xYn3w62teS5qd6ndN_MEU_jeE",
    #                                   ws_name="My new sheet")))

    print(f"report done in {int(time.time() - start_time)}sec at {time.strftime('%H:%M:%S', time.localtime())}")
