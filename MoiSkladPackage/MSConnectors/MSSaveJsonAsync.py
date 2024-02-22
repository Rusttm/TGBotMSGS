from MoiSkladPackage.MSConnectors.MSMainClass import MSMainClass
import os
import json
import re
import aiofiles
import asyncio


class MSSaveJsonAsync(MSMainClass):
    """ connector: save dictionary data file to json """
    logger_name = f"{os.path.basename(__file__)}"
    _dir_name = "data"
    _file_name = "ms_requested_data.json"
    
    def __init__(self):
        super().__init__()

    async def save_data_json_file_async(self, data_dict=None, file_name=None, dir_name=None) -> bool:
        """ save dictionary data file to json
        return True or False"""
        try:
            if file_name:
                self._file_name = await self.corrected_file_name(file_name)
            # if dir_name == "config":
            if dir_name:
                self._dir_name = dir_name
            up_dir_file = os.path.dirname(os.path.dirname(__file__))
            dir_path = os.path.join(up_dir_file, self._dir_name)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            DATA_FILE_PATH = os.path.join(dir_path, f"{self._file_name}")
            if not os.path.exists(DATA_FILE_PATH):
                await aiofiles.open(DATA_FILE_PATH, 'x')
            if os.path.exists(DATA_FILE_PATH) and data_dict:
                async with aiofiles.open(DATA_FILE_PATH, 'w') as ff:
                    await ff.write(json.dumps(data_dict, ensure_ascii=False))
                self.logger.debug(f"{__class__.__name__} saved data to json file {DATA_FILE_PATH}")
                return True
            else:
                self.logger.error(f"{__class__.__name__} can't read json file, it doesnt exist!")
                # print(f"{__class__.__name__} can't write data to file {self.file_name}")
                return False
        except Exception as e:
            self.logger.error(f"{__class__.__name__} can't write to json file! {e}")
            # print(e)
            return False

    async def corrected_file_name(self, file_name) -> str:
        """ return corrected file name in filename.json"""
        if re.search("json", file_name):
            return file_name
        else:
            return f"{file_name}.json"

    def save_data_json_file_sync(self, data_dict: dict, file_name: str) -> bool:
        try:
            loop = asyncio.get_event_loop()
            result = loop.run_until_complete(self.save_data_json_file_async(data_dict=data_dict, file_name=file_name))
        except:
            loop = asyncio.new_event_loop()
            result = loop.run_until_complete(self.save_data_json_file_async(data_dict=data_dict, file_name=file_name))
        return result


if __name__ == '__main__':
    connector = MSSaveJsonAsync()
    print(connector.save_data_json_file_sync(data_dict={"data": "some data"}, file_name="temporary_file"))
    # print(connector.save_data_json_file(data_dict={"data": "some data"}, file_name="temporary_file"))
