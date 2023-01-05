import GlobalVars
import os
import pickle

class Setting:
    __default_setting = GlobalVars.DEFAULT_SETTING.copy()
    @staticmethod
    def ReadSettingFromFile(_file):
        setting: dict = {}
        if os.path.exists(_file):
            with open(_file, 'rb') as fp:
                try:
                    setting = pickle.load(fp)
                    for key, val in Setting.__default_setting.items():
                        if key not in setting:
                            setting[key] = val
                except:
                    setting = Setting.__default_setting
        else:
            setting = Setting.__default_setting
        return setting

    @staticmethod
    def SaveSettingToFile(_setting, _file):
        with open(_file, 'wb') as fp:
            pickle.dump(_setting, fp)
        return