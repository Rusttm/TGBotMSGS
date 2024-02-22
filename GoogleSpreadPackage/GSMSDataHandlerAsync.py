# -*- coding: utf-8 -*-
# from https://gspread-asyncio.readthedocs.io/en/latest/
from GoogleSpreadPackage.GSMainClass import GSMainClass
import asyncio
import os
# from https://stackoverflow.com/questions/879173/how-to-ignore-deprecation-warnings-in-python
# its hide pandas deprecation information
def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn
import pandas as pd
import numpy as np


class GSMSDataHandlerAsync(GSMainClass):
    """ data handler """
    logger_name = f"{os.path.basename(__file__)}"
    _dir_name = "config"
    data_dir_name = "data"

    def __init__(self):
        super().__init__()

    async def convert_ms_dict_2df_async(self, ms_data: dict) -> pd.DataFrame:
        """ gets data {data:[], col_list: [] }"""
        spread_sheet_df = pd.DataFrame()
        try:
            columns = ms_data.get("col_list")
            data = ms_data.get("data")
            spread_sheet_df = pd.DataFrame(data, columns=columns)
            spread_sheet_df.replace({np.nan: 0}, inplace=True)
        except Exception as e:
            msg = f"{__class__.__name__} cant convert {ms_data} to Dataframe, Error: \n {e} "
            self.logger.warning(msg)
            print(msg)
        return spread_sheet_df



if __name__ == "__main__":
    import time

    start_time = time.time()
    bal_dict = {'data': {
            'Дата': '11.02.24 16:17',
            'деньги на счетах': 1858546,
            'склад себестоимость': 31512481,
            'другие': 710918,
            'москваконтрагенты': 450593,
            'поставщики': 2984930,
            'новосибирскконтрагенты': 698376,
            'покупатели пфо': 0,
            'Итог': 38215844},
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
    connect = GSMSDataHandlerAsync()
    print(asyncio.run(
        connect.convert_ms_dict_2df_async(ms_data=bal_dict)))
    print(f"report done in {int(time.time() - start_time)}sec at {time.strftime('%H:%M:%S', time.localtime())}")
