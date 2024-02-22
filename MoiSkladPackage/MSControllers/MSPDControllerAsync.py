import os
from GoogleSpreadPackage.GSMSContAsync import GSMSContAsync
import asyncio
import pandas as pd


class MSPDControllerAsync(GSMSContAsync):
    logger_name = f"{os.path.basename(__file__)}"
    def __init__(self):
        super().__init__()

    async def pd_profit_report_async(self, from_date="2024-01-01", to_date="2024-01-31") -> pd.DataFrame:
        """ converter to pd"""
        profit_data = pd.DataFrame()
        try:
            from MoiSkladPackage.MSReports.MSReportProfitAsync import MSReportProfitAsync
            connector = MSReportProfitAsync()
            ms_data = await connector.get_handled_expenses(from_date=from_date, to_date=to_date)
            # await self.save_balances_ms_gs_async(balances_data)
            columns = ms_data.get("col_list")
            data = ms_data.get("data")
            spread_sheet_df = pd.DataFrame(data, columns=columns)
            print(spread_sheet_df)
            msg = f"{__class__.__name__} saves balance data to spreadsheet. "
            self.logger.debug(msg)
        except Exception as e:
            msg = f"{__class__.__name__} cant saves balance data to spreadsheet, Error: \n {e} "
            self.logger.warning(msg)
            print(msg)
        return profit_data




if __name__ == "__main__":
    controller = MSPDControllerAsync()
    # print(connect.get_stores_good_price())
    # print(connect.get_stores_dict())
    print(asyncio.run(controller.pd_profit_report_async()))
    controller.logger.debug("stock_all class initialized")