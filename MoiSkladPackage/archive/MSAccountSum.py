from MSMainClass import MSMainClass
import os

class MSAccountSum(MSMainClass):
    """ clas get accounts remains"""
    logger_name = f"{os.path.basename(__file__)}"
    url_key = "url_money"
    save_2file = False

    def __init__(self):
        super().__init__()

    def get_account_summ(self) -> int:
        """this function gets sum of bank accounts remains"""
        account_bal = int()
        # get account sum
        try:
            import MSRequester
            requester = MSRequester.MSRequester()
            requester.set_config(self.url_key)
            acc_req = requester.get_api_data(to_file=self.save_2file)
            account_bal = int()
            for account in acc_req['rows'][1:]:
                account_bal += int(account['balance']/100)
        except Exception as e:
            msg = f"module {__class__.__name__} can't read account data, error: {e}"
            self.logger.error(msg)
        return account_bal

    def get_account_remains(self) -> dict:
        """this function gets sum of bank accounts remains"""
        accounts_bal = dict({'accounts_sum': 0, 'accounts': dict()})
        # get account sum
        try:
            import MSRequester
            requester = MSRequester.MSRequester()
            requester.set_config(self.url_key)
            acc_req = requester.get_api_data(to_file=self.save_2file)
            new_dict = dict()
            accounts_sum = int()
            for account_elem in acc_req['rows'][1:]:
                account_num = account_elem['account']['name']
                account_sum = account_elem['balance']/100
                new_dict[account_num] = int(account_sum)
                accounts_sum += int(account_sum)
            accounts_bal['accounts'] = dict(sorted(new_dict.items(), key=lambda x: x[1], reverse=True))
            accounts_bal['accounts_sum'] = accounts_sum
        except Exception as e:
            msg = f"module {__class__.__name__} can't read account data, error: {e}"
            self.logger.error(msg)
        return accounts_bal


if __name__ == "__main__":
    connect = MSAccountSum()
    print(connect.get_account_summ())
    print(connect.get_account_remains())
    connect.logger.debug("accounting class initialized")
