# -*- coding: utf-8 -*-

# https://stackoverflow.com/questions/41790750/writing-files-asynchronously
import aiofiles
import gspread.utils

from GSMainClass import GSMainClass
from GSConnAsync import GSConnAsync
import asyncio
import os
# from https://gspread-asyncio.readthedocs.io/en/latest/
import gspread_asyncio


class GSExportAsync(GSConnAsync):
    """ google sheet asynchronous writer"""
    logger_name = f"{os.path.basename(__file__)}"
    _dir_name = "config"
    _data_dir_name = "data"
    _async_gc = None

    def __init__(self):
        super().__init__()

    async def save_spreadsheet_csv_async(self, spread_sheet_id: str = None,
                                         spread_sheet: gspread_asyncio.AsyncioGspreadSpreadsheet = None):
        try:
            self._async_gc = await self.create_gs_client_async()
            if spread_sheet or spread_sheet_id:
                if not spread_sheet_id:
                    spread_sheet_id = spread_sheet.id
                else:
                    spread_sheet = await self._async_gc.open_by_key(spread_sheet_id)
                binary_file_data = await self._async_gc.export(spread_sheet_id, format=gspread.utils.ExportFormat.CSV)
                file_name = spread_sheet.title + ".csv"
                file_path = os.path.join(self._data_dir_name, file_name)
                async with aiofiles.open(file_path, 'wb') as ff:
                    await ff.write(binary_file_data)
                msg = f"{__class__.__name__} converted spread_sheet {spread_sheet_id} to {file_path}"
                self.logger.debug(msg)
                return file_path
            else:
                msg = f"{__class__.__name__} cant convert to csv, "
                self.logger.warning(msg)
                print(msg)
                return None
        except Exception as e:
            msg = f"{__class__.__name__} cant convert spread_sheet {spread_sheet_id} to csv, Error: \n {e}"
            self.logger.error(msg)
            return None

    async def save_spreadsheet_xlsx_async(self, spread_sheet_id: str = None,
                                          spread_sheet: gspread_asyncio.AsyncioGspreadSpreadsheet = None):
        try:
            self._async_gc = await self.create_gs_client_async()
            if spread_sheet or spread_sheet_id:
                if not spread_sheet_id:
                    spread_sheet_id = spread_sheet.id
                else:
                    spread_sheet = await self._async_gc.open_by_key(spread_sheet_id)
                binary_file_data = await self._async_gc.export(spread_sheet_id, format=gspread.utils.ExportFormat.EXCEL)
                file_name = spread_sheet.title + ".xlsx"
                file_path = os.path.join(self._data_dir_name, file_name)
                async with aiofiles.open(file_path, 'wb') as ff:
                    await ff.write(binary_file_data)
                msg = f"{__class__.__name__} converted spread_sheet {spread_sheet_id} to {file_path}"
                self.logger.debug(msg)
                return file_path
            else:
                msg = f"{__class__.__name__} cant convert to xlsx"
                self.logger.warning(msg)
                return None
        except Exception as e:
            msg = f"{__class__.__name__} cant convert spread_sheet {spread_sheet_id} to xlsx, Error: \n {e}"
            self.logger.error(msg)
            return None


if __name__ == "__main__":
    import time

    start_time = time.time()
    print(f"report starts at {time.strftime('%H:%M:%S', time.localtime())}")
    connect = GSExportAsync()
    # loop = asyncio.get_event_loop()
    # result = loop.run_until_complete(self.get_api_data_async(to_file=to_file))
    # print(connect.load_conf_data())
    # print(asyncio.run(connect.save_spreadsheet_csv_async(spread_sheet_id="1YtCslaQVP06Mqxr4I2xYn3w62teS5qd6ndN_MEU_jeE")))
    print(
        asyncio.run(
            connect.save_spreadsheet_xlsx_async(spread_sheet_id="1YtCslaQVP06Mqxr4I2xYn3w62teS5qd6ndN_MEU_jeE")))
    # ws = asyncio.run(connect.add_worksheet_2spreadsheet(spread_sheet=ss))
    # print(ws)
    print(f"report done in {int(time.time() - start_time)}sec at {time.strftime('%H:%M:%S', time.localtime())}")
