from aip import AipOcr
from threading import Thread

class TextReconizeThread(Thread):

    def __init__(self, _reconize_method, _args) -> None:
        super().__init__()
        self.__result_text = ''
        self.__args = _args
        self.__reconize_method = _reconize_method
    
    def run(self) -> None:
        self.__result_text = self.__reconize_method(**self.__args)
        return

    def Result(self):
        return self.__result_text if self.__result_text else ''


def BaiduOcr(_img, _appid='', _apikey='', _secretkey='', _options=None) -> str:
    if _appid and _apikey and _secretkey:
        client = AipOcr(_appid, _apikey, _secretkey)
    else:
        return

    result_text = ''
    try:
        result = client.basicGeneral(_img, _options)
        print(result)
        if 'words_result' in result:
            for res in result['words_result']:
                result_text += res['words']
                result_text += '\n'
        else:
            result_text = result
    except:
        result_text = u'网络连接失败！'

    return result_text

