import asyncio
import os

from MoiSkladPackage.MSConnectors.MSMainClass import MSMainClass


class MSProdAsync(MSMainClass):
    """ clas get products list"""
    logger_name = f"{os.path.basename(__file__)}"
    _url_prod_list = 'url_prod_list'
    async_requester = None
    to_file = False
    _module_conf_dir = "config"
    _module_conf_file = "ms_balances_config.json"


    def __init__(self, to_file=False):
        super().__init__()
        if to_file:
            self.to_file = to_file
        self._module_config = self.set_module_config_sync(self._module_conf_dir, self._module_conf_file)
        from MoiSkladPackage.MSConnectors.MSRequesterAsync import MSRequesterAsync
        self.async_requester = MSRequesterAsync()


    async def get_prod_list_async(self) -> dict:
        """this return dict {"position_href": cost}"""
        prod_list = dict()
        try:
            req = await self.async_requester.get_api_data_async(url_conf_key=self._url_prod_list, to_file=self.to_file)
            prod_list = req.get('rows')
        except Exception as e:
            msg = f"module {__class__.__name__} can't read stock_all data, error: {e}"
            self.logger.error(msg)
        return prod_list

    async def get_first_prod_async(self) -> dict:
        prod = dict()
        prod = await self.get_prod_list_async()
        return prod[0]
if __name__ == "__main__":
    connect = MSProdAsync()
    # print(connect.get_stores_good_price())
    # print(connect.get_stores_dict())
    print(asyncio.run(connect.get_first_prod_async()))
    connect.logger.debug("stock_all class initialized")
