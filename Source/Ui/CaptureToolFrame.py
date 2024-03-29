import wx
import Util
import GlobalVars

class CaptureToolFrame(wx.Frame):
    ID_OK = 300
    ID_CANCEL = 301
    BUTTON_SIZE = (30, 30)

    def __init__(self, _parent, _pos=wx.DefaultPosition):
        super().__init__(
            _parent, 
            pos=_pos, 
            style=wx.NO_BORDER | wx.STAY_ON_TOP | wx.WANTS_CHARS
        )
        # self.__last_point = _pos
        self.TOOL_BUTTON_SETTING = {
            self.ID_OK: 
            {
                'show_on_screen': True,
                'size': self.BUTTON_SIZE,           
                'icon_disable': u'正确的_correct_grey.png',  
                'icon_normal': u'正确的_correct_green.png', 
                'help_text': u'确定',
                'handler': self.__OnOk
            },
            self.ID_CANCEL: 
            {
                'show_on_screen': True,
                'size': self.BUTTON_SIZE,
                'icon_disable': u'错误_error_grey.png',
                'icon_normal': u'错误_error_red.png', 
                'help_text': u'退出',
                'handler': self.__OnCancel                
            }
        }
        self.__keymap = {
            wx.WXK_ESCAPE: {
                'handler': self.__OnCancel,
                'id': self.ID_CANCEL
            },
            wx.WXK_RETURN: {
                'handler': self.__OnOk,
                'id': self.ID_OK
            }
        }
        self.__InitUi()
        self.Show()
        self.Raise()
        self.SetFocus()
        self.Bind(wx.EVT_CHAR, self.__OnChar)
        
        return
    
    def __InitUi(self):
        BORDER = 5
        self.__main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.__buttons: dict[str, wx.BitmapButton] = {}
        for button_id, button_setting in self.TOOL_BUTTON_SETTING.items():
            if 'show_on_screen' in button_setting and button_setting['show_on_screen']:
                bitmap_disable = Util.GetIcon(button_setting['icon_disable'], button_setting['size'])
                bitmap_normal =  Util.GetIcon(button_setting['icon_normal'], button_setting['size'])
                bitmap_button = wx.BitmapButton(
                    self, 
                    button_id, 
                    bitmap_disable, 
                    size=button_setting['size']
                )
                bitmap_button.SetLabel(button_setting['help_text'])
                bitmap_button.SetHelpText(button_setting['help_text'])
                bitmap_button.SetBitmapCurrent(bitmap_normal)
                self.__main_sizer.Add(bitmap_button, 0, wx.ALL, BORDER)
                self.__buttons[button_id] = bitmap_button
                bitmap_button.Bind(wx.EVT_BUTTON, button_setting['handler'], id=button_id)
        
        self.SetSizerAndFit(self.__main_sizer)
        
        return
                
    def __OnOk(self, _evt: wx.CommandEvent):
        self.Hide()
        self.Parent.GetCapture()
        return
    
    def __OnCancel(self, _evt: wx.CommandEvent):
        self.Parent.Exit()
        return

    def __OnChar(self, _evt: wx.KeyEvent):
        key_code = _evt.GetKeyCode()
        # print(self.__class__, '.__Onchar: ', key_code)
        if key_code in self.__keymap:
            _evt.SetId(self.__keymap[key_code]['id'])
            self.__keymap[key_code]['handler'](_evt)
        else:
            _evt.Skip()
        return