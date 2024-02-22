import datetime
from MoiSkladPackage.MSConnectors.MSMainClass import MSMainClass
import time
import asyncio
from datetime import datetime
import os


class MSReportBalacesAsync(MSMainClass):
    """ gather balances in one jsonfile"""
    logger_name = f"{os.path.basename(__file__)}"
    _main_key = "ms_balance"
    _info_key = "info"
    _module_conf_dir = "config"
    _module_conf_file = "ms_balances_config.json"
    _conf_dir = "config"
    _conf_file = "ms_main_config"
    result_bal_columns_key = "result_bal_columns"
    _module_config: dict = None

    def __init__(self):
        super().__init__()
        self._module_config = self.set_module_config_sync(self._module_conf_dir, self._module_conf_file)

    async def get_accounts_sum_async(self) -> dict:
        res_accounts = dict({'деньги на счетах': 0})
        try:
            from MoiSkladPackage.MSReports.MSAccountSumAsync import MSAccountSumAsync
            ini_dict = MSAccountSumAsync()
            res_accounts['деньги на счетах'] = await ini_dict.get_account_summ_async()
        except Exception as e:
            msg = f"module {__class__.__name__} can't read account data, error: {e}"
            self.logger.error(msg)
        return res_accounts

    async def get_stocks_cost_async(self) -> dict:
        """ return sum of all stores without excluded"""
        res_costs = dict({'склад себестоимость': 0})
        try:
            from MoiSkladPackage.MSReports.MSStoresSumAsync import MSStoresSumAsync
            ini_dict = MSStoresSumAsync()
            stores_dict = await ini_dict.get_stores_cost_dict_async()
            excluded_stores_list = list(self._module_config.values())
            for store_name, store_sum in stores_dict.items():
                if store_name not in excluded_stores_list:
                    res_costs['склад себестоимость'] = res_costs.get('склад себестоимость', 0) + int(store_sum)
        except Exception as e:
            msg = f"module {__class__.__name__} can't read stores data, error: {e}"
            self.logger.error(msg)
        return res_costs

    async def get_customers_groups_sum_async(self) -> dict:
        """ return dict of groups with balances {'другие': 710918, 'москваконтрагенты': 450593, 'поставщики': 2984930}"""
        cust_groups = dict({'другие поставщики': 0})
        try:
            from MoiSkladPackage.MSReports.MSCustBalAsync import MSCustBalAsync
            ini_dict = MSCustBalAsync()
            cust_groups = await ini_dict.get_cust_groups_sum_async()
            cust_groups = {key: -value for key, value in cust_groups.items()}
        except Exception as e:
            msg = f"module {__class__.__name__} can't read customers group balances data, error: {e}"
            self.logger.error(msg)
        return cust_groups

    async def form_balance_dict_async(self) -> dict:
        result_dict = dict({"Дата": datetime.now().strftime("%Y.%m.%d %H:%M")})
        balance_sum = int()
        accounts_money_sum = await self.get_accounts_sum_async()
        balance_sum += sum([int(value) for value in accounts_money_sum.values()])
        result_dict.update(accounts_money_sum)
        stocks_sum = await self.get_stocks_cost_async()
        balance_sum += sum([int(value) for value in stocks_sum.values()])
        result_dict.update(stocks_sum)
        cust_groups_bal = await self.get_customers_groups_sum_async()
        balance_sum += sum([int(value) for value in cust_groups_bal.values()])
        result_dict.update(cust_groups_bal)
        result_dict.update({"Итог": balance_sum})
        return result_dict
    async def get_balance_data_async(self) -> dict:
        """ return data in format {"data": {balances_dict}, "col_list": ["data", "summ" ..] }"""
        res_dict = dict({"data": {}, "col_list": [], "info": {}})
        res_dict[self._info_key] = self._module_config.get(self._main_key).get(self._info_key)
        show_col_list = list(self._module_config.get(self._main_key).get(self.result_bal_columns_key))
        data_list = [await self.form_balance_dict_async()]
        # handling empty dict values
        for d in data_list:
            new_dict = dict()
            for col_name in show_col_list:
                value = d.get(col_name, 0)
                new_dict[col_name] = value
                if col_name == 'Итог':
                    res_dict["info"]["total"] = value
            d = new_dict
        res_dict["data"] = data_list
        res_dict["col_list"] = show_col_list
        return res_dict


if __name__ == "__main__":
    start_time = time.time()
    print(f"report starts at {time.strftime('%H:%M:%S', time.localtime())}")
    connect = MSReportBalacesAsync()
    print(asyncio.run(connect.get_balance_data_async()))
    print(f"report done in {int(start_time-time.time())}sec at {time.strftime('%H:%M:%S', time.localtime())}")



