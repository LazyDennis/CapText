from wx.adv import TaskBarIcon
import wx.adv
import wx
from GrabFrame import GrabFrame
from SettingDialog import SettingDialog
from io import BytesIO
import Util
from ImageTuningPanel import ImageTuningPanel
from Setting import Setting
from TextReconize import TextReconizeThread

import GlobalVars


class Mainframe(wx.Frame):
    __main_sizer: wx.BoxSizer
    __grab_frame: GrabFrame
    __capture_bitmap: wx.StaticBitmap
    __raw_bitmap: wx.Bitmap = None
    __result_bitmap: wx.Bitmap = None
    __result_text: wx.TextCtrl
    __handler_map: dict = None
    __keymap: dict = None
    __reconize_type: int = GlobalVars.RECONIZE_TYPE['百度']
    __reconize_method: dict = None
    __setting: dict = {}
    __tuning_panel: ImageTuningPanel = None
    __setting_file = GlobalVars.SETTING_FILE
    # __language_type: str

    def __init__(self, title):
        self.DEFAULT_WINDOW_SIZE = wx.Size(
            wx.GetDisplaySize().GetWidth() * 0.5,
            wx.GetDisplaySize().GetHeight() * 0.5)
        super().__init__(None, title=title, size=self.DEFAULT_WINDOW_SIZE)
        self.__handler_map = {
            '__OnNew': self.__OnNew,
            '__OnOpenImage': self.__OnOpenImage,
            '__OnSaveCapture': self.__OnSaveCapture,
            '__OnSaveText': self.__OnSaveText,
            '__OnExit': self.OnExit,
            '__OnCapture': self.OnCapture,
            '__OnRecognize': self.__OnRecognize,
            '__OnSetting': self.OnSetting,
            '__OnImageEnhance': self.__OnImageEnhance,
            '__OnHelp': self.__OnHelp,
            '__OnAbout': self.__OnAbout
        }

        self.__keymap = {
            wx.WXK_ESCAPE: {
                'handler': self.__OnKeyEsc,
                'id': wx.ID_ANY
            }
        }

        self.__setting = self.__InitSetting()

        self.__InitUi()

        self.ApplySetting()
        self.Bind(wx.EVT_SIZE, self.__OnResize)
        self.Bind(wx.EVT_CLOSE, self.__OnClose)
        self.Bind(wx.EVT_ICONIZE, self.__OnIconize)
        self.Bind(wx.EVT_MOVING, self.__OnMoving)

    def __InitSetting(self):
        return Setting.ReadSettingFromFile(self.__setting_file)

    def __InitUi(self):
        icon_bundle = wx.IconBundle()
        icon_bundle.AddIcon(
            wx.Icon(
                Util.GetIcon('frame_icon_large',
                             GlobalVars.ICON_SETTING['frame_icon_large'])))
        icon_bundle.AddIcon(
            wx.Icon(
                Util.GetIcon('frame_icon_small',
                             GlobalVars.ICON_SETTING['frame_icon_small'])))

        self.SetIcons(icon_bundle)
        self.__menu_bar = self.__InitMenu()
        self.__toolbar = self.__InitToolBar()
        self.__main_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.__main_sizer.Add(self.__InitCapturePanel(), 1, wx.EXPAND)
        self.__main_sizer.Add(self.__InitRecognizeResPanel(), 1, wx.EXPAND)

        self.__status_bar = self.__InitStatusBar()

        self.__taskbar_icon = MainframeIcon(self, self.__setting)

        self.SetSizer(self.__main_sizer)
        self.Center()

    def __InitMenu(self):
        menu_bar = wx.MenuBar()

        for menu_info in GlobalVars.MENUS:
            if menu_info['show_on_screen']:
                menu = wx.Menu()
                for item in menu_info['menu_items']:
                    if item['show_on_screen'] and 'menutool' in item and item['menutool']:
                        menu_item = wx.MenuItem(**item['property'])
                        if 'icon' in item and item['icon']:
                            menu_item.SetBitmap(
                                Util.GetIcon(
                                    item['icon'],
                                    GlobalVars.ICON_SETTING['menu_icon']))
                        menu.Append(menu_item)
                        if 'handler' in item and item['handler']:
                            handler = self.__handler_map[item['handler']]
                            self.Bind(wx.EVT_MENU,
                                      handler,
                                      id=item['property']['id'])
                            lastchar = item['property']['text'][-1::]
                            if ord(lastchar) >= ord('A') and ord(
                                    lastchar) <= ord('Z'):
                                self.__keymap[ord(lastchar) - ord('A') + 1] = {
                                    'handler': handler,
                                    'id': item['property']['id']
                                }
                menu_bar.Append(menu, menu_info['title'])

        self.SetMenuBar(menu_bar)

        return menu_bar

    def __InitToolBar(self):
        toolbar: wx.ToolBar = self.CreateToolBar(wx.TB_FLAT | wx.TB_HORIZONTAL
                                                 | wx.TB_TEXT)
        for menu in GlobalVars.MENUS:
            if menu['show_on_screen']:
                for item in menu['menu_items']:
                    if item['show_on_screen'] and 'toolbartool' in item and item[
                            'toolbartool']:
                        if 'icon' in item and item['icon']:
                            icon_bmp = Util.GetIcon(
                                item['icon'],
                                GlobalVars.ICON_SETTING['toolbar_icon'])
                        label_text: str = item['property']['text']
                        label: str = ''
                        help_string = item['property']['helpString']
                        pos = label_text.find('CTRL')
                        if ~pos:
                            label = label_text[:pos:]
                            shortcut_key = label_text[pos::]
                            pos = shortcut_key.find('&')
                            shortcut_key = shortcut_key[:pos:] + shortcut_key[
                                pos + 1::]
                            help_string += '(' + shortcut_key + ')'
                        toolbar.AddTool(item['property']['id'], label,
                                        icon_bmp, wx.NullBitmap,
                                        wx.ITEM_NORMAL, help_string,
                                        help_string)
                toolbar.AddSeparator()

        toolbar.Realize()

        return toolbar

    def __InitCapturePanel(self):
        self.__capture_bitmap = wx.StaticBitmap(self)
        return self.__capture_bitmap

    def __InitRecognizeResPanel(self):
        self.__result_text = wx.TextCtrl(self,
                                         style=wx.TE_MULTILINE | wx.TE_LEFT)
        self.__result_text.Bind(wx.EVT_CHAR, self.__OnChar)
        return self.__result_text

    def __InitStatusBar(self):
        status_bar: wx.StatusBar = self.CreateStatusBar()
        status_bar.SetFieldsCount(2, [-1, 250])

        return status_bar

    def __OnNew(self, _evt):
        if _evt:
            self.SetSize(self.DEFAULT_WINDOW_SIZE)
        self.__capture_bitmap.SetBitmap(wx.NullBitmap)
        self.__result_bitmap = None
        self.__raw_bitmap = None
        self.__result_text.SetValue('')
        if self.__tuning_panel:
            self.__tuning_panel.SetDefault()
        self.Layout()
        self.Refresh()
        return

    def __OnOpenImage(self, _evt: wx.Event):
        path = self.__OpenDialog(_evt.GetId())
        if path:
            open_image = wx.Bitmap(path)
            try:
                self.__raw_bitmap = wx.Bitmap(open_image)
                self.__result_bitmap = self.__raw_bitmap
                self.SetCaptureBitmap(open_image)
            except:
                wx.MessageBox(u'打开图片文件失败！',
                              u'错误',
                              style=wx.OK | wx.CENTER | wx.ICON_ERROR)
        return

    def __OnSaveCapture(self, _evt: wx.Event):
        id = _evt.GetId()
        if self.__result_bitmap and self.__result_bitmap != wx.NullBitmap:
            path: str = self.__OpenDialog(id)
            if path:
                bitmap_type = path[-3::].lower()
                if bitmap_type not in GlobalVars.BITMAP_TYPE_MAP:
                    bitmap_type = 'jpg'
                    path += '.' + bitmap_type
            self.__result_bitmap.SaveFile(
                path, GlobalVars.BITMAP_TYPE_MAP[bitmap_type])
        else:
            item = Util.GetMenuById(id)
            wx.MessageBox(u'没有可保存的截图！', item['property']['helpString'],
                          wx.OK | wx.CENTER | wx.ICON_INFORMATION)

        return

    def __OnSaveText(self, _evt: wx.Event):
        id = _evt.GetId()
        path = self.__OpenDialog(id)
        if path:
            self.__result_text.SaveFile(path)
        return

    def __OpenDialog(self, _id):
        item = Util.GetMenuById(_id)
        dialog = wx.FileDialog(self, **item['dialog'])
        res = dialog.ShowModal()
        path = None
        if res == wx.ID_OK:
            path = dialog.GetPath()

        dialog.Destroy()
        return path

    def OnExit(self, _evt):
        do_exit = None
        
        if wx.MessageBox(u'是否退出程序？', 
                         u'退出提示', 
                         wx.YES_NO 
                         | wx.NO_DEFAULT 
                         | wx.CENTER 
                         | wx.ICON_QUESTION, 
                         self) == wx.YES:
            if self.__taskbar_icon:
                self.__taskbar_icon.Destroy()
            wx.Exit()
            do_exit = True
        else:
            do_exit = False
        return do_exit

    def OnCapture(self, _evt):
        self.__OnNew(None)

        def GetDisplayRects(display: wx.Display):
            mode: wx.VideoMode = display.GetCurrentMode()
            show_rect: wx.Rect = display.GetGeometry()
            show_x, show_y = show_rect.GetPosition()
            real_w, real_h = mode.w, mode.h
            if show_x:
                real_x = real_w * (abs(show_x) / show_x)
            else:
                real_x = 0
            if show_y:
                real_y = real_h * (abs(show_y) / show_y)
            else:
                real_y = 0
            cap_rect: wx.Rect = wx.Rect(real_x, real_y, real_w, real_h)
            return show_rect, cap_rect

        if self.__setting['capture_all_display'] == GlobalVars.CAPTURE_ALL_DISPLAY:
            show_rects: list[wx.Rect] = []
            cap_rects: list[wx.Rect] = []
            for i in range(wx.Display.GetCount()):
                display = wx.Display(i)
                show_rect, cap_rect = GetDisplayRects(display)
                show_rects.append(show_rect)
                cap_rects.append(cap_rect)

            def SumRects(rects: list[wx.Rect]):
                if rects:
                    res_rect = wx.Rect(0, 0, 0, 0)
                    for rect in rects:
                        res_rect += rect
                    return res_rect
                else:
                    return None

            show_sum_rect: wx.Rect = SumRects(show_rects)
            cap_sum_rect: wx.Rect = SumRects(cap_rects)
        else:
            display = wx.Display(self)
            show_sum_rect, cap_sum_rect = GetDisplayRects(display)

        '''For debugging'''
        # display_pos_x_min = 0
        # display_pos_y_min = 0
        # display_sum_width, display_sum_heigth = wx.GetDisplaySize()
        '''For debugging'''

        if self.__tuning_panel:
            self.__tuning_panel.Hide()
        self.Hide()
        if not self.IsShown():
            wx.MilliSleep(250)
            screen_bitmap = self.__GetScreenBmp(
                cap_sum_rect.GetSize(), cap_sum_rect.GetPosition())
            wx.Bitmap.Rescale(screen_bitmap, show_sum_rect.GetSize())
            self.__grab_frame: GrabFrame = GrabFrame(
                self, screen_bitmap, show_sum_rect.GetSize(),
                show_sum_rect.GetPosition())
            self.__grab_frame.Bind(wx.EVT_SHOW, self.__OnGrabFrameHidden)
            # TODO: 转移至GramFrame类中绑定
            self.__grab_frame.Bind(wx.EVT_CHAR, self.__OnChar)
            self.__grab_frame.Bind(wx.EVT_RIGHT_UP, self.__OnKeyEsc)
        return

    def __OnRecognize(self, _evt):
        if self.__result_bitmap:
            self.__TextRecognize(self.__result_bitmap)
        return

    def OnSetting(self, _evt):
        self.__setting_dialog = SettingDialog(self, self.__setting, (400, -1))
        if self.__setting_dialog.ShowModal() == wx.ID_OK:
            self.__setting = self.__setting_dialog.GetSetting()
            self.ApplySetting()
        self.__setting_dialog.Close()

        return

    def __OnHelp(self, _evt):

        return

    def __OnAbout(self, _evt):

        return

    def __OnChar(self, _evt: wx.KeyEvent):
        key_code = _evt.GetKeyCode()
        if key_code in self.__keymap:
            _evt.SetId(self.__keymap[key_code]['id'])
            self.__keymap[key_code]['handler'](_evt)
        else:
            _evt.Skip()
        return

    def __GetScreenBmp(self, _display_size: wx.Size, _dispaly_pos: wx.Point):
        bmp: wx.Bitmap = wx.Bitmap(_display_size.x, _display_size.y)
        dc = wx.ScreenDC()
        memdc = wx.MemoryDC()
        memdc.SelectObject(bmp)
        memdc.Blit(0, 0, _display_size.x, _display_size.y, dc, _dispaly_pos.x,
                   _dispaly_pos.y)
        memdc.SelectObject(wx.NullBitmap)
        return bmp

    def __TextRecognize(self, _grab_bitmap: wx.Bitmap):
        temp_img = BytesIO()
        image: wx.Image = _grab_bitmap.ConvertToImage()
        image.SaveFile(temp_img, wx.BITMAP_TYPE_JPEG)

        from GlobalVars import RECONIZE_METHOD
        if self.__reconize_method is None:
            self.__reconize_method = RECONIZE_METHOD[
                self.__reconize_type].copy()
        if 'language_type' in self.__setting:
            self.__reconize_method['_args']['_options'][
                'language_type'] = self.__setting['language_type']

        from wx.lib.agw.pyprogress import PyProgress
        pro_dlg = PyProgress(self, title=u'识别中', agwStyle= wx.PD_APP_MODAL | wx.PD_ELAPSED_TIME)
        pro_dlg.CenterOnParent()
        self.__reconize_method['_args'].update({'_img': temp_img.getvalue()})
        text_reco = TextReconizeThread(**self.__reconize_method)
        text_reco.start()
        while text_reco.is_alive():
            pro_dlg.UpdatePulse()
            wx.MilliSleep(100)
        pro_dlg.Destroy()
        self.Raise()
        self.__result_text.ChangeValue(text_reco.Result())
        self.__status_bar.SetStatusText(u'识别完成！', 0)
        wx.TheClipboard.SetData(wx.TextDataObject(self.__result_text.GetValue()))

        return

    def ProcessGrabBitmap(self, _grab_bitmap: wx.Bitmap):
        self.Show()
        if self.__tuning_panel:
            self.__tuning_panel.Show()
        if _grab_bitmap:
            self.__raw_bitmap = wx.Bitmap(_grab_bitmap)
            self.__result_bitmap = self.__raw_bitmap
            self.SetCaptureBitmap(_grab_bitmap)
        self.__grab_frame.Close()
        return

    def SetCaptureBitmap(self, _bitmap: wx.Bitmap):
        if _bitmap or _bitmap != wx.NullBitmap:
            ctrl_width, ctrl_height = self.__capture_bitmap.GetSize()
            bitmap_width, bitmap_height = _bitmap.GetSize()
            ctrl_ratio = ctrl_width / ctrl_height
            bitmap_ratio = bitmap_width / bitmap_height
            if bitmap_ratio >= ctrl_ratio:
                target_width = ctrl_width
                target_height = target_width / bitmap_width * bitmap_height
            else:
                target_height = ctrl_height
                target_width = ctrl_height / bitmap_height * bitmap_width
            wx.Bitmap.Rescale(_bitmap, (target_width, target_height))
            self.__capture_bitmap.SetBitmap(_bitmap)
            self.Layout()
        return

    def __OnResize(self, _evt: wx.SizeEvent):
        frame_width, frame_height = _evt.GetSize()
        self.__capture_bitmap.SetSize(
            frame_width / 2,
            self.__capture_bitmap.GetSize().GetHeight())
        if self.__result_bitmap:
            self.SetCaptureBitmap(wx.Bitmap(self.__result_bitmap))
        self.__OnMoving(None)

        _evt.Skip()
        return

    def __OnGrabFrameHidden(self, _evt: wx.ShowEvent):
        if not _evt.IsShown() and self.__result_bitmap:
            self.__TextRecognize(self.__result_bitmap)
        return

    def __OnKeyEsc(self, _evt):
        self.__grab_frame.Hide()
        if not self.__grab_frame.IsShown():
            self.Show()
            if self.__tuning_panel:
                self.__tuning_panel.Show(
                    self.__tuning_panel.GetTool().IsToggled())
            self.__grab_frame.Close()
        return

    def SetText(self, _text: str):
        self.__result_text.SetValue(_text)
        return

    def SetStatusText(self, _text: str):
        self.__status_bar.SetStatusText(_text, 0)
        return


    def __OnClose(self, _evt: wx.CloseEvent):
        if self.__setting['close_setting'] == GlobalVars.CLOSE_USER_SELECT:
            from CloseDialog import CloseDialog
            close_dialog = CloseDialog(self, self.__setting)
            res = close_dialog.ShowModal()
            if res == wx.ID_OK:
                close_setting = close_dialog.GetSetting()
                if not close_setting['allowed_prompt']:
                    self.__setting['close_setting'] = close_setting['close_setting']
                setting = close_setting['close_setting']
            else:
                _evt.Veto()
                return
        else:
            setting = self.__setting['close_setting']
        self.ApplySetting()

        if setting == GlobalVars.CLOSE_TO_TASKBAR:
            self.Iconize(True)
            self.Hide()
            _evt.Veto()
        else:            
            if self.OnExit(None):
                _evt.Skip()
            else:
                _evt.Veto()
            return

    def __OnIconize(self, _evt: wx.IconizeEvent):
        if self.__setting['minimize_to_taskbar']:
            self.Show(not self.IsShown())
        _evt.Skip()
        return

    def ApplySetting(self):
        Setting.SaveSettingToFile(self.__setting, self.__setting_file)
        self.__SetStatusBarText()
        self.__SetHotkey()
        return

    def __SetStatusBarText(self):
        status_text = u'当前识别语言：'
        for key, val in GlobalVars.RECONIZE_LANGUAGE.items():
            if val == self.__setting['language_type']:
                status_text += key
                break
        self.__status_bar.SetStatusText(status_text, 1)
        return

    def __SetHotkey(self):
        if 'hotkey' in self.__setting and self.__setting['hotkey']:
            self.RegisterHotKey(0, wx.MOD_CONTROL | wx.MOD_ALT,
                                ord(self.__setting['hotkey']))
            self.Bind(wx.EVT_HOTKEY, self.__OnHotkey, id=0)
        else:
            self.UnregisterHotKey(0)
            self.Unbind(wx.EVT_HOTKEY, id=0)
            pass
        return

    def __OnHotkey(self, _evt):
        self.OnCapture(None)
        if self.IsIconized():
            self.Iconize(False)

        self.Raise()
        return

    def __OnImageEnhance(self, _evt: wx.CommandEvent):
        tool: wx.ToolBarToolBase = self.__toolbar.FindById(_evt.GetId())
        if self.__tuning_panel is None:
            self.__tuning_panel = ImageTuningPanel(self, tool)
            pos: wx.Point = self.GetPosition()
            panel_size = self.__tuning_panel.GetSize()
            self.__tuning_panel.SetPosition(
                wx.Point(pos.x - panel_size.GetWidth(), pos.y))
        else:
            self.__tuning_panel.Show(not self.__tuning_panel.IsShown())
            tool.Toggle(self.__tuning_panel.IsShown())
        return

    def GetRawBitmap(self) -> wx.Bitmap:
        return self.__raw_bitmap

    def SetResultBitmap(self, _bitmap: wx.Bitmap):
        self.__result_bitmap = _bitmap
        return

    def GetResultBitmap(self) -> wx.Bitmap:
        return self.__result_bitmap

    def __OnMoving(self, _evt):
        if self.__tuning_panel:
            frame_pos: wx.Point = self.GetPosition()
            tuning_size: wx.Size = self.__tuning_panel.GetSize()
            self.__tuning_panel.SetPosition(
                wx.Point(frame_pos.x - tuning_size.GetWidth(), frame_pos.y))
        if _evt:
            _evt.Skip()
        return


class MainframeIcon(TaskBarIcon):
    ID_MINIMIZE_TO_TASKBAR = 900
    __main_menu : dict = GlobalVars.MENUS
    __icon_menu : dict ={
        GlobalVars.ID_SHOW: None,
        ID_MINIMIZE_TO_TASKBAR: None,
        GlobalVars.ID_CAPTURE: None,
        GlobalVars.ID_SETTING: None,
        wx.ID_SEPARATOR: None,
        GlobalVars.ID_EXIT:None
    }
    def __init__(self, _main_frame: Mainframe, _setting):
        super().__init__()
        self.__main_frame = _main_frame
        self.__setting = _setting
        self.__handler_map = {
            '__OnShow': self.__OnShow,
            '__OnCheckMinimzieToTaskBar': self.__OnCheckMinimzieToTaskBar,
            '__OnExit': self.__main_frame.OnExit,
            '__OnCapture': self.__OnCapture,
            '__OnSetting': self.__OnSetting
        }
        self.SetIcon(self.__main_frame.GetIcon(), self.__main_frame.GetTitle())
        self.__InitMenu()
        
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DCLICK,
                  self.__OnTaskbarLeftDoubleClick)
        self.Bind(wx.adv.EVT_TASKBAR_RIGHT_UP, self.__OnTaskbarRightUp)

        return

    def GetPopupMenu(self):
        return self.__menu

    def __InitMenu(self):
        self.__menu = wx.Menu()
        for main_menu in self.__main_menu:
            for item in main_menu['menu_items']:
                if item['property']['id'] in self.__icon_menu and \
                   self.__icon_menu[item['property']['id']] is None:
                    self.__icon_menu[item['property']['id']] = item
        self.__icon_menu[self.ID_MINIMIZE_TO_TASKBAR] = {
                'property':
                {
                    'id': self.ID_MINIMIZE_TO_TASKBAR,
                    'text': u'最小化到系统托盘',
                    'helpString': u'最小化到系统托盘',
                    'kind': wx.ITEM_CHECK
                },
                'show_on_screen': True,
                'handler': '__OnCheckMinimzieToTaskBar'
            }
        for key, value in  self.__icon_menu.items():
            menu_item = wx.MenuItem(**value['property'])
            self.__menu.Append(menu_item)
            if 'handler' in value and value['handler']:
                handler = self.__handler_map[value['handler']]
                self.Bind(wx.EVT_MENU, handler, id=key)
            if key == self.ID_MINIMIZE_TO_TASKBAR:
                menu_item.Check(self.__setting['minimize_to_taskbar'])        
        return

    def __OnTaskbarLeftDoubleClick(self, _evt):
        self.__main_frame.Iconize(not self.__main_frame.IsIconized())
        if not self.__main_frame.IsShown():
            self.__main_frame.Show(True)
            self.__main_frame.Raise()
        else:
            self.__main_frame.Show(False)

        return

    def __OnTaskbarRightUp(self, _evt):
        self.PopupMenu(self.__menu)
        return

    def __OnShow(self, _evt):
        self.__main_frame.Iconize(False)
        self.__main_frame.Show(True)
        return

    def __OnCapture(self, _evt):
        self.__OnShow(None)
        self.__main_frame.OnCapture(_evt)
        return

    def __OnSetting(self, _evt):
        self.__OnShow(None)
        self.__main_frame.OnSetting(_evt)
        return

    def __OnCheckMinimzieToTaskBar(self, _evt: wx.CommandEvent):
        menu_item: wx.MenuItem = self.__menu.FindItemById(_evt.GetId())
        self.__setting['minimize_to_taskbar'] = menu_item.IsChecked()
        self.__main_frame.ApplySetting()
        return