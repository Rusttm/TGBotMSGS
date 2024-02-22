import asyncio
import os

from MoiSkladPackage.MSConnectors.MSMainClass import MSMainClass


class MSStoresSumAsync(MSMainClass):
    """ clas get sum of stores"""
    logger_name = f"{os.path.basename(__file__)}"
    url_stock_all = "url_stock_all"
    url_stores = "url_stores"
    url_stock_stores = "url_stock_stores"
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


    async def get_goods_cost_async(self) -> dict:
        """this return dict {"position_href": cost}"""
        stock_price = dict()
        try:
            stock_dict = await self.async_requester.get_api_data_async(url_conf_key=self.url_stock_all, to_file=self.to_file)
            for pos in stock_dict['rows']:
                stock_price[pos['meta']['href']] = pos['price']/100
        except Exception as e:
            msg = f"module {__class__.__name__} can't read stock_all data, error: {e}"
            self.logger.error(msg)
        return stock_price
    async def get_stores_dict_async(self) -> dict:
        """ return stores dict {store_href: store_name }"""
        stores = dict()

        try:
            stores_dict = await self.async_requester.get_api_data_async(url_conf_key=self.url_stores, to_file=self.to_file)
            for pos in stores_dict['rows']:
                stores[pos['meta']['href']] = pos['name']
        except Exception as e:
            msg = f"module {__class__.__name__} can't read stock_all data, error: {e}"
            self.logger.error(msg)
        return stores
    async def get_stores_cost_dict_async(self) -> dict:
        """ return stores dict {store_href: store_name }"""
        stores = dict()
        # request goods price
        goods_cost_dict = await self.get_goods_cost_async()
        try:
            goods_by_stores_dict = await self.async_requester.get_api_data_async(url_conf_key=self.url_stock_stores, to_file=self.to_file)
            for pos in goods_by_stores_dict['rows']:
                goods_href = pos['meta']['href']
                goods_cost = goods_cost_dict.get(goods_href, 0)
                for stock in pos['stockByStore']:
                    stock_name = dict(stock).get('name', 'unknown_store')
                    stock_num = dict(stock).get('stock', 0)
                    stores[stock_name] = stock_num * goods_cost + stores.get(stock_name, 0)
        except Exception as e:
            msg = f"module {__class__.__name__} can't read stock_all data, error: {e}"
            self.logger.error(msg)
        # return stores
        return dict(sorted(stores.items(), key=lambda x: int(x[1]), reverse=True))

if __name__ == "__main__":
    connect = MSStoresSumAsync()
    # print(connect.get_stores_good_price())
    # print(connect.get_stores_dict())
    print(asyncio.run(connect.get_stores_cost_dict_async()))
    connect.logger.debug("stock_all class initialized")
