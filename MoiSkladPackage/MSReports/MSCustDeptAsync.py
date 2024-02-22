import asyncio
import os
from MoiSkladPackage.MSConnectors.MSMainClass import MSMainClass


class MSCustDeptAsync(MSMainClass):
    """gather customers departments dict"""
    logger_name = f"{os.path.basename(__file__)}"
    _url_departments_list = "url_departments_list"
    _url_customers_list = "url_customers_list"
    _config_file_name = "ms_balances_config.json"
    _config_data = None
    _to_file = False
    _unknown_dep = "неизвестно"  # отдел для неопределенных клиентов
    async_requester = None


    def __init__(self, to_file=False):
        super().__init__()
        if to_file:
            self.to_file = to_file
        from MoiSkladPackage.MSConnectors import MSRequesterAsync
        self.async_requester = MSRequesterAsync.MSRequesterAsync()


    async def get_customers_dep_dict_async(self, to_file=False) -> dict:
        """ return dict {cust_href: department_href}"""
        if to_file:
            self._to_file = to_file
        customers_dict = dict()
        try:
            customers_json = await self.async_requester.get_api_data_async(url_conf_key=self._url_customers_list, to_file=self._to_file)
            for customer in customers_json['rows']:
                # customer_name = customer['name']
                customer_href = customer['meta']['href']
                # customer_groups_list = customer['tags']
                customer_department_href = customer['group']['meta']['href']
                # customers_dict[customer_href] = customer_groups_list
                customers_dict[customer_href] = customer_department_href
        except Exception as e:
            msg = f"module {__class__.__name__} can't read customers_list data, error: {e}"
            self.logger.error(msg)
        return customers_dict

    async def get_departments_name_dict_async(self, to_file=False) -> dict:
        """ returns dict {department_href: department_name}"""
        if to_file:
            self._to_file = to_file
        departments_dict = dict()
        try:
            departments_json = await self.async_requester.get_api_data_async(url_conf_key=self._url_departments_list, to_file=self._to_file)
            for dep in departments_json['rows']:
                dep_href = dep['meta']['href']
                department_name = dep['name']
                departments_dict[dep_href] = department_name
        except Exception as e:
            msg = f"module {__class__.__name__} can't read departments_list data, error: {e}"
            self.logger.error(msg)
        return departments_dict

    async def get_customers_dep_name_dict_async(self) -> dict:
        """this return dict {cust_href: department_name}}"""
        customers_dep_name = dict()
        try:
            customers_dep_dict = await self.get_customers_dep_dict_async()
            departments_name_dict = await self.get_departments_name_dict_async()
            customers_dep_name = {key: departments_name_dict.get(value, self._unknown_dep) for key, value in customers_dep_dict.items()}
        except Exception as e:
            msg = f"module {__class__.__name__} can't gather dict(customer: dep_name), error: {e}"
            self.logger.error(msg)
        return customers_dep_name


if __name__ == "__main__":
    connect = MSCustDeptAsync()
    # print(asyncio.run(connect.get_customers_dep_dict_async()))
    # print(asyncio.run(connect.get_departments_name_dict_async()))
    print(asyncio.run(connect.get_customers_dep_name_dict_async()))
    connect.logger.debug("stock_all class initialized")
