import datetime

from MoiSkladPackage.MSConnectors.MSMainClass import MSMainClass

import time
import asyncio
import datetime
import os


class MSReportProfitAsync(MSMainClass):
    """ gather profit report in one dict"""
    logger_name = f"{os.path.basename(__file__)}"
    _main_key = "ms_profit"
    _info_key = "info"
    _agent_payments_key = "agent_payments"
    _agent_payments_purpose = "Выплаты Агенту"
    _dep_expenses_key = "dep_expences"
    _module_conf_dir = "config"
    _module_conf_file = "ms_profit_config.json"
    _result_bal_columns_key = "result_profit_columns"  # list of result columns
    _module_config = None
    _unknown_dep = "неизвестно"
    _result_profit_columns = "result_profit_columns"

    def __init__(self):
        super().__init__()
        self._module_config = self.get_json_data_sync(self._module_conf_dir, self._module_conf_file)

    async def get_dep_sales_dict_async(self, from_date: str, to_date: str) -> dict:
        """ result returns
        {'Новосибирск': {'Выручка': 15, 'Себестоимость': 783, 'Валовая прибыль': 77},
            'Саратов': {'Выручка': 53, 'Себестоимость': 42, 'Валовая прибыль': 9},
            'Всего': {'Выручка': 23.58, 'Себестоимость': 12.93, 'Валовая прибыль': 19.6}}
        """
        dep_sum_sales = dict()

        try:
            from MoiSkladPackage.MSReports.MSCustDeptAsync import MSCustDeptAsync
            requester1 = MSCustDeptAsync()
            res_cust_dep = await requester1.get_customers_dep_name_dict_async()
            from MoiSkladPackage.MSReports.MSCustSalesProfitAsync import MSCustSalesProfitAsync
            requester2 = MSCustSalesProfitAsync()
            res_cust_sales = await requester2.get_customers_sales_dict_async(from_date=from_date, to_date=to_date)
            summary_sales = 0
            summary_cost = 0
            summary_profit = 0
            for cust_href, cust_data in res_cust_sales.items():
                dep_name = res_cust_dep.get(cust_href, self._unknown_dep)
                sales = cust_data.get('cust_sales')
                cost = cust_data.get('cust_cost')
                profit = cust_data.get('cust_profit')
                summary_sales += sales
                summary_cost += cost
                summary_profit += profit
                if not dep_sum_sales.get(dep_name, None):
                    dep_sales_dict = dict()
                else:
                    dep_sales_dict = dep_sum_sales.get(dep_name)
                dep_sales_dict = {'Выручка': dep_sales_dict.get('Выручка', 0) + sales,
                                  'Себестоимость': dep_sales_dict.get('Себестоимость', 0) + cost,
                                  'Валовая прибыль': dep_sales_dict.get('Валовая прибыль', 0) + profit}
                dep_sum_sales[dep_name] = dep_sales_dict
            dep_sum_sales["Всего"] = dict({'Выручка': summary_sales,
                                           'Себестоимость': summary_cost,
                                           'Валовая прибыль': summary_profit})
        except Exception as e:
            msg = f"module {__class__.__name__} can't read customers department data, error: {e}"
            self.logger.error(msg)
        return dep_sum_sales

    async def get_handled_dep_sales(self, from_date: str, to_date: str):
        """ handler for agent payments result:
        {'Новосибирск': {'Выручка': 15, 'Себестоимость': 781, 'Валовая прибыль': 7, 'Выплаты Агенту': -97},
        'Саратов': {'Выручка': 5, 'Себестоимость': 21, 'Валовая прибыль': 31},
        'Основной': {'Выручка': 30.0, 'Себестоимость': 7.75, 'Валовая прибыль': 2},
        'Москва': {'Выручка': 6, 'Себестоимость': 45, 'Валовая прибыль': 2, 'Выплаты Агенту': -6},
        'Всего': {'Выручка': 23, 'Себестоимость': 12, 'Валовая прибыль': 10, 'Выплаты Агенту': -285}}
        """

        dep_sales = await self.get_dep_sales_dict_async(from_date=from_date, to_date=to_date)
        # get info {'Новосибирск': {'Валовая прибыль': 0.28}, 'Москва': {'Выручка': 0.11}}
        additional_dep_expences = self._module_config.get(self._main_key).get(self._agent_payments_key)

        for department, dep_dict in dep_sales.items():
            agent_payments_dict = additional_dep_expences.get(department, None)
            if agent_payments_dict:
                for key, mult in agent_payments_dict.items():
                    agent_sum = dep_dict.get(key, 0) * mult
                    dep_dict[self._agent_payments_purpose] = dep_dict.get(self._agent_payments_purpose, 0) - agent_sum
                    # dep_sales["Всего"]["Выплаты Агенту"] = dep_sales["Всего"].get("Выплаты Агенту", 0) - agent_sum
        return dep_sales


    async def get_handled_expenses(self, from_date: str, to_date: str, report_type="custom") -> dict:
        result_dict = dict()
        result_dict["info"] = self._module_config.get(self._main_key).get(self._info_key)
        data_list = list()
        show_only_res_cols = list(["date_from", "date_to", "report_type"])
        try:
            from MoiSkladPackage.MSReports.MSPaymentsAsync import MSPaymentsAsync
            requester3 = MSPaymentsAsync()
            general_expenses = await requester3.get_purpose_sum_dict_async(from_date=from_date, to_date=to_date, report_type=report_type)
            handled_dep_sales = await self.get_handled_dep_sales(from_date=from_date, to_date=to_date)
            # get info {"Новосибирск": {"Новосибирск склад": 1},"Москва": {"Москва склад": 1,"Аренда": 1}}
            additional_dep_expenses = self._module_config.get(self._main_key).get(self._dep_expenses_key)
            for dep_name, dep_dict in additional_dep_expenses.items():
                temp_dict = handled_dep_sales.get(dep_name, dict())
                for exp_key, exp_mult in dep_dict.items():
                    dep_exp_sum = general_expenses["data"].get(exp_key, 0) * exp_mult
                    temp_dict[exp_key] = temp_dict.get(exp_key, 0) + dep_exp_sum
                handled_dep_sales[dep_name] = temp_dict


            """ handled_dep_sales like 
            {'Новосибирск': {'Выручка': 17, 'Себестоимость': 71, 'Валовая прибыль': 8, 'Выплаты Агенту': -2, 'Новосибирск склад': -2}, 
            'Саратов': {'Выручка': 5, 'Себестоимость': 2, 'Валовая прибыль': 1, 'Выплаты Агенту': 0.0}, 
            'Основной': {'Выручка': 30, 'Себестоимость': 7, 'Валовая прибыль': 2}, 
            'Москва': {'Выручка': 6, 'Себестоимость': 4, 'Валовая прибыль': 2, 'Москва склад': -6, 'Аренда': -4}, 
            'Всего': {'Выручка': 22, 'Себестоимость': 3, 'Валовая прибыль': 1, 'Выплаты Агенту': -2}}
"""
            # change "Выплаты Агенту" from dep to 'Всего'
            # general_expenses["data"][self._agent_payments_purpose] = handled_dep_sales['Всего'].get(self._agent_payments_purpose,0)
            handled_dep_sales['Всего'].update(general_expenses.get('data'))
            show_only_res_cols = self._module_config.get(self._main_key).get(self._result_profit_columns)
            # exclude not showed columns
            for dep_name, dep_dict in handled_dep_sales.items():
                temp_dict = dict()
                for expenses_key in show_only_res_cols:
                    temp_dict[expenses_key] = handled_dep_sales[dep_name].get(expenses_key, 0)
                handled_dep_sales[dep_name] = temp_dict

            # count summary in each department
            for dep_name, dep_dict in handled_dep_sales.items():
                summary = 0
                for exp, exp_sum in dep_dict.items():
                    if exp not in ['Выручка', 'Себестоимость']:
                        summary += exp_sum
                dep_dict['Чистая прибыль'] = summary
                if dep_name == "Всего":
                    result_dict["info"]["total"] = summary
                dep_dict['Отдел'] = dep_name
                dep_dict.update(general_expenses.get('date'))
                data_list.append(dep_dict)

        except Exception as e:
            msg = f"module {__class__.__name__} can't handle expenses data, error: {e}"
            self.logger.error(msg)
        result_dict["data"] = data_list
        result_dict["col_list"] = show_only_res_cols

        return result_dict

    async def get_daily_profit_report_async(self) -> dict:
        """report to current day from 1 day of this month"""
        cur_month = datetime.datetime.now().month
        cur_year = datetime.datetime.now().year
        from_date = f"{cur_year}-{cur_month}-01"
        to_date = str(datetime.datetime.now().strftime("%Y-%m-%d"))
        report_type = "daily"
        result = await self.get_handled_expenses(from_date, to_date, report_type)
        return result

    async def get_monthly_profit_report_async(self, to_month: int, to_year: int) -> dict:
        """report to current day from 1 day of this month"""
        import calendar
        month_first_day_datetime = datetime.datetime.strptime(f"{to_year}-{to_month}-01", "%Y-%m-%d")
        month_last_day = calendar.monthrange(to_year, to_month)[1]
        month_last_day_datetime = datetime.datetime.strptime(
            f"{to_year}-{to_month}-{month_last_day}", "%Y-%m-%d")
        from_date = month_first_day_datetime.strftime("%Y-%m-%d")
        to_date = month_last_day_datetime.strftime("%Y-%m-%d")
        report_type = "monthly"
        result = await self.get_handled_expenses(from_date, to_date, report_type)
        return result



if __name__ == "__main__":
    start_time = time.time()
    print(f"report starts at {time.strftime('%H:%M:%S', time.localtime())}")
    connect = MSReportProfitAsync()
    # print(asyncio.run(connect.get_dep_sales_dict_async(from_date="2024-01-01", to_date="2024-01-31")))
    # print(asyncio.run(connect.get_outpayments_dict_async(from_date="2024-01-01", to_date="2024-01-31")))
    # print(asyncio.run(connect.get_handled_dep_sales(from_date="2024-01-01", to_date="2024-01-31")))
    # print(asyncio.run(connect.get_handled_expenses(from_date="2024-01-01", to_date="2024-01-31")))
    # print(asyncio.run(connect.get_daily_profit_report_async()))
    print(asyncio.run(connect.get_monthly_profit_report_async(to_year=2024, to_month=3)))
    print(f"report done in {int(time.time() - start_time)}sec at {time.strftime('%H:%M:%S', time.localtime())}")
