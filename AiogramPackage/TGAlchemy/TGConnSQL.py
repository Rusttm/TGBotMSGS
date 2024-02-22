import asyncio

from AiogramPackage.TGConnectors.BOTMainClass import BOTMainClass
import os
class TGConnSQL(BOTMainClass):
    logger_name = f"{os.path.basename(__file__)}"
    _main_key = "bot_config"
    _sql_key = "sql_config"
    _type_sql_key = "sqlite_config"
    # _type_sql_key = "pgsql_config"
    _config_dir_name = "config"
    _config_file_name = "bot_main_config.json"
    _db_dir_name = "data_sql"
    # _db_file_name = "sql.db"
    _module_config: dict = None
    __url: str = None
    def __init__(self):
        super().__init__()

    def get_sql_url(self):
        try:
            self._module_config = self.get_main_config_json_data_sync(self._config_dir_name, self._config_file_name)
            sql_config_dict = self._module_config.get(self._main_key).get(self._sql_key).get(self._type_sql_key)
            init_modules = sql_config_dict.get("init_modules", '')
            host = sql_config_dict.get('url', '')
            port = sql_config_dict.get('port', '')
            database = sql_config_dict.get('db_name', '')
            user = sql_config_dict.get('user', '')
            password = sql_config_dict.get('user_pass', '')
            self.logger.debug(f"{__class__.__name__} read data from config")
            if self._type_sql_key == "sqlite_config":
                up_file_dir = os.path.dirname(os.path.dirname(__file__))
                db_path = os.path.join(up_file_dir, self._db_dir_name, database)
                self.__url = f"{init_modules}:///{db_path}"
            else:
                self.__url = f"{init_modules}://{user}:{password}@{host}:{port}/{database}"
            # self.__url_no_db = f"postgresql://{user}:{password}@{host},{port}/"
        except Exception as e:
            print(f"configuration data not loaded {e}")
            self.logger.error(f"{__class__.__name__} can't create connector in SQLAlchemy! {e}")
        return self.__url

if __name__ == "__main__":
    product = dict({'meta': {'href': 'https://api.moysklad.ru/api/remap/1.2/entity/product/019c8e46-a807-11eb-0a80-00ec00080e83', 'metadataHref': 'https://api.moysklad.ru/api/remap/1.2/entity/product/metadata', 'type': 'product', 'mediaType': 'application/json', 'uuidHref': 'https://online.moysklad.ru/app/#good/edit?id=019c84fe-a807-11eb-0a80-00ec00080e7d'},
                    'id': '019c8e46-a807-11eb-0a80-00ec00080e83',
                    'accountId': 'e4154b3e-56fa-11eb-0a80-06e200011b76',
                    'owner': {'meta': {'href': 'https://api.moysklad.ru/api/remap/1.2/entity/employee/e430cdb4-56fa-11eb-0a80-079c0026a51d', 'metadataHref': 'https://api.moysklad.ru/api/remap/1.2/entity/employee/metadata', 'type': 'employee', 'mediaType': 'application/json', 'uuidHref': 'https://online.moysklad.ru/app/#employee/edit?id=e430cdb4-56fa-11eb-0a80-079c0026a51d'}},
                    'shared': True,
                    'group': {'meta': {'href': 'https://api.moysklad.ru/api/remap/1.2/entity/group/e415b013-56fa-11eb-0a80-06e200011b77', 'metadataHref': 'https://api.moysklad.ru/api/remap/1.2/entity/group/metadata', 'type': 'group', 'mediaType': 'application/json'}},
                    'updated': '2022-03-05 01:13:56.083',
                    'name': 'AA33L-Y02A1 Цилиндр с уплотнительными кольцами MT8016LN#102',
                    'description': 'AA33L-Y02A1 Цилиндр с уплотнительными кольцами MT8016LN#102',
                    'code': 'м77000000000929',
                    'externalCode': 'pegSRlphgwfboyZfp5FHB0',
                    'archived': False,
                    'pathName': 'Торговый каталог/Запасные части/Запасные части Meite MT8016 NL',
                    'productFolder': {'meta': {'href': 'https://api.moysklad.ru/api/remap/1.2/entity/productfolder/7dac9640-a806-11eb-0a80-01430007cea9', 'metadataHref': 'https://api.moysklad.ru/api/remap/1.2/entity/productfolder/metadata', 'type': 'productfolder', 'mediaType': 'application/json', 'uuidHref': 'https://online.moysklad.ru/app/#good/edit?id=7dac9640-a806-11eb-0a80-01430007cea9'}},
                    'effectiveVat': 20,
                    'effectiveVatEnabled': True,
                    'vat': 20, 'vatEnabled': True,
                    'useParentVat': False,
                    'uom': {'meta': {'href': 'https://api.moysklad.ru/api/remap/1.2/entity/uom/19f1edc0-fc42-4001-94cb-c9ec9c62ec10', 'metadataHref': 'https://api.moysklad.ru/api/remap/1.2/entity/uom/metadata', 'type': 'uom', 'mediaType': 'application/json'}},
                    'images': {'meta': {'href': 'https://api.moysklad.ru/api/remap/1.2/entity/product/019c8e46-a807-11eb-0a80-00ec00080e83/images', 'type': 'image', 'mediaType': 'application/json', 'size': 0, 'limit': 1000, 'offset': 0}},
                    'minPrice': {'value': 60000.0, 'currency': {'meta': {'href': 'https://api.moysklad.ru/api/remap/1.2/entity/currency/e4485ffd-56fa-11eb-0a80-079c0026a562', 'metadataHref': 'https://api.moysklad.ru/api/remap/1.2/entity/currency/metadata', 'type': 'currency', 'mediaType': 'application/json', 'uuidHref': 'https://online.moysklad.ru/app/#currency/edit?id=e4485ffd-56fa-11eb-0a80-079c0026a562'}}},
                    'salePrices': [{'value': 240000.0, 'currency': {'meta': {'href': 'https://api.moysklad.ru/api/remap/1.2/entity/currency/e4485ffd-56fa-11eb-0a80-079c0026a562', 'metadataHref': 'https://api.moysklad.ru/api/remap/1.2/entity/currency/metadata', 'type': 'currency', 'mediaType': 'application/json', 'uuidHref': 'https://online.moysklad.ru/app/#currency/edit?id=e4485ffd-56fa-11eb-0a80-079c0026a562'}},
                                    'priceType': {'meta': {'href': 'https://api.moysklad.ru/api/remap/1.2/context/companysettings/pricetype/e4492cfd-56fa-11eb-0a80-079c0026a563', 'type': 'pricetype', 'mediaType': 'application/json'}, 'id': 'e4492cfd-56fa-11eb-0a80-079c0026a563', 'name': 'Цена розн', 'externalCode': 'cbcf493b-55bc-11d9-848a-00112f43529a'}},
                                   {'value': 0.0, 'currency': {'meta': {'href': 'https://api.moysklad.ru/api/remap/1.2/entity/currency/e4485ffd-56fa-11eb-0a80-079c0026a562', 'metadataHref': 'https://api.moysklad.ru/api/remap/1.2/entity/currency/metadata', 'type': 'currency', 'mediaType': 'application/json', 'uuidHref': 'https://online.moysklad.ru/app/#currency/edit?id=e4485ffd-56fa-11eb-0a80-079c0026a562'}},
                                    'priceType': {'meta': {'href': 'https://api.moysklad.ru/api/remap/1.2/context/companysettings/pricetype/91ef8b05-570f-11eb-0a80-079c0029e363', 'type': 'pricetype', 'mediaType': 'application/json'}, 'id': '91ef8b05-570f-11eb-0a80-079c0029e363', 'name': 'Цена опт', 'externalCode': '6b4df01d-572c-4bcd-a72c-44bb568ff7ba'}}, {'value': 0.0, 'currency': {'meta': {'href': 'https://api.moysklad.ru/api/remap/1.2/entity/currency/e4485ffd-56fa-11eb-0a80-079c0026a562', 'metadataHref': 'https://api.moysklad.ru/api/remap/1.2/entity/currency/metadata', 'type': 'currency', 'mediaType': 'application/json', 'uuidHref': 'https://online.moysklad.ru/app/#currency/edit?id=e4485ffd-56fa-11eb-0a80-079c0026a562'}},
                                                                                                                                                                                                                                                                                                                                                                       'priceType': {'meta': {'href': 'https://api.moysklad.ru/api/remap/1.2/context/companysettings/pricetype/cdaa9907-69f6-11eb-0a80-0338002d0134', 'type': 'pricetype', 'mediaType': 'application/json'}, 'id': 'cdaa9907-69f6-11eb-0a80-0338002d0134', 'name': 'Арбен', 'externalCode': '1fcaec3a-1980-4bb2-94c7-c3baa8b18c3c'}}, {'value': 0.0, 'currency': {'meta': {'href': 'https://api.moysklad.ru/api/remap/1.2/entity/currency/e4485ffd-56fa-11eb-0a80-079c0026a562', 'metadataHref': 'https://api.moysklad.ru/api/remap/1.2/entity/currency/metadata', 'type': 'currency', 'mediaType': 'application/json', 'uuidHref': 'https://online.moysklad.ru/app/#currency/edit?id=e4485ffd-56fa-11eb-0a80-079c0026a562'}}, 'priceType': {'meta': {'href': 'https://api.moysklad.ru/api/remap/1.2/context/companysettings/pricetype/0f7205d7-7b33-11eb-0a80-08f800068612', 'type': 'pricetype', 'mediaType': 'application/json'}, 'id': '0f7205d7-7b33-11eb-0a80-08f800068612', 'name': 'ЭРА', 'externalCode': '07b29f4b-8c02-49a6-ad86-4423efc4ff0b'}}, {'value': 0.0, 'currency': {'meta': {'href': 'https://api.moysklad.ru/api/remap/1.2/entity/currency/e4485ffd-56fa-11eb-0a80-079c0026a562', 'metadataHref': 'https://api.moysklad.ru/api/remap/1.2/entity/currency/metadata', 'type': 'currency', 'mediaType': 'application/json', 'uuidHref': 'https://online.moysklad.ru/app/#currency/edit?id=e4485ffd-56fa-11eb-0a80-079c0026a562'}}, 'priceType': {'meta': {'href': 'https://api.moysklad.ru/api/remap/1.2/context/companysettings/pricetype/44b0b82f-d402-11eb-0a80-0ddf000718b0', 'type': 'pricetype', 'mediaType': 'application/json'}, 'id': '44b0b82f-d402-11eb-0a80-0ddf000718b0', 'name': 'Сапогова', 'externalCode': 'e8448e0f-1548-4b36-9075-281ac209f846'}}, {'value': 0.0, 'currency': {'meta': {'href': 'https://api.moysklad.ru/api/remap/1.2/entity/currency/e4485ffd-56fa-11eb-0a80-079c0026a562', 'metadataHref': 'https://api.moysklad.ru/api/remap/1.2/entity/currency/metadata', 'type': 'currency', 'mediaType': 'application/json', 'uuidHref': 'https://online.moysklad.ru/app/#currency/edit?id=e4485ffd-56fa-11eb-0a80-079c0026a562'}}, 'priceType': {'meta': {'href': 'https://api.moysklad.ru/api/remap/1.2/context/companysettings/pricetype/c3fe9017-359c-11ec-0a80-029b00069168', 'type': 'pricetype', 'mediaType': 'application/json'}, 'id': 'c3fe9017-359c-11ec-0a80-029b00069168', 'name': 'МЕГАСТРОЙ', 'externalCode': '183119a1-5c92-4bdf-836e-c1ddf63872e7'}}, {'value': 0.0, 'currency': {'meta': {'href': 'https://api.moysklad.ru/api/remap/1.2/entity/currency/e4485ffd-56fa-11eb-0a80-079c0026a562', 'metadataHref': 'https://api.moysklad.ru/api/remap/1.2/entity/currency/metadata', 'type': 'currency', 'mediaType': 'application/json', 'uuidHref': 'https://online.moysklad.ru/app/#currency/edit?id=e4485ffd-56fa-11eb-0a80-079c0026a562'}}, 'priceType': {'meta': {'href': 'https://api.moysklad.ru/api/remap/1.2/context/companysettings/pricetype/888049bd-aec9-11ee-0a80-117b007a4e00', 'type': 'pricetype', 'mediaType': 'application/json'}, 'id': '888049bd-aec9-11ee-0a80-117b007a4e00', 'name': 'Стройгранд', 'externalCode': '8b37fe0a-4f4e-42f9-be86-b3eddfc0d133'}}],
                    'buyPrice': {'value': 345.0, 'currency': {'meta': {'href': 'https://api.moysklad.ru/api/remap/1.2/entity/currency/eeb95bfd-570b-11eb-0a80-01de0029f5ef', 'metadataHref': 'https://api.moysklad.ru/api/remap/1.2/entity/currency/metadata', 'type': 'currency', 'mediaType': 'application/json', 'uuidHref': 'https://online.moysklad.ru/app/#currency/edit?id=eeb95bfd-570b-11eb-0a80-01de0029f5ef'}}},
                    'barcodes': [{'ean13': '2000000009933'}, {'code128': 'AA33L-Y02A1'}],
                    'supplier': {'meta': {'href': 'https://api.moysklad.ru/api/remap/1.2/entity/counterparty/3297017e-5783-11eb-0a80-06ec00b86625', 'metadataHref': 'https://api.moysklad.ru/api/remap/1.2/entity/counterparty/metadata', 'type': 'counterparty', 'mediaType': 'application/json', 'uuidHref': 'https://online.moysklad.ru/app/#company/edit?id=3297017e-5783-11eb-0a80-06ec00b86625'}},
                    'attributes': [{'meta': {'href': 'https://api.moysklad.ru/api/remap/1.2/entity/product/metadata/attributes/838b9fcc-859d-11eb-0a80-005a00356e0b', 'type': 'attributemetadata', 'mediaType': 'application/json'}, 'id': '838b9fcc-859d-11eb-0a80-005a00356e0b', 'name': 'Производитель', 'type': 'string', 'value': 'Meite'}, {'meta': {'href': 'https://api.moysklad.ru/api/remap/1.2/entity/product/metadata/attributes/3d57e1e2-859e-11eb-0a80-010e0037e03f', 'type': 'attributemetadata', 'mediaType': 'application/json'}, 'id': '3d57e1e2-859e-11eb-0a80-010e0037e03f', 'name': 'Модель', 'type': 'string', 'value': 'MT8016LN#102'}, {'meta': {'href': 'https://api.moysklad.ru/api/remap/1.2/entity/product/metadata/attributes/c56db16b-859e-11eb-0a80-005a00359f0d', 'type': 'attributemetadata', 'mediaType': 'application/json'}, 'id': 'c56db16b-859e-11eb-0a80-005a00359f0d', 'name': 'Код производителя', 'type': 'string', 'value': 'AA33L-Y02A1'}, {'meta': {'href': 'https://api.moysklad.ru/api/remap/1.2/entity/product/metadata/attributes/b0fe8080-859e-11eb-0a80-02b50037a4da', 'type': 'attributemetadata', 'mediaType': 'application/json'}, 'id': 'b0fe8080-859e-11eb-0a80-02b50037a4da', 'name': 'Категория товара', 'type': 'string', 'value': 'Все товары/Строительство и ремонт/Инструменты/Расходные материалы и оснастка/Для пневмоинструмента'}],
                    'paymentItemType': 'GOOD',
                    'discountProhibited': False,
                    'country': {'meta': {'href': 'https://api.moysklad.ru/api/remap/1.2/entity/country/fd44cd2e-b398-4222-9c43-f75688bdf327', 'metadataHref': 'https://api.moysklad.ru/api/remap/1.2/entity/country/metadata', 'type': 'country', 'mediaType': 'application/json', 'uuidHref': 'https://online.moysklad.ru/app/#country/edit?id=fd44cd2e-b398-4222-9c43-f75688bdf327'}},
                    'article': 'MT8016LN#102',
                    'weight': 0.0,
                    'volume': 0.0,
                    'variantsCount': 0,
                    'isSerialTrackable': False,
                    'trackingType': 'NOT_TRACKED',
                    'files': {'meta': {'href': 'https://api.moysklad.ru/api/remap/1.2/entity/product/019c8e46-a807-11eb-0a80-00ec00080e83/files', 'type': 'files', 'mediaType': 'application/json', 'size': 0, 'limit': 1000, 'offset': 0}}})
    connector = TGConnSQL()
    print(connector.get_sql_url())