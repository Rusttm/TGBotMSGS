# -*- coding: utf-8 -*-
# from https://gspread-asyncio.readthedocs.io/en/latest/
import datetime

from GoogleSpreadPackage.GSConnAsync import GSConnAsync
import asyncio
import os


# from https://stackoverflow.com/questions/879173/how-to-ignore-deprecation-warnings-in-python
# its hide pandas deprecation information
def warn(*args, **kwargs):
    pass


import warnings

warnings.warn = warn
import pandas as pd


class GSMSContAsync(GSConnAsync):
    """ data handler """
    logger_name = f"{os.path.basename(__file__)}"
    _gs_names_key = "gs_names"
    _ws_id_key = "ws_id"
    _async_gc = None

    def __init__(self):
        super().__init__()

    async def save_data_ms_gs_async(self, ms_data: dict, gs_tag: str, insert=False, ws_id: int = None) -> pd.DataFrame:
        df = pd.DataFrame()
        try:
            self._async_gc = await self.create_gs_client_async()
            gs_id = self._config_data.get(self._gs_names_key).get(gs_tag)
            if not ws_id:
                ws_id = self._config_data.get(self._ws_id_key).get(gs_tag)
            from GoogleSpreadPackage.GSMSDataHandlerAsync import GSMSDataHandlerAsync
            handler = GSMSDataHandlerAsync()
            df = await handler.convert_ms_dict_2df_async(ms_data=ms_data)
            spread_sheet = await self._async_gc.open_by_key(gs_id)
            work_sheet = await spread_sheet.get_worksheet_by_id(ws_id)
            # df = pd.DataFrame(await work_sheet.get_all_values())
            if insert:
                await work_sheet.clear()
                await work_sheet.insert_rows([df.columns.values.tolist()] + df.values.tolist())
            else:
                await work_sheet.append_rows(df.values.tolist())
        except Exception as e:
            msg = f"{__class__.__name__} cant get spreadsheet metadata, Error: \n {e} "
            self.logger.warning(msg)
            print(msg)
        return df

    async def save_data_ms_gs_id_async(self, ms_data: dict, gs_id: str, insert=False, ws_id: int = None, time_col=False) -> pd.DataFrame:
        df = pd.DataFrame()
        try:
            self._async_gc = await self.create_gs_client_async()
            from GoogleSpreadPackage.GSMSDataHandlerAsync import GSMSDataHandlerAsync
            handler = GSMSDataHandlerAsync()
            df = await handler.convert_ms_dict_2df_async(ms_data=ms_data)
            if time_col:
                # df["rep_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                df.insert(0, "rep_time", datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
            spread_sheet = await self._async_gc.open_by_key(gs_id)
            if not ws_id:
                ws_id = 0
                gs_tag_id_dict = self._config_data.get(self._gs_names_key)
                for tag, id in gs_tag_id_dict.items():
                    if id == gs_id:
                        ws_id = self._config_data.get(self._ws_id_key).get(tag)
                        break
            work_sheet = await spread_sheet.get_worksheet_by_id(ws_id)
            # df = pd.DataFrame(await work_sheet.get_all_values())
            if insert:
                await work_sheet.clear()
                await work_sheet.insert_rows([df.columns.values.tolist()] + df.values.tolist())
            else:
                await work_sheet.append_rows(df.values.tolist())
        except Exception as e:
            msg = f"{__class__.__name__} cant get spreadsheet metadata, Error: \n {e} "
            self.logger.warning(msg)
            print(msg)
        return df

if __name__ == "__main__":
    import time

    start_time = time.time()
    ms_data = {'data': {
        'Дата': '11.02.24 16:17',
        'деньги на счетах': 1,
        'склад себестоимость': 31,
        'другие': 71,
        'москваконтрагенты': 4593,
        'поставщики': 20,
        'новосибирскконтрагенты': 6986,
        'покупатели пфо': 0,
        'Итог': 384},
        'col_list':
            ['Дата',
             'Итог',
             'деньги на счетах',
             'склад себестоимость',
             'поставщики',
             'новосибирскконтрагенты',
             'москваконтрагенты',
             'покупатели пфо',
             'другие']}
    print(f"report starts at {time.strftime('%H:%M:%S', time.localtime())}")
    connect = GSMSContAsync()
    # print(asyncio.run(
    #     connect.get_spreadsheet_ws_names_list_async(spread_sheet_id="1YtCslaQVP06Mqxr4I2xYn3w62teS5qd6ndN_MEU_jeE")))
    # print(asyncio.run(
    #     connect.save_data_ms_gs_async(ms_data=ms_data, gs_tag="gs_test", insert=True)))

    print(asyncio.run(
        connect.save_profit_ms_gs_async(ms_data=ms_data)))

    print(f"report done in {int(time.time() - start_time)}sec at {time.strftime('%H:%M:%S', time.localtime())}")
