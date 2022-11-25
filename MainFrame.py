import wx
from GrabFrame import GrabFrame
from aip import AipOcr
from api import APP_ID, API_KEY, SECRET_KEY
from io import BytesIO
import Util

import GlobalVars


class Mainframe(wx.Frame):
    __main_sizer: wx.BoxSizer
    # __capture_panel: wx.Panel
    # __text_panel: wx.Panel
    # __capture_button : wx.Button
    __grab_frame: GrabFrame
    __capture_bitmap: wx.StaticBitmap
    __result_text: wx.TextCtrl
    # __result_bitmap : wx.Bitmap

    def __init__(self, title):
        super().__init__(None,
                         title=title,
                         size=wx.Size(wx.GetDisplaySize().GetWidth() * 0.5,
                                      wx.GetDisplaySize().GetHeight() * 0.5))
        self.__handler_map = {
            '__OnNew': self.__OnNew,
            '__OnOpenImage': self.__OnOpenImage,
            '__OnSaveCapture': self.__OnSaveCapture,
            '__OnSaveText': self.__OnSaveText,
            '__OnExit': self.__OnExit,
            '__OnCapture': self.__OnCapture,
            '__OnRecognize': self.__OnRecognize,
            '__OnSetting': self.__OnSetting,
            '__OnHelp': self.__OnHelp,
            '__OnAbout': self.__OnAbout}

        self.__keymap = {}

        self.__InitUi()

        # self.__result_text.Bind(wx.EVT_KEY_DOWN, self.__OnKeyDown)
        self.__result_text.Bind(wx.EVT_CHAR, self.__OnChar)

        # self.grab_bitmap : wx.Bitmap = None
        # self.__result_bitmap: wx.Bitmap = None

    def __InitUi(self):
        self.__menu_bar = self.__InitMenu()
        self.__toolbar = self.__InitToolBar()
        self.__main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # upper_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # downer_sizer = wx.BoxSizer(wx.VERTICAL)

        self.__main_sizer.Add(self.__InitCapturePanel(), 1, wx.EXPAND)
        self.__main_sizer.Add(self.__InitRecognizeResPanel(), 1, wx.EXPAND)

        # downer_sizer.Add(self.__InitCaptureButton(), 0, wx.ALIGN_LEFT | wx.ALL, 10)
        # downer_sizer.Add(self.__InitRecognizeButton(), 0, wx.ALIGN_LEFT | wx.ALL, 10)

        # self.__main_sizer.Add(upper_sizer, 1, wx.EXPAND)
        # self.__main_sizer.Add(downer_sizer, 0, wx.EXPAND)

        self.SetSizer(self.__main_sizer)

        self.CreateStatusBar()

    def __InitMenu(self):
        menu_bar = wx.MenuBar()

        for menu_info in GlobalVars.MENUS:
            menu = wx.Menu()
            for item in menu_info['menu_items']:
                menu_item = wx.MenuItem(**item['property'])
                if 'icon' in item and item['icon']:
                    icon_path = GlobalVars.ICON_PATH + item['icon']
                    menu_item.SetBitmap(Util.GetIcon(
                                icon_path, GlobalVars.ICON_SETTING['menu_icon']))
                menu.Append(menu_item)
                if 'handler' in item and item['handler']:
                    handler = self.__handler_map[item['handler']]
                    self.Bind(wx.EVT_MENU, handler, id=item['property']['id'])
                    lastchar = item['property']['text'][-1::]
                    if ord(lastchar) >= ord('A') and ord(lastchar) <= ord('Z'):
                        self.__keymap[ord(lastchar) - ord('A') + 1] = handler
            menu_bar.Append(menu, menu_info['title'])
        # print(self.__handler_map)
        self.SetMenuBar(menu_bar)

        # self.Bind(wx.EVT_MENU, self.__OnNew, id=100)
        # self.Bind(wx.EVT_MENU, self.__OnOpenImage, id=101)
        # self.Bind(wx.EVT_MENU, self.__OnSaveCapture, id=102)
        # self.Bind(wx.EVT_MENU, self.__OnSaveText, id=103)
        # self.Bind(wx.EVT_MENU, self.__OnExit, id=199)
        # self.Bind(wx.EVT_MENU, self.__OnCapture, id=200)
        # self.Bind(wx.EVT_MENU, self.__OnRecognize, id=201)
        # self.Bind(wx.EVT_MENU, self.__OnSetting, id=210)
        # self.Bind(wx.EVT_MENU, self.__OnHelp, id=300)
        # self.Bind(wx.EVT_MENU, self.__OnAbout, id=301)
        return menu_bar

    def __InitToolBar(self):
        toolbar : wx.ToolBar = self.CreateToolBar(wx.TB_FLAT | wx.TB_HORIZONTAL | wx.TB_TEXT)
        for menu in GlobalVars.MENUS:
            for item in menu['menu_items']:
                if 'toolbartool' in item and item['toolbartool']:
                    if 'icon' in item and item['icon']:
                        icon_path = GlobalVars.ICON_PATH + item['icon']
                        icon_bmp = Util.GetIcon(
                                    icon_path, GlobalVars.ICON_SETTING['toolbar_icon'])
                    label_text: str = item['property']['text']
                    label : str = ''
                    help_string = item['property']['helpString']
                    pos = label_text.find('CTRL')
                    if ~pos :
                        label = label_text[:pos:]
                        shortcut_key = label_text[pos::]
                        pos = shortcut_key.find('&')
                        shortcut_key = shortcut_key[:pos:] + shortcut_key[pos + 1::]
                        help_string += '(' + shortcut_key + ')'
                    toolbar.AddTool(
                        item['property']['id'],
                        label,
                        icon_bmp,
                        wx.NullBitmap,
                        wx.ITEM_NORMAL,
                        help_string,
                        help_string
                    )
            toolbar.AddSeparator()

        toolbar.Realize()

        return toolbar

    def __InitCapturePanel(self) -> wx.BoxSizer:
        # sizer = wx.BoxSizer(wx.HORIZONTAL)
        # self.__capture_panel = wx.Panel(self, wx.ID_ANY, style=wx.TAB_TRAVERSAL | wx.NO_BORDER)
        # panel_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.__capture_bitmap = wx.StaticBitmap(self)
        # self.__capture_bitmap.SetScaleMode(wx.StaticBitmap.Scale_AspectFit)
        # panel_sizer.Add(self.__capture_bitmap, 1, wx.EXPAND)
        # self.__capture_panel.SetSizer(panel_sizer)

        # sizer.Add(self.__capture_panel, 1, wx.EXPAND)

        return self.__capture_bitmap

    def __InitRecognizeResPanel(self) -> wx.BoxSizer:
        # sizer = wx.BoxSizer(wx.HORIZONTAL)
        # self.__text_panel = wx.Panel(self, wx.ID_ANY, style=wx.TAB_TRAVERSAL | wx.NO_BORDER)
        # panel_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.__result_text = wx.TextCtrl(
            self, style=wx.TE_MULTILINE | wx.TE_LEFT)
        # panel_sizer.Add(self.__result_text, 1, wx.EXPAND)
        # self.__text_panel.SetSizer(panel_sizer)

        # sizer.Add(self.__text_panel, 1, wx.EXPAND)

        return self.__result_text

    # def __InitCaptureButton(self) -> wx.BoxSizer:
    #     sizer = wx.BoxSizer(wx.HORIZONTAL)
    #     self.__capture_button = wx.Button(self, wx.ID_ANY, u'截图')
    #     sizer.Add(self.__capture_button, 0, wx.EXPAND)
    #     self.__capture_button.Bind(wx.EVT_BUTTON, self.__OnClick)
    #     return sizer

    # def __InitRecognizeButton(self) -> wx.BoxSizer:
    #     sizer = wx.BoxSizer(wx.HORIZONTAL)
    #     self.__recognize_button = wx.Button(self, wx.ID_ANY, u'识别')
    #     sizer.Add(self.__recognize_button, 0, wx.EXPAND)
    #     self.__recognize_button.Bind(wx.EVT_BUTTON, self.__OnRecognize)
    #     return sizer

    def __OnNew(self, evt):
        self.__capture_bitmap.SetBitmap(wx.NullBitmap)
        self.__result_text.SetValue('')
        return

    def __OnOpenImage(self, evt):
        dialog = wx.FileDialog(self)
        return

    def __OnSaveCapture(self, evt):

        return

    def __OnSaveText(self, evt):

        return

    def __OpenDialog(self, evt):

        return

    def __OnExit(self, evt):
        self.Destroy()
        # exit(0)
        return

    def __OnCapture(self, evt):
        self.Hide()
        if not self.IsShown():
            # self.grab_bitmap = self.__GetScreenBmp()
            # wx.Sleep(1)
            wx.MilliSleep(250)
            screen_bitmap = self.__GetScreenBmp()
            self.__grab_frame: GrabFrame = GrabFrame(self, screen_bitmap)
        return

    def __OnRecognize(self, evt):
        self.__TextRecognize(self.__capture_bitmap.GetBitmap())
        return

    def __OnSetting(self, evt):

        return

    def __OnHelp(self, evt):

        return

    def __OnAbout(self, evt):

        return

    # def __OnKeyDown(self, evt: wx.KeyEvent):
    #     print('key down:', evt.GetKeyCode())
    #     evt.Skip()
    #     return

    def __OnChar(self, evt: wx.KeyEvent):
        self.__keymap[evt.GetKeyCode()](evt)
        evt.Skip()
        return

    def __GetScreenBmp(self):
        s: wx.Size = wx.GetDisplaySize()
        bmp: wx.Bitmap = wx.Bitmap(s.x, s.y)
        dc = wx.ScreenDC()
        memdc = wx.MemoryDC()
        memdc.SelectObject(bmp)
        memdc.Blit(0, 0, s.x, s.y, dc, 0, 0)
        memdc.SelectObject(wx.NullBitmap)
        return bmp

    def __TextRecognize(self, _grab_bitmap: wx.Bitmap):
        temp_img = BytesIO()
        image: wx.Image = _grab_bitmap.ConvertToImage()
        image.SaveFile(temp_img, wx.BITMAP_TYPE_JPEG)
        client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
        options = {'language_type': 'CHN_ENG', 'paragraph': True}
        result = client.basicGeneral(temp_img.getvalue(), options)
        print(result)
        text = ''
        for res in result['words_result']:
            text += res['words']
            text += '\n'
        self.__result_text.SetValue(text)
        return

    def ProcessGrabBitmap(self, _grab_bitmap: wx.Bitmap):
        self.__grab_frame.Destroy()
        self.__capture_bitmap.SetScaleMode(wx.StaticBitmap.Scale_AspectFit)
        self.__capture_bitmap.SetBitmap(_grab_bitmap)
        self.Layout()
        self.Refresh()
        # wx.Sleep(0.5)
        self.__TextRecognize(_grab_bitmap)
        # self.__result_bitmap = _grab_bitmap
        return
