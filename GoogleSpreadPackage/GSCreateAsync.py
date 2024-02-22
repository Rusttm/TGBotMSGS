# -*- coding: utf-8 -*-

import os
from GSMainClass import GSMainClass
from GSConnAsync import GSConnAsync
import asyncio
# from https://gspread-asyncio.readthedocs.io/en/latest/
import gspread_asyncio


class GSCreateAsync(GSConnAsync):
    """ google sheet asynchronous writer"""
    logger_name = f"{os.path.basename(__file__)}"

    def __init__(self):
        super().__init__()


    async def create_gsheet_and_full_permission(self,
                                                spread_sheet_name=None) -> gspread_asyncio.AsyncioGspreadSpreadsheet:
        """ create new sheet, give full access permission and return obj spread_sheet"""
        try:
            self._async_gc = await self.create_gs_client_async()
            if not spread_sheet_name: spread_sheet_name = "Test spread sheet"
            spread_sheet = await self._async_gc.create(spread_sheet_name)
            spread_sheet_href = f"https://docs.google.com/spreadsheets/d/{spread_sheet.id}"
            # Allow anyone with the URL to write to this spreadsheet.
            await self._async_gc.insert_permission(spread_sheet.id, None, perm_type="anyone", role="writer")
            # print(f"{type(spread_sheet)=}") # <class 'gspread_asyncio.AsyncioGspreadSpreadsheet'>
            msg = f"created spreadsheet {spread_sheet_href}"
            print(msg)
            self.logger.info(msg)
            return spread_sheet
        except Exception as e:
            msg = f"{__class__.__name__} cant create google spread sheet {spread_sheet_name=}, Error: \n {e}"
            self.logger.warning(msg)
            return None

    async def add_worksheet_2spreadsheet(self, spread_sheet_id=None, spread_sheet=None, work_sheet_name=None) -> object:
        try:
            self._async_gc = await self.create_gs_client_async()
            if spread_sheet_id:
                spread_sheet = await self._async_gc.open_by_key(spread_sheet_id)
            if spread_sheet:
                if not work_sheet_name:
                    work_sheet_name = "new_sheet"
                from GSGetInfoAsync import GSGetInfoAsync
                ws_names_list = await GSGetInfoAsync().get_spreadsheet_ws_names_list_async(spread_sheet_id)
                while work_sheet_name in ws_names_list:
                    last_symbol = work_sheet_name[-1:]
                    if last_symbol in [str(n) for n in range(10)]:
                        last_symbol = str(int(last_symbol) + 1)
                    else:
                        last_symbol = '1'
                    work_sheet_name = work_sheet_name[:-1] + last_symbol
                work_sheet = await spread_sheet.add_worksheet(work_sheet_name, 10, 15)
                msg = f"{__class__.__name__} creates worksheet {work_sheet_name} in {spread_sheet_id=}"
                self.logger.debug(msg)
                return work_sheet

            else:
                print(f"Не указан spread_sheet для добавления листа")
                return None
        except Exception as e:
            msg = f"{__class__.__name__} cant add worksheet to {spread_sheet_id=}, Error: \n {e}"
            self.logger.error(msg)
            return None



if __name__ == "__main__":
    import time

    start_time = time.time()
    print(f"report starts at {time.strftime('%H:%M:%S', time.localtime())}")
    connect = GSCreateAsync()
    # loop = asyncio.get_event_loop()
    # result = loop.run_until_complete(self.get_api_data_async(to_file=to_file))
    # print(connect.load_conf_data())
    # print(asyncio.run(connect.create_gsheet_and_full_permission(spread_sheet_name="Temporary spreadsheet")))
    print(asyncio.run(connect.add_worksheet_2spreadsheet(spread_sheet_id="1YtCslaQVP06Mqxr4I2xYn3w62teS5qd6ndN_MEU_jeE",
                                                         work_sheet_name="My new sheet3")))
    # ws = asyncio.run(connect.add_worksheet_2spreadsheet(spread_sheet=ss))
    # print(ws)
    print(f"report done in {int(start_time - time.time())}sec at {time.strftime('%H:%M:%S', time.localtime())}")
