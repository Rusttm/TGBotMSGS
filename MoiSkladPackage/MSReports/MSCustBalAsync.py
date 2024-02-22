import asyncio
import os
from MoiSkladPackage.MSConnectors.MSMainClass import MSMainClass


class MSCustBalAsync(MSMainClass):
    """ clas get sum of stores"""
    logger_name = f"{os.path.basename(__file__)}"
    url_customers_bal = "url_customers_bal"
    url_customers_list = "url_customers_list"

    _main_key = "ms_balance"
    other_companies_group_name = "другие поставщики"
    customers_columns_key = "customers_bal_columns"
    excluded_groups_key = "excluded_groups"
    include_other_companies_key = "include_other_companies"
    _dir_name = "config"
    _config_file_name = "ms_balances_config.json"
    config_data = None
    async_requester = None
    to_file = False

    def __init__(self, to_file=False):
        super().__init__()
        if to_file:
            self.to_file = to_file
        from MoiSkladPackage.MSConnectors.MSRequesterAsync import MSRequesterAsync
        self.async_requester = MSRequesterAsync()

    async def get_customers_dict_async(self):
        """ return customers dict {customer_href: customer_groups_list}"""
        customers_dict = dict()
        try:
            customers_json = await self.async_requester.get_api_data_async(url_conf_key=self.url_customers_list, to_file=self.to_file)
            for customer in customers_json['rows']:
                # customer_name = customer['name']
                customer_href = customer['meta']['href']
                customer_groups_list = customer['tags']
                customers_dict[customer_href] = customer_groups_list
        except Exception as e:
            msg = f"module {__class__.__name__} can't read customers_list data, error: {e}"
            self.logger.error(msg)
        return customers_dict

    async def get_customers_bal_async(self, balance_filter="balance!=0") -> dict:
        """returns dict {customer_href: [customer_balance, customer_name]}"""
        customers_bal = dict()
        try:
            self.async_requester.set_api_param_line(f'filter={balance_filter}')
            cust_bal_dict = await self.async_requester.get_api_data_async(url_conf_key=self.url_customers_bal, to_file=self.to_file)
            for customer in cust_bal_dict['rows']:
                customer_name = customer['counterparty']['name']
                customer_bal = customer['balance'] / 100
                customer_href = customer['counterparty']['meta']['href']
                customers_bal[customer_href] = [customer_bal, customer_name]
        except Exception as e:
            msg = f"module {__class__.__name__} can't read stock_all data, error: {e}"
            self.logger.error(msg)
        return customers_bal

    async def get_cust_groups_sum_async(self) -> dict:
        """ returns {customers_group: summ_balance}"""
        cust_groups_sum = dict()
        try:
            # self.config_data = await self.load_conf_data()
            # print(f"{self.config_data=}")
            # {customer_href: customer_group_list}
            customers_groups = await self.get_customers_dict_async()
            # {customer_href: [customer_bal, customer_name]}
            customers_bal = await self.get_customers_bal_async()
            # ["поставщики", "новосибирскконтрагенты", "москваконтрагенты", "покупатели пфо", "другие"]
            customers_show_groups = list(self._module_config[self._main_key][self.customers_columns_key])
            # ["ПАО \"ТРАНСКОНТЕЙНЕР\"","ФТС России","ООО \"ТРАСКО\"", "ООО \"МЕДИТЕРРАНЕАН ШИППИНГ КОМПАНИ РУСЬ\""],
            other_customers = list(self._module_config[self._main_key][self.include_other_companies_key])
            for customer_href in customers_bal:
                customer_in_groups = customers_groups.get(customer_href, None)
                # get bal sum
                customer_bal = customers_bal.get(customer_href)[0]
                # get name
                customer_name = customers_bal.get(customer_href)[1]
                if customer_in_groups:
                    for show_group in customers_show_groups:
                        customer_groups = customers_groups.get(customer_href, None)
                        if show_group in customer_groups:
                            cust_groups_sum[show_group] = cust_groups_sum.get(show_group, 0) + int(customer_bal)
                            break
                        elif customer_name in other_customers:
                            cust_groups_sum[self.other_companies_group_name] = cust_groups_sum.get(self.other_companies_group_name, 0) + int(customer_bal)
                            break

        except Exception as e:
            msg = f"module {__class__.__name__} can't make cust_groups_sum data, error: {e}"
            self.logger.error(msg)
        return cust_groups_sum


if __name__ == "__main__":
    connect = MSCustBalAsync()
    # print(connect.get_stores_good_price())
    # print(connect.get_stores_dict())
    # print(asyncio.run(connect.get_customers_dict_async()))
    # print(asyncio.run(connect.get_customers_bal_async()))
    print(asyncio.run(connect.get_cust_groups_sum_async()))
    connect.logger.debug("stock_all class initialized")
