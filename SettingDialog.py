import wx
import GlobalVars

class SettingDialog(wx.Dialog):
    __main_sizer: wx.BoxSizer
    __setting : dict
    
    '''
    setting = {
        'language_type': __language_type,
        'hot_key':
        {
            'capture': ctrl + atl + a,
        }
    }
    '''

    def __init__(self, _parent, _setting, _size=wx.DefaultSize):
        super().__init__(_parent, wx.ID_ANY, u'设置', size=_size)
        self.__setting = _setting
        self.__InitUI()

        return

    def __InitUI(self):
        self.__main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.__hotkey_text_ctrl = self.__InitHotkeySetting()
        self.__lang_type_sel = self.__InitLanguageTypeSelection()
        self.__main_sizer.AddStretchSpacer(1)
        self.__InitDialogButton()
        self.SetSizer(self.__main_sizer)
        # self.Fit()
        return

    def __InitHotkeySetting(self):
        BORDER = 5
        hotkey_set_sizer = wx.BoxSizer(wx.HORIZONTAL)
        hotkey_label = wx.StaticText(self, wx.ID_ANY, u'全局热键：')
        hotkey_text_ctrl = wx.TextCtrl(self, size=(150, -1))
        

        hotkey_set_sizer.Add(hotkey_label, 0, wx.ALIGN_CENTER | wx.ALL, BORDER)
        hotkey_set_sizer.Add(hotkey_text_ctrl, 1, wx.EXPAND | wx.ALL, BORDER)
        self.__main_sizer.Add(hotkey_set_sizer, 0, wx.ALIGN_CENTER)
        hotkey_text_ctrl.Bind(wx.EVT_CHAR, self.__OnChar)
        if 'hotkey' in self.__setting and self.__setting['hotkey']:
            hotkey_text_ctrl.SetValue('Ctrl + Alt + ' + self.__setting['hotkey'])
        return hotkey_text_ctrl

    def __InitLanguageTypeSelection(self):
        BORDER = 5
        lang_type_label = wx.StaticText(self, wx.ID_ANY, u'识别语言：')
        lang_type_sel = wx.ComboBox(self,
                                    wx.ID_ANY,
                                    wx.EmptyString,
                                    size=(150, -1),
                                    style=wx.CB_DROPDOWN
                                    | wx.CB_READONLY)
        i = 0
        select_index = 0
        for key, value in GlobalVars.RECONIZE_LANGUAGE.items():
            lang_type_sel.Append(key, value)
            if 'language_type' in self.__setting:
                if self.__setting['language_type'] == value:
                    select_index = i
            i += 1

        lang_type_sel.SetSelection(select_index)
        self.__setting['language_type'] = lang_type_sel.GetClientData(select_index)
        lang_type_sel.Bind(wx.EVT_COMBOBOX, self.__OnLanguageTypeSelect)

        lang_type_sizer = wx.BoxSizer(wx.HORIZONTAL)
        lang_type_sizer.Add(lang_type_label, 0, wx.ALIGN_CENTER | wx.ALL, BORDER)
        lang_type_sizer.Add(lang_type_sel, 1, wx.EXPAND | wx.ALL, BORDER)
        self.__main_sizer.Add(lang_type_sizer, 0, wx.ALIGN_CENTER)
        return lang_type_sel
    
    def __InitDialogButton(self):
        BORDER = 5
        dialog_button_line = wx.StaticLine(self, wx.ID_ANY)
        dialog_button_sizer = wx.StdDialogButtonSizer()
        button_ok = wx.Button(self, wx.ID_OK, u'确定')
        button_cancel = wx.Button(self, wx.ID_CANCEL, u'取消')
        dialog_button_sizer.AddButton(button_ok)
        dialog_button_sizer.AddButton(button_cancel)
        dialog_button_sizer.Realize()
        self.__main_sizer.Add(dialog_button_line, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, BORDER)
        self.__main_sizer.Add(dialog_button_sizer, 0, wx.ALIGN_CENTER | wx.ALL, BORDER)
        return

    def __OnChar(self, _evt: wx.KeyEvent):
        key_code = _evt.GetKeyCode()
        text: str = ''
        if key_code == 32:
            text = u'[空格]'
        elif key_code in range(33, 126):
            text = chr(key_code).upper()
        elif key_code == 8 or key_code == 127:
            self.__hotkey_text_ctrl.Clear()

        if text:
            self.__hotkey_text_ctrl.SetValue('Ctrl + Alt + ' + text)
        else:
            _evt.Skip()

        self.__setting['hotkey'] = text
        return

    def __OnLanguageTypeSelect(self, _evt: wx.CommandEvent):
        self.__setting['language_type'] = self.__lang_type_sel.GetClientData(
            _evt.GetSelection())
        return
    
    def GetSetting(self) -> dict:
        
        return self.__setting