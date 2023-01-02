import wx
import GlobalVars


class CloseDialog(wx.Dialog):
    BORDER = 5
    SIZE = wx.Size(150, -1)
    __dialog_setting: dict = {}
    __close_setting_choices : dict[int: str]
    
    def __init__(self, _parent, _setting):
        super().__init__(_parent, title=u'关闭提示', style=wx.CAPTION)
        self.__dialog_setting['close_setting'] = _setting['close_setting']
        self.__close_setting_choices = GlobalVars.CLOSE_SETTING
        self.__InitUI()

    def __InitUI(self):
        self.__main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.__main_sizer.AddStretchSpacer(1)
        self.__close_setting: wx.RadioBox = self.__InitCloseSetting()
        self.__main_sizer.AddStretchSpacer(1)
        self.__close_prompt: wx.CheckBox = self.__InitPrompt()
        self.__main_sizer.AddStretchSpacer(1)
        self.__InitDialogButton()
        self.SetSizer(self.__main_sizer)
        self.Fit()
        return
    
    def __InitCloseSetting(self):
        border = self.BORDER
        size = self.SIZE
        close_setting_label = wx.StaticText(self, label=u'关闭方式：')
        close_setting = wx.RadioBox(self, 
                                    size=size, 
                                    majorDimension=1, 
                                    style=wx.RA_SPECIFY_COLS,
                                    choices=list(self.__close_setting_choices.values()))
        close_setting.SetSelection(
            close_setting.FindString(
                self.__close_setting_choices[GlobalVars.CLOSE_TO_TASKBAR]))
        close_setting_sizer = wx.BoxSizer(wx.HORIZONTAL)
        close_setting_sizer.Add(close_setting_label, 0, wx.ALIGN_CENTER | wx.ALL, border)
        close_setting_sizer.Add(close_setting, 1, wx.EXPAND | wx.ALL, border)
        self.__main_sizer.Add(close_setting_sizer, 0, wx.ALIGN_CENTER)
        
        return close_setting
    
    def __InitPrompt(self):
        border = self.BORDER
        size = self.SIZE
        close_prompt_sizer = wx.BoxSizer(wx.HORIZONTAL)
        close_prompt = wx.CheckBox(self, label=u'不再提示', size=size)
        close_prompt.SetValue(wx.CHK_UNCHECKED)
        close_prompt.SetHelpText(u'以后可以在设置中修改。')
        close_prompt_sizer.Add(close_prompt, 0, wx.ALIGN_CENTER | wx.ALL, border)
        
        self.__main_sizer.Add(close_prompt_sizer, 0, wx.ALIGN_LEFT)
        
        return close_prompt
        

    def __InitDialogButton(self):
        border = self.BORDER
        dialog_button_line = wx.StaticLine(self, wx.ID_ANY)
        dialog_button_sizer = wx.StdDialogButtonSizer()
        button_ok = wx.Button(self, wx.ID_OK, u'确定')
        button_cancel = wx.Button(self, wx.ID_CANCEL, u'取消')
        dialog_button_sizer.AddButton(button_ok)
        dialog_button_sizer.AddButton(button_cancel)
        dialog_button_sizer.Realize()
        self.__main_sizer.Add(dialog_button_line, 0,
                              wx.EXPAND | wx.TOP | wx.BOTTOM, border)
        self.__main_sizer.Add(dialog_button_sizer, 0, wx.ALIGN_CENTER | wx.ALL,
                              border)
        return
    
    def GetSetting(self) -> dict:
        import Util
        self.__dialog_setting['allowed_prompt'] = (
            self.__close_prompt.GetValue() == wx.CHK_UNCHECKED)
        self.__dialog_setting['close_setting'] = Util.GetDictKey(
            self.__close_setting_choices, 
            self.__close_setting.GetString(self.__close_setting.GetSelection()))
        return self.__dialog_setting
    