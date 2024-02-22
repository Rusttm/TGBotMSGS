import datetime
from MoiSkladPackage.MSConnectors.MSMainClass import MSMainClass
import time
import asyncio
import datetime
import os


class MSReportLowMarginAsync(MSMainClass):
    """ list of low margin sales"""
    logger_name = f"{os.path.basename(__file__)}"
    _main_key = "ms_sales"
    _info_key = "info"
    _profit_margin_key = "profit_margin"
    _module_conf_dir = "config"
    _module_conf_file = "ms_sales_config.json"
    _module_config: dict = None

    def __init__(self):
        super().__init__()
        self._module_config = self.set_module_config_sync(self._module_conf_dir, self._module_conf_file)

    async def get_low_margin_cust_list_async(self, from_date, to_date) -> dict:
        """ return dict low margin clients"""
        res_margins = dict({'data': [], 'col_list': ['name', 'sale', 'profitability'], 'info': {'total': 0}})
        profit_margin = self._module_config.get(self._main_key).get(self._profit_margin_key)
        res_margins["info"] = self._module_config.get(self._main_key).get(self._info_key)
        try:
            from MoiSkladPackage.MSReports.MSCustSalesProfitAsync import MSCustSalesProfitAsync
            requester = MSCustSalesProfitAsync()
            req_data = await requester.get_customers_sales_dict_async(from_date=from_date, to_date=to_date)
            counter = 0
            names_list = []

            for cust_href, cust_dict in req_data.items():
                name_dict = dict()
                profit = cust_dict.get('cust_profit', 0)
                sales = cust_dict.get('cust_sales', 0)
                name = cust_dict.get('cust_name', 'unknown')
                if sales > 0:
                    profitability = int(round(profit/sales, 2)*100)
                    if profitability < profit_margin:
                        name_dict['name'] = name
                        name_dict['profitability'] = profitability
                        name_dict['sale'] = sales
                        counter += 1
                        names_list.append(name_dict)
            res_margins["data"] = names_list
            res_margins["info"]["total"] = counter
            res_margins["info"]["margin"] = profit_margin

        except Exception as e:
            msg = f"module {__class__.__name__} can't read sales data, error: {e}"
            self.logger.error(msg)
        return res_margins

    async def get_today_low_margin_clients_async(self) -> dict:
        # res_margins = dict({'data': [], 'col_list': ['name', 'profitability'], 'info': {'total': 0}})
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        req_data = await self.get_low_margin_cust_list_async(from_date=today, to_date=today)
        return req_data



if __name__ == "__main__":
    start_time = time.time()
    print(f"report starts at {time.strftime('%H:%M:%S', time.localtime())}")
    connect = MSReportLowMarginAsync()
    print(asyncio.run(connect.get_low_margin_cust_list_async(from_date="2023-01-9", to_date="2023-01-9")))
    # print(asyncio.run(connect.get_today_low_margin_clients_async()))
    print(f"report done in {int(start_time-time.time())}sec at {time.strftime('%H:%M:%S', time.localtime())}")



