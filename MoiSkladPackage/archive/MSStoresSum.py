import os

from MoiSkladPackage.MSConnectors.MSMainClass import MSMainClass


class MSStoresSum(MSMainClass):
    """ clas get sum of stores"""
    logger_name = f"{os.path.basename(__file__)}"
    url_stock_all = "url_stock_all"
    url_stores = "url_stores"
    url_stock_stores = "url_stock_stores"


    def __init__(self):
        super().__init__()

    def get_goods_cost(self) -> dict:
        """this return dict {"position_href": cost}"""
        stock_price = dict()
        try:
            from MoiSkladPackage.archive.MSRequester import MSRequester
            requester = MSRequester()
            requester.set_config(self.url_stock_all)
            stock_dict = requester.get_api_data(to_file=True)
            for pos in stock_dict['rows']:
                stock_price[pos['meta']['href']] = pos['price']/100
        except Exception as e:
            msg = f"module {__class__.__name__} can't read stock_all data, error: {e}"
            self.logger.error(msg)
        return stock_price
    def get_stores_dict(self) -> dict:
        """ return stores dict {store_href: store_name }"""
        stores = dict()

        try:
            from MoiSkladPackage.archive.MSRequester import MSRequester
            requester = MSRequester()
            requester.set_config(self.url_stores)
            stores_dict = requester.get_api_data(to_file=True)
            for pos in stores_dict['rows']:
                stores[pos['meta']['href']] = pos['name']
        except Exception as e:
            msg = f"module {__class__.__name__} can't read stock_all data, error: {e}"
            self.logger.error(msg)
        return stores
    def get_stores_cost_dict(self) -> dict:
        """ return stores dict {store_href: store_name }"""
        stores = dict()
        # request goods price
        goods_cost_dict = self.get_goods_cost()
        try:
            from MoiSkladPackage.archive.MSRequester import MSRequester
            requester = MSRequester()
            requester.set_config(self.url_stock_stores)
            goods_by_stores_dict = requester.get_api_data(to_file=True)
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
    connect = MSStoresSum()
    # print(connect.get_stores_good_price())
    # print(connect.get_stores_dict())
    print(connect.get_stores_cost_dict())
    connect.logger.debug("stock_all class initialized")
