import wx
import GlobalVars


class SettingDialog(wx.Dialog):
    BORDER = 5
    SIZE = wx.Size(150, -1)
    __main_sizer: wx.BoxSizer
    __setting: dict
    __cap_dis_set_choices: dict[int: str]
    __close_setting_choices : dict[int: str]
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
        self.__cap_dis_set_choices = GlobalVars.CAPTURE_DISPLAY_SETTING
        self.__close_setting_choices = GlobalVars.CLOSE_SETTING
        self.__InitUI()

        return

    def __InitUI(self):
        self.__main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.__hotkey_text_ctrl = self.__InitHotkeySetting()
        self.__lang_type_sel = self.__InitLanguageTypeSelection()
        self.__cap_dis_set = self.__InitCaptrueDisplaySetting()
        self.__close_setting = self.__InitCloseSetting()
        self.__main_sizer.AddStretchSpacer(1)
        self.__InitDialogButton()
        self.SetSizerAndFit(self.__main_sizer)
        
        return

    def __InitHotkeySetting(self):
        border = self.BORDER
        size = self.SIZE
        hotkey_set_sizer = wx.BoxSizer(wx.HORIZONTAL)
        hotkey_label = wx.StaticText(self, wx.ID_ANY, u'全局热键：')
        hotkey_text_ctrl = wx.TextCtrl(self, size=size)

        hotkey_set_sizer.Add(hotkey_label, 0, wx.ALIGN_CENTER | wx.ALL, border)
        hotkey_set_sizer.Add(hotkey_text_ctrl, 1, wx.EXPAND | wx.ALL, border)
        self.__main_sizer.Add(hotkey_set_sizer, 0, wx.ALIGN_CENTER)
        hotkey_text_ctrl.Bind(wx.EVT_CHAR, self.__OnChar)
        if 'hotkey' in self.__setting and self.__setting['hotkey']:
            hotkey_text_ctrl.SetValue('Ctrl + Alt + ' +
                                      self.__setting['hotkey'])
        return hotkey_text_ctrl

    def __InitLanguageTypeSelection(self):
        border = self.BORDER
        size = self.SIZE
        lang_type_label = wx.StaticText(self, wx.ID_ANY, u'识别语言：')
        lang_type_sel = wx.ComboBox(self,
                                    wx.ID_ANY,
                                    wx.EmptyString,
                                    size=size,
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
        self.__setting['language_type'] = lang_type_sel.GetClientData(
            select_index)
        # lang_type_sel.Bind(wx.EVT_COMBOBOX, self.__OnLanguageTypeSelect)

        lang_type_sizer = wx.BoxSizer(wx.HORIZONTAL)
        lang_type_sizer.Add(lang_type_label, 0, wx.ALIGN_CENTER | wx.ALL,
                            border)
        lang_type_sizer.Add(lang_type_sel, 1, wx.EXPAND | wx.ALL, border)
        self.__main_sizer.Add(lang_type_sizer, 0, wx.ALIGN_CENTER)
        return lang_type_sel

    def __InitCaptrueDisplaySetting(self):
        border = self.BORDER
        size = self.SIZE
        cap_dis_set_sizer = wx.BoxSizer(wx.HORIZONTAL)
        cap_dis_set_label = wx.StaticText(self, label=u'截屏方式：')
        cap_dis_set = wx.RadioBox(self,
                                  choices=list(
                                      self.__cap_dis_set_choices.values()),
                                  style=wx.RA_SPECIFY_COLS,
                                  majorDimension=1,
                                  size=size)
        if wx.Display.GetCount() == 1:
            cap_dis_set.EnableItem(
                cap_dis_set.FindString(self.__cap_dis_set_choices[
                    GlobalVars.CAPTURE_ALL_DISPLAY]), False)
            cap_dis_set.SetSelection(cap_dis_set.FindString(self.__cap_dis_set_choices[
                    GlobalVars.CAPTURE_CURRENT_DISPLAY]))
        cap_dis_set_sizer.Add(cap_dis_set_label, 0, wx.ALIGN_CENTER | wx.ALL,
                              border)
        cap_dis_set_sizer.Add(cap_dis_set, 1, wx.EXPAND | wx.ALL, border)
        self.__main_sizer.Add(cap_dis_set_sizer, 0, wx.ALIGN_CENTER)

        return cap_dis_set
    
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

        # self.__setting['hotkey'] = text
        return

    # def __OnLanguageTypeSelect(self, _evt: wx.CommandEvent):
    #     # self.__setting['language_type'] = self.__lang_type_sel.GetClientData(
    #     #     _evt.GetSelection())
    #     return

    def GetSetting(self) -> dict:
        import Util
        self.__setting['hotkey'] = self.__hotkey_text_ctrl.GetValue()[-1::]
        self.__setting['language_type'] = self.__lang_type_sel.GetClientData(
            self.__lang_type_sel.GetSelection())
        self.__setting['capture_all_display'] = Util.GetDictKey(
            self.__cap_dis_set_choices,
            self.__cap_dis_set.GetString(self.__cap_dis_set.GetSelection()))
        self.__setting['close_setting'] = Util.GetDictKey(
            self.__close_setting_choices, 
            self.__close_setting.GetString(self.__close_setting.GetSelection()))
        return self.__setting