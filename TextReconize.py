from threading import Thread
from api import APP_ID, API_KEY, SECRET_KEY
from aip import AipOcr
from MainFrame import Mainframe

class TextReconThread(Thread):
    def __init__(self, _image_stream, main_frame : Mainframe) -> None:
        super().__init__()
        self.__image_stream = _image_stream
        self.__result_text = ''
        self.__main_frame = main_frame
        
    def run(self) -> None:
        client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
        options = {'language_type': 'CHN_ENG', 'paragraph': True}
        try:
            result = client.basicGeneral(self.__image_stream.getvalue(), options)
        except:
            self.__result_text = u'网络连接失败！'
            return
        print(result)
        for res in result['words_result']:
            self.__result_text += res['words']
            self.__result_text += '\n'
        self.__main_frame.SetText(self.__result_text)
        return
    
    def GetResult(self):
        return self.__result_text