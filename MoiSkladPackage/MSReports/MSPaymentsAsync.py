import asyncio
import os
from MoiSkladPackage.MSConnectors.MSMainClass import MSMainClass
import datetime

class MSPaymentsAsync(MSMainClass):
    """return out_payments in period by purpose"""
    logger_name = f"{os.path.basename(__file__)}"
    _url_outpayments_list = "url_outpayments_list"
    _url_expence_items_list = "url_expence_items_list"
    # _config_dir = "config"
    # _config_file_name = "ms_balances_config.json"
    # _config_data = None
    _module_conf_dir = "config"
    _module_conf_file = "ms_profit_config.json"
    _to_file = False
    _unknown_purpose = "неизвестно"  # для неопределенных платежей
    async_requester = None

    def __init__(self, to_file=False):
        super().__init__()
        if to_file:
            self.to_file = to_file
        from MoiSkladPackage.MSConnectors.MSRequesterAsync import  MSRequesterAsync
        self.async_requester = MSRequesterAsync()

    async def get_purposes_dict_async(self, to_file=False) -> dict:
        """ purposes dict {purpose_href: purpose_name}"""
        if to_file:
            self._to_file = to_file
        purposes_dict = dict()
        try:
            purposes_json = await self.async_requester.get_api_data_async(url_conf_key=self._url_expence_items_list, to_file=self._to_file)
            for purpose in purposes_json['rows']:
                purpose_href = purpose['meta']['href']
                purpose_name = purpose['name']
                purposes_dict[purpose_href] = purpose_name
        except Exception as e:
            msg = f"module {__class__.__name__} can't read expenses items data, error: {e}"
            self.logger.error(msg)
        return purposes_dict

    async def get_payments_purpose_dict_async(self, from_date: str, to_date: str, report_type: str, to_file=False) -> dict:
        """ return dict
        {'date': {'date_from': '2024-01-01', 'date_to': '2024-02-13', 'report_type': 'daily'},
        'data':{purpose_name: payments_sum}}"""
        if to_file:
            self._to_file = to_file
        if not from_date:
            from_date = '2024-01-01'
        if not to_date:
            to_date = str(datetime.datetime.now().strftime("%Y-%m-%d"))
        request_param_line = f"filter=moment>={from_date} 00:00:00&filter=moment<={to_date} 23:59:00"
        date_dict = dict({"date_from": from_date, "date_to": to_date, "report_type": report_type})
        payments_purpose_dict = dict()
        try:
            self.async_requester.set_api_param_line(request_param_line)
            out_payments_json = await self.async_requester.get_api_data_async(url_conf_key=self._url_outpayments_list, to_file=self._to_file)
            for payment in out_payments_json['rows']:
                purpose_href = payment['expenseItem']['meta']['href']
                payment_sum = payment['sum']/100
                payments_purpose_dict[purpose_href] = payments_purpose_dict.get(purpose_href, 0) + payment_sum
        except Exception as e:
            msg = f"module {__class__.__name__} can't read customers_list data, error: {e}"
            self.logger.error(msg)
        return dict({"date": date_dict, "data": payments_purpose_dict})

    async def get_purpose_sum_dict_async(self, from_date: str, to_date: str, report_type, to_file=False) -> dict:
        """ report returns
        {'date': {'date_from': '2024-01-01', 'date_to': '2024-02-13', 'report_type': 'daily'},
        'data': {'Зарплата': -215585.2, 'Перемещение': -1512690.0}} """
        if to_file:
            self._to_file = to_file
        purpose_sum_dict = dict()
        purpose_date_dict = dict()
        try:
            purposes_dict = await self.get_purposes_dict_async()
            purpose_payments_dict = await self.get_payments_purpose_dict_async(from_date=from_date, to_date=to_date, to_file=to_file, report_type=report_type)
            purpose_date_dict = dict({"date": purpose_payments_dict.get("date")})
            purpose_date_dict["date"]["report_type"] = report_type
            purpose_payments_sum_dict = purpose_payments_dict.get("data")
            purpose_sum_dict = {purposes_dict.get(href, self._unknown_purpose): -summ for href, summ in purpose_payments_sum_dict.items()}
        except Exception as e:
            msg = f"module {__class__.__name__} can't read departments_list data, error: {e}"
            self.logger.error(msg)
        purpose_date_dict.update({"data": purpose_sum_dict})
        return purpose_date_dict

    async def get_current_month_purpose_sum_dict_async(self, to_file=False) -> dict:
        cur_month = datetime.datetime.now().month
        cur_year = datetime.datetime.now().year
        from_date = f"{cur_year}-{cur_month}-01"
        to_date = str(datetime.datetime.now().strftime("%Y-%m-%d"))
        purpose_payments_dict = await self.get_purpose_sum_dict_async(from_date=from_date, to_date=to_date, to_file=to_file)
        purpose_date_dict = dict({"date": purpose_payments_dict.get("date")})
        purpose_date_dict["date"]["report_type"] = "daily"
        purpose_date_dict.update({"data": purpose_payments_dict.get("data")})
        return purpose_date_dict

    async def get_last_month_purpose_sum_dict_async(self, to_file=False) -> dict:
        payouts_last_month_profit = dict()

        try:
            cur_month = datetime.datetime.now().month
            cur_year = datetime.datetime.now().year
            cur_month_first_day = datetime.datetime.strptime(f"{cur_year}-{cur_month}-01", "%Y-%m-%d")
            last_month_last_day = cur_month_first_day - datetime.timedelta(days=1)
            last_month_first_day = datetime.datetime.strptime(
                f"{last_month_last_day.year}-{last_month_last_day.month}-01", "%Y-%m-%d")
            from_date = last_month_first_day.strftime("%Y-%m-%d")
            to_date = last_month_last_day.strftime("%Y-%m-%d")
            payouts_last_month_profit = await self.get_purpose_sum_dict_async(from_date, to_date, to_file)
            payouts_last_month_profit["date"]["report_type"] = "month"
        except Exception as e:
            msg = f"module {__class__.__name__} can't read purposes sum data, error: {e}"
            self.logger.error(msg)
        return payouts_last_month_profit

    async def get_month_purpose_sum_dict_async(self, to_month: int, to_year: int, to_file=False) -> dict:
        payouts_month_profit = dict()

        try:
            import calendar
            month_first_day_datetime = datetime.datetime.strptime(f"{to_year}-{to_month}-01", "%Y-%m-%d")
            month_last_day = calendar.monthrange(to_year, to_month)[1]
            month_last_day_datetime = datetime.datetime.strptime(
                f"{to_year}-{to_month}-{month_last_day}", "%Y-%m-%d")
            from_date = month_first_day_datetime.strftime("%Y-%m-%d")
            to_date = month_last_day_datetime.strftime("%Y-%m-%d")
            payouts_month_profit = await self.get_purpose_sum_dict_async(from_date, to_date, to_file)
            payouts_month_profit["date"]["report_type"] = "month"
        except Exception as e:
            msg = f"module {__class__.__name__} can't read purposes sum data, error: {e}"
            self.logger.error(msg)
        return payouts_month_profit

if __name__ == "__main__":
    connect = MSPaymentsAsync()
    # print(asyncio.run(connect.get_purposes_dict_async()))
    # print(asyncio.run(connect.get_payments_purpose_dict_async()))
    # print(asyncio.run(connect.get_purpose_sum_dict_async()))
    # print(asyncio.run(connect.get_current_month_purpose_sum_dict_async()))
    # print(asyncio.run(connect.get_last_month_purpose_sum_dict_async()))
    print(asyncio.run(connect.get_month_purpose_sum_dict_async(to_month=12, to_year=2023)))
    connect.logger.debug("stock_all class initialized")
