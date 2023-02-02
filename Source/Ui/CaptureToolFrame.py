import wx
import Util

class CaptureToolFrame(wx.Frame):
    ID_OK = 300
    ID_CANCEL = 301
    BUTTON_SIZE = (35, 35)

    def __init__(self, _parent, _pos):
        super().__init__(
            _parent, 
            pos=_pos, 
            style=wx.NO_BORDER | wx.STAY_ON_TOP
        )
        self.__last_point = _pos
        self.TOOL_BUTTON_SETTING = {
        self.ID_OK: 
        {
            'show_on_screen': True,
            'size': self.BUTTON_SIZE,           
            'icon': u'截图_screenshot-one.png',  
            'help_text': u'确定',
            'handler': self.__OnOk
        },
        self.ID_CANCEL: 
        {
            'show_on_screen': True,
            'size': self.BUTTON_SIZE,
            'icon': u'退出_logout.png',
            'help_text': u'确定',
            'handler': self.__OnCancel                
        }
    }
        self.__InitUi()
        self.Show()
        self.Raise()
        
        return
    
    def __InitUi(self):
        BORDER = 5
        self.__main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.__buttons: dict[str, wx.BitmapButton] = {}
        for btn_id, btn_set in self.TOOL_BUTTON_SETTING.items():
            if 'show_on_screen' in btn_set and btn_set['show_on_screen']:
                bmp = Util.GetIcon(btn_set['icon'], btn_set['size'])
                bmp_btn = wx.BitmapButton(
                    self, 
                    btn_id, 
                    bmp, 
                    size=btn_set['size']
                )
                bmp_btn.SetLabel(btn_set['help_text'])
                bmp_btn.SetHelpText(btn_set['help_text'])
                self.__main_sizer.Add(bmp_btn, 0, wx.ALL, BORDER)
                self.__buttons[btn_id] = bmp_btn
                bmp_btn.Bind(wx.EVT_BUTTON, btn_set['handler'], id=btn_id)
        self.SetSizerAndFit(self.__main_sizer)
        
        return
                
    def __OnOk(self, _evt: wx.CommandEvent):
        self.Hide()
        self.Parent.GetCapture(self.__last_point)
        return
    
    def __OnCancel(self, _evt: wx.CommandEvent):
        self.Parent.Exit()
        return