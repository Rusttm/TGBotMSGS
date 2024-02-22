from MoiSkladPackage.MSConnectors.MSMainClass import MSMainClass
import asyncio
import os
class MSAccountSumAsync(MSMainClass):
    """ clas get accounts remains"""
    logger_name = f"{os.path.basename(__file__)}"
    url_key = "url_money"
    save_2file = False
    async_requester = None
    _main_key = "ms_accounts"
    _info_key = "info"
    _accounts_columns_key = "accounts_list"
    _module_conf_dir = "config"
    _module_conf_file = "ms_accounts_config.json"
    _module_config: dict = None

    def __init__(self):
        super().__init__()
        from MoiSkladPackage.MSConnectors.MSRequesterAsync import MSRequesterAsync
        self.async_requester = MSRequesterAsync()
        self._module_config = self.set_module_config_sync(self._module_conf_dir, self._module_conf_file)

    async def get_account_summ_async(self) -> int:
        """this function gets sum of bank accounts remains"""
        account_bal = int()
        # get account sum
        try:
            acc_req = await self.async_requester.get_api_data_async(url_conf_key=self.url_key, to_file=self.save_2file)
            account_bal = int()
            for account in acc_req['rows'][1:]:
                account_bal += int(account['balance']/100)
        except Exception as e:
            msg = f"module {__class__.__name__} can't read account data, error: {e}"
            self.logger.error(msg)
        return account_bal

    async def get_account_remains_async(self) -> dict:
        """this function gets sum of bank accounts remains"""
        res_accounts = dict({'data': ['итого'], 'col_list': [], 'info': {'total': 0}})
        res_accounts[self._info_key] = self._module_config.get(self._main_key).get(self._info_key)
        accounts_cols_list = self._module_config.get(self._main_key).get(self._accounts_columns_key)

        # get account sum
        try:
            acc_req = await self.async_requester.get_api_data_async(url_conf_key=self.url_key, to_file=self.save_2file)
            new_dict = dict()
            accounts_sum = int()
            accounts_list = list()
            for account_elem in acc_req['rows'][1:]:
                account_num = account_elem['account']['name']
                accounts_list.append(account_num)
                account_sum = account_elem['balance']/100
                new_dict[account_num] = int(account_sum)
                accounts_sum += int(account_sum)
            new_dict['итого'] = accounts_sum
            # accounts_bal['accounts'] = dict(sorted(new_dict.items(), key=lambda x: x[1], reverse=True))
            # accounts_bal['accounts_sum'] = accounts_sum

            # handle colums and names list
            gathered_accounts = list(set(accounts_list + accounts_cols_list))
            for account in gathered_accounts:
                if account not in accounts_cols_list:
                    msg = f" attention!!! account {account} is not in config list {self._module_conf_file}, please declare it!"
                    print(msg)
                    self.logger.warning(msg)
            res_accounts["col_list"] = accounts_cols_list
            for account in accounts_cols_list:
                new_dict[account] = new_dict.get(account, 0)
            res_accounts["data"] = [new_dict]

            res_accounts["info"]["total"] = accounts_sum

        except Exception as e:
            msg = f"module {__class__.__name__} can't read account data, error: {e}"
            self.logger.error(msg)
        return res_accounts

    def get_account_remains_sync(self) -> dict:
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(self.get_account_remains_async())
        # result = asyncio.run(self.get_config_json_data_async(file_name=file_name))
        return result


if __name__ == "__main__":
    connect = MSAccountSumAsync()
    # print(asyncio.run(connect.get_account_summ_async()))
    print(asyncio.run(connect.get_account_remains_async()))
    connect.logger.debug("accounting class initialized")

