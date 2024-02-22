# -*- coding: utf-8 -*-
from GSConnAsync import GSConnAsync
import os
import asyncio

class GSSaveDataAsync(GSConnAsync):
    """ google sheet asynchronous writer"""
    logger_name = f"{os.path.basename(__file__)}"

    def __init__(self):
        super().__init__()


    async def upd_spreadsheet_title_async(self, spread_sheet_id: str, new_title: str) -> bool:
        """ update title of spreadsheet"""
        try:
            spread_sheet = await self._async_gc.open_by_key(spread_sheet_id)
            await spread_sheet.update_title(new_title)
            return True
        except Exception as e:
            msg = f"{__class__.__name__} cant get rename spreadsheet, Error: \n {e} "
            self.logger.warning(msg)
            print(msg)
            return False

    async def clear_ws_all_async(self, spread_sheet_id: str, ws_name: str) -> bool:
        """ clear all data in spreadsheet"""
        try:
            import GSGetInfoAsync
            connector = GSGetInfoAsync.GSGetInfoAsync()
            name_is_in_ws = await connector.check_ws_name_is_exist(spread_sheet_id, ws_name)
            if not name_is_in_ws: raise AttributeError
            ws_id = await connector.get_ws_id_by_name_async(spread_sheet_id, ws_name)
            spread_sheet = await self._async_gc.open_by_key(spread_sheet_id)
            work_sheet = await spread_sheet.get_worksheet_by_id(ws_id)
            # clear data
            await work_sheet.clear()
            # clear notes
            await work_sheet.clear_notes()
            # clear filters
            await work_sheet.clear_basic_filter()
            return True
        except Exception as e:
            msg = f"{__class__.__name__} cant get rename spreadsheet, Error: \n {e} "
            self.logger.warning(msg)
            print(msg)
            return False



if __name__ == "__main__":
    import time

    start_time = time.time()
    print(f"report starts at {time.strftime('%H:%M:%S', time.localtime())}")
    connect = GSSaveDataAsync()
    # loop = asyncio.get_event_loop()
    # result = loop.run_until_complete(self.get_api_data_async(to_file=to_file))
    # print(connect.load_conf_data())
    # print(asyncio.run(connect.save_spreadsheet_csv_async(spread_sheet_id="1YtCslaQVP06Mqxr4I2xYn3w62teS5qd6ndN_MEU_jeE")))
    # print(
    #     asyncio.run(connect.get_spreadsheet_metadata_async(spread_sheet_id="1YtCslaQVP06Mqxr4I2xYn3w62teS5qd6ndN_MEU_jeE")))
    print(asyncio.run(
            connect.upd_spreadsheet_title_async(spread_sheet_id="1YtCslaQVP06Mqxr4I2xYn3w62teS5qd6ndN_MEU_jeE",
                                                new_title="NewName")))

    # ws = asyncio.run(connect.add_worksheet_2spreadsheet(spread_sheet=ss))
    # print(ws)
    print(f"report done in {int(start_time - time.time())}sec at {time.strftime('%H:%M:%S', time.localtime())}")
