import asyncio
import os
import datetime

from MoiSkladPackage.MSConnectors.MSMainClass import MSMainClass


class MSCustSalesProfitAsync(MSMainClass):
    """gather customers profit dict filtered in month"""
    logger_name = f"{os.path.basename(__file__)}"
    _url_profit_by_cust_list = "url_profit_by_cust_list"
    _module_conf_file = "ms_main_config.json"
    _module_conf_dir = "config"
    _to_file = False
    async_requester = None
    _module_config = None

    def __init__(self, to_file=False):
        super().__init__()
        if to_file:
            self.to_file = to_file
        from MoiSkladPackage.MSConnectors.MSRequesterAsync import MSRequesterAsync
        self.async_requester = MSRequesterAsync()
        self._module_config = self.async_requester.set_module_config_sync(self._module_conf_dir, self._module_conf_file)

    async def get_customers_sales_dict_async(self, from_date, to_date, to_file=False) -> dict:
        """ return dict {{cust_href: [cust_name, cust_sales, cust_cost, cust_profit]}}"""
        if to_file:
            self._to_file = to_file
        if not from_date:
            from_date = '2023-12-31'
        if not to_date:
            to_date = str(datetime.datetime.now().strftime("%Y-%m-%d"))

        customers_sales_dict = dict()
        request_param_line = f"momentFrom={from_date} 00:00:00&momentTo={to_date} 23:59:00"
        self.async_requester.set_api_param_line(request_param_line)
        try:
            customers_sales_json = await self.async_requester.get_api_data_async(
                url_conf_key=self._url_profit_by_cust_list, to_file=self._to_file)
            for customer in customers_sales_json['rows']:
                customer_href = customer['counterparty']['meta']['href']
                customer_name = customer['counterparty']['name']
                customer_sales = customer['sellSum'] / 100
                customer_cost = customer['sellCostSum'] / 100
                customer_profit = customer['profit'] / 100
                customers_sales_dict[customer_href] = dict({"cust_name": customer_name,
                                                            "cust_sales": customer_sales,
                                                            "cust_cost": customer_cost,
                                                            "cust_profit": customer_profit})
        except Exception as e:
            msg = f"module {__class__.__name__} can't read profit by customers data, error: {e}"
            self.logger.error(msg)
        return customers_sales_dict

    async def get_current_month_customers_sales_dict_async(self) -> dict:
        cur_month = datetime.datetime.now().month
        cur_year = datetime.datetime.now().year
        from_date = f"{cur_year}-{cur_month}-01"
        to_date = str(datetime.datetime.now().strftime("%Y-%m-%d"))
        customers_current_month_profit = await self.get_customers_sales_dict_async(from_date, to_date)
        return customers_current_month_profit

    async def get_last_month_customers_sales_dict_async(self) -> dict:
        customers_last_month_profit = dict()
        try:
            cur_month = datetime.datetime.now().month
            cur_year = datetime.datetime.now().year
            cur_month_first_day = datetime.datetime.strptime(f"{cur_year}-{cur_month}-01", "%Y-%m-%d")
            last_month_last_day = cur_month_first_day - datetime.timedelta(days=1)
            last_month_first_day = datetime.datetime.strptime(
                f"{last_month_last_day.year}-{last_month_last_day.month}-01", "%Y-%m-%d")
            from_date = last_month_first_day.strftime("%Y-%m-%d")
            to_date = last_month_last_day.strftime("%Y-%m-%d")
            customers_last_month_profit = await self.get_customers_sales_dict_async(from_date, to_date)
        except Exception as e:
            msg = f"module {__class__.__name__} can't read profit by customers data, error: {e}"
            self.logger.error(msg)
        return customers_last_month_profit


if __name__ == "__main__":
    connect = MSCustSalesProfitAsync()
    print(asyncio.run(connect.get_customers_sales_dict_async("2023-12-01", "2023-12-31")))
    # print(asyncio.run(connect.get_current_month_customers_sales_dict_async()))
    # print(asyncio.run(connect.get_last_month_customers_sales_dict_async()))
    connect.logger.debug("stock_all class initialized")
