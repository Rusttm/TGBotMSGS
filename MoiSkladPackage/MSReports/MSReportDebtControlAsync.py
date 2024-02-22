import datetime
from MoiSkladPackage.MSConnectors.MSMainClass import MSMainClass
import time
import asyncio
import datetime
import os


class MSReportDebtControlAsync(MSMainClass):
    """ count sum of cust balances """
    logger_name = f"{os.path.basename(__file__)}"
    _main_key = "ms_debt"
    _info_key = "info"
    _group_columns_key = "group_columns"
    _include_other_companies_key = "include_other_companies"
    _other_companies_group_name = "другие клиенты"
    _module_conf_dir = "config"
    _module_conf_file = "ms_debt_control_config.json"
    _module_config: dict = None

    def __init__(self):
        super().__init__()
        self._module_config = self.set_module_config_sync(self._module_conf_dir, self._module_conf_file)

    async def get_customers_debt_sum_async(self) -> dict:
        """ sum only negative!!! (debt) balances in client group
        return dict of groups with balances {'другие': 710918, 'москваконтрагенты': 450593, 'поставщики': 2984930}"""
        res_debt = dict({'data': [], 'col_list': [], 'info': {'total': 0}})
        cust_groups = dict()
        try:
            from MoiSkladPackage.MSReports.MSCustBalAsync import MSCustBalAsync
            requester = MSCustBalAsync()
            # {customer_href: customer_group_list}
            customers_groups = await requester.get_customers_dict_async()
            # {customer_href: [customer_bal, customer_name]}
            customers_bal = await requester.get_customers_bal_async(balance_filter="balance<0")
            # ["поставщики", "новосибирскконтрагенты", "москваконтрагенты", "покупатели пфо", "другие клиенты"]
            customers_show_groups = list(self._module_config[self._main_key][self._group_columns_key])
            other_customers = list(self._module_config[self._main_key][self._include_other_companies_key])
            res_debt[self._info_key] = self._module_config[self._main_key][self._info_key]
            total_sum = 0
            for cust_href, cust_list in customers_bal.items():
                cust_sum = cust_list[0]
                cust_name = cust_list[1]
                cust_groups_names_list = customers_groups.get(cust_href)
                for main_group in customers_show_groups:
                    if main_group in cust_groups_names_list:
                        cust_groups[main_group] = cust_groups.get(main_group, 0) + cust_sum
                        total_sum += cust_sum
                        break
                    if cust_name in other_customers:
                        cust_groups[self._other_companies_group_name] = cust_groups.get(self._other_companies_group_name, 0) + int(cust_sum)
                        total_sum += cust_sum
                        break
            res_debt["col_list"] = customers_show_groups
            cust_groups["итого"] = total_sum
            # handle groups
            for group in customers_show_groups:
                cust_groups[group] = cust_groups.get(group, 0)
            res_debt["data"] = [cust_groups]
            res_debt["info"]["total"] = total_sum

        except Exception as e:
            msg = f"module {__class__.__name__} can't read customers group balances data, error: {e}"
            self.logger.error(msg)
        return res_debt



if __name__ == "__main__":
    start_time = time.time()
    print(f"report starts at {time.strftime('%H:%M:%S', time.localtime())}")
    connect = MSReportDebtControlAsync()
    print(asyncio.run(connect.get_customers_debt_sum_async()))
    print(f"report done in {int(start_time-time.time())}sec at {time.strftime('%H:%M:%S', time.localtime())}")



