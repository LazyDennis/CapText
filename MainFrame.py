import wx
from GrabFrame import GrabFrame
from aip import AipOcr
from api import APP_ID, API_KEY, SECRET_KEY
from io import BytesIO
import Util

import GlobalVars


class Mainframe(wx.Frame):
    __main_sizer: wx.BoxSizer    
    __grab_frame: GrabFrame
    __capture_bitmap: wx.StaticBitmap
    __result_bitmap : wx.Bitmap
    __result_text: wx.TextCtrl
    __handler_map: dict
    __keymap: dict
    
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
            '__OnAbout': self.__OnAbout
        }

        self.__keymap = {}
        self.__result_bitmap = None
        self.__InitUi()

    def __InitUi(self):
        self.SetBackgroundStyle(wx.BG_STYLE_SYSTEM)
        self.SetForegroundColour('#FF0000')
        
        self.__menu_bar = self.__InitMenu()
        self.__toolbar = self.__InitToolBar()
        self.__main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.__main_sizer.Add(self.__InitCapturePanel(), 1, wx.EXPAND)
        self.__main_sizer.Add(self.__InitRecognizeResPanel(), 1, wx.EXPAND)

        self.SetSizer(self.__main_sizer)
        self.CreateStatusBar()

        self.Bind(wx.EVT_SIZE, self.__OnResize)        

    def __InitMenu(self):
        menu_bar = wx.MenuBar()

        for menu_info in GlobalVars.MENUS:
            menu = wx.Menu()
            for item in menu_info['menu_items']:
                menu_item = wx.MenuItem(**item['property'])
                if 'icon' in item and item['icon']:
                    icon_path = GlobalVars.ICON_PATH + item['icon']
                    menu_item.SetBitmap(
                        Util.GetIcon(icon_path,
                                     GlobalVars.ICON_SETTING['menu_icon']))
                menu.Append(menu_item)
                if 'handler' in item and item['handler']:
                    handler = self.__handler_map[item['handler']]
                    self.Bind(wx.EVT_MENU, handler, id=item['property']['id'])
                    lastchar = item['property']['text'][-1::]
                    if ord(lastchar) >= ord('A') and ord(lastchar) <= ord('Z'):
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
            for item in menu['menu_items']:
                if 'toolbartool' in item and item['toolbartool']:
                    if 'icon' in item and item['icon']:
                        icon_path = GlobalVars.ICON_PATH + item['icon']
                        icon_bmp = Util.GetIcon(
                            icon_path, GlobalVars.ICON_SETTING['toolbar_icon'])
                    label_text: str = item['property']['text']
                    label: str = ''
                    help_string = item['property']['helpString']
                    pos = label_text.find('CTRL')
                    if ~pos:
                        label = label_text[:pos:]
                        shortcut_key = label_text[pos::]
                        pos = shortcut_key.find('&')
                        shortcut_key = shortcut_key[:pos:] + shortcut_key[pos +
                                                                          1::]
                        help_string += '(' + shortcut_key + ')'
                    toolbar.AddTool(item['property']['id'], label, icon_bmp,
                                    wx.NullBitmap, wx.ITEM_NORMAL, help_string,
                                    help_string)
            toolbar.AddSeparator()

        toolbar.Realize()

        return toolbar

    def __InitCapturePanel(self) -> wx.BoxSizer:
        self.__capture_bitmap = wx.StaticBitmap(self)
        return self.__capture_bitmap

    def __InitRecognizeResPanel(self) -> wx.BoxSizer:
        self.__result_text = wx.TextCtrl(self,
                                         style=wx.TE_MULTILINE | wx.TE_LEFT)
        self.__result_text.Bind(wx.EVT_CHAR, self.__OnChar)
        return self.__result_text

    def __OnNew(self, evt):
        self.__capture_bitmap.SetBitmap(wx.NullBitmap)
        self.__result_text.SetValue('')
        self.Layout()
        return

    def __OnOpenImage(self, evt: wx.Event):
        path = self.__OpenDialog(evt.GetId())
        open_image = wx.Bitmap(path)
        self.__result_bitmap = wx.Bitmap(open_image)
        self.__SetCaptureBitmap(open_image)
        # self.Layout()
        return

    def __OnSaveCapture(self, evt: wx.Event):
        id = evt.GetId()
        path: str = self.__OpenDialog(id)
        bitmap_type = path[-3::].lower()
        if bitmap_type not in GlobalVars.BITMAP_TYPE_MAP:
            bitmap_type = 'jpg'
            path += '.' + bitmap_type
        bitmap: wx.Bitmap = self.__capture_bitmap.GetBitmap()
        if bitmap and bitmap != wx.NullBitmap:
            bitmap.SaveFile(path, GlobalVars.BITMAP_TYPE_MAP[bitmap_type])
        else:
            item = Util.GetMenuById(id)
            wx.MessageBox(u'没有可保存的截图！', item['property']['helpString'],
                        wx.OK | wx.CENTER | wx.ICON_INFORMATION)

        return

    def __OnSaveText(self, evt: wx.Event):
        id = evt.GetId()
        path = self.__OpenDialog(id)
        self.__result_text.SaveFile(path)
        return

    def __OpenDialog(self, id):
        item = Util.GetMenuById(id)
        dialog = wx.FileDialog(self, **item['dialog'])
        res = dialog.ShowModal()
        path = None
        if res == wx.ID_OK:
            path = dialog.GetPath()

        dialog.Destroy()
        return path

    def __OnExit(self, evt):
        self.Destroy()
        return

    def __OnCapture(self, evt):
        self.Hide()
        if not self.IsShown():
            wx.MilliSleep(250)
            screen_bitmap = self.__GetScreenBmp()
            self.__grab_frame: GrabFrame = GrabFrame(self, screen_bitmap)
        return

    def __OnRecognize(self, evt):
        self.__TextRecognize(self.__result_bitmap)
        return

    def __OnSetting(self, evt):

        return

    def __OnHelp(self, evt):

        return

    def __OnAbout(self, evt):

        return

    def __OnChar(self, evt: wx.KeyEvent):
        key_code = evt.GetKeyCode()
        if key_code in self.__keymap:
            evt.SetId(self.__keymap[key_code]['id'])
            self.__keymap[key_code]['handler'](evt)
        else:
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
        self.__result_bitmap = wx.Bitmap(_grab_bitmap)
        self.__capture_bitmap.SetScaleMode(wx.StaticBitmap.Scale_AspectFill)
        self.__SetCaptureBitmap(_grab_bitmap)
        wx.MilliSleep(250)
        self.__TextRecognize(self.__result_bitmap)
        return
    
    def __SetCaptureBitmap(self, bitmap : wx.Bitmap):
        ctrl_width, ctrl_height = self.__capture_bitmap.GetSize()
        bitmap_width, bitmap_height = bitmap.GetSize()
        ctrl_ratio = ctrl_width / ctrl_height
        bitmap_ratio = bitmap_width / bitmap_height
        if bitmap_ratio >= ctrl_ratio:
            target_width = ctrl_width
            target_height = target_width / bitmap_width * bitmap_height
        else:
            target_height = ctrl_height
            target_width = ctrl_height / bitmap_height * bitmap_width
        print('ctrl size: ', (ctrl_width, ctrl_height), 'bitmap size: ', (bitmap_width, bitmap_height), 'target size: ', (target_width, target_height))
        print(bitmap is self.__result_bitmap)
        wx.Bitmap.Rescale(bitmap, (target_width, target_height))
        self.__capture_bitmap.SetBitmap(bitmap)
        self.Layout()
        return
    
    def __OnResize(self, evt : wx.SizeEvent):
        frame_width, frame_height = evt.GetSize()        
        self.__capture_bitmap.SetSize(frame_width / 2, 
                                self.__capture_bitmap.GetSize().GetHeight())
        if self.__result_bitmap:
            self.__SetCaptureBitmap(wx.Bitmap(self.__result_bitmap))

        evt.Skip()
        return
