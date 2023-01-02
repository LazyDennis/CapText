import GlobalVars
import os
import json

class Setting:
    __default_setting = GlobalVars.DEFAULT_SETTING.copy()
    @staticmethod
    def ReadSettingFromFile(_file):
        setting: dict = {}
        if os.path.exists(_file):
            with open(_file, 'rb') as fp:
                try:
                    setting = json.loads(fp.read().decode('utf-8'))
                except:
                    setting = Setting.__default_setting
        else:
            setting = Setting.__default_setting
        return setting

    @staticmethod
    def SaveSettingToFile(_setting, _file):
        with open(_file, 'wb') as fp:
            fp.write(json.dumps(_setting, 
                                sort_keys=True,
                                indent=4,
                                separators=(',', ':')).encode('utf-8'))
        return