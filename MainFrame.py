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
    __clipboard: wx.Clipboard
    
    
    def __init__(self, title):
        self.DEFAULT_WINDOW_SIZE = wx.Size(wx.GetDisplaySize().GetWidth() * 0.5,
                                      wx.GetDisplaySize().GetHeight() * 0.5)
        super().__init__(None,
                         title=title,
                         size=self.DEFAULT_WINDOW_SIZE)
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

        self.__keymap = {
            wx.WXK_ESCAPE: {'handler': self.__OnKeyEsc, 'id': wx.ID_ANY}
        }
        self.__result_bitmap = None
        self.__clipboard = wx.Clipboard()
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
            if GlobalVars.MENUS.index(menu) < len(GlobalVars.MENUS) - 1:
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

    def __OnNew(self, _evt):
        self.SetSize(self.DEFAULT_WINDOW_SIZE)
        self.__capture_bitmap.SetBitmap(wx.NullBitmap)
        self.__result_bitmap = None
        self.__result_text.SetValue('')
        self.Layout()
        self.Refresh()
        return

    def __OnOpenImage(self, _evt: wx.Event):
        path = self.__OpenDialog(_evt.GetId())
        open_image = wx.Bitmap(path)
        self.__result_bitmap = wx.Bitmap(open_image)
        self.__SetCaptureBitmap(open_image)
        return

    def __OnSaveCapture(self, _evt: wx.Event):
        id = _evt.GetId()
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

    def __OnSaveText(self, _evt: wx.Event):
        id = _evt.GetId()
        path = self.__OpenDialog(id)
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

    def __OnExit(self, _evt):
        wx.Exit()
        return

    def __OnCapture(self, _evt):
        displays = []
        display_sum_width = 0
        display_sum_heigth = 0
        for i in range(wx.Display.GetCount()):
            display = wx.Display(i)
            displays.append(display)
            display_sum_width += display.Geometry[2]
            display_sum_heigth += display.Geometry[3]
            
        self.Hide()
        if not self.IsShown():
            wx.MilliSleep(250)
            screen_bitmap = self.__GetScreenBmp(wx.Size(display_sum_width, display_sum_heigth))
            self.__grab_frame: GrabFrame = GrabFrame(self, screen_bitmap, (display_sum_width, display_sum_heigth)) # wx.GetDisplaySize())
            self.__grab_frame.Bind(wx.EVT_SHOW, self.__OnGrabFrameHidden)
            self.__grab_frame.Bind(wx.EVT_CHAR, self.__OnChar)
        return

    def __OnRecognize(self, _evt):
        if self.__result_bitmap:
            self.__TextRecognize(self.__result_bitmap)
        return

    def __OnSetting(self, _evt):

        return

    def __OnHelp(self, _evt):

        return

    def __OnAbout(self, _evt):

        return

    def __OnChar(self, _evt: wx.KeyEvent):
        key_code = _evt.GetKeyCode()
        print('key_code', key_code)
        if key_code in self.__keymap:
            _evt.SetId(self.__keymap[key_code]['id'])
            self.__keymap[key_code]['handler'](_evt)
        else:
            _evt.Skip()
        return

    def __GetScreenBmp(self, _display_size : wx.Size):
        bmp: wx.Bitmap = wx.Bitmap(_display_size.x, _display_size.y)
        dc = wx.ScreenDC()
        memdc = wx.MemoryDC()
        memdc.SelectObject(bmp)
        memdc.Blit(0, 0, _display_size.x, _display_size.y, dc, 0, 0)
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
        self.Show()
        self.__result_bitmap = wx.Bitmap(_grab_bitmap)
        self.__grab_frame.Close()
        self.__CopyBitmapToClipboard(self.__result_bitmap)
        self.__capture_bitmap.SetScaleMode(wx.StaticBitmap.Scale_AspectFill)
        self.__SetCaptureBitmap(_grab_bitmap)
        return
    
    def __SetCaptureBitmap(self, _bitmap : wx.Bitmap):
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
    
    def __OnResize(self, _evt : wx.SizeEvent):
        frame_width, frame_height = _evt.GetSize()        
        self.__capture_bitmap.SetSize(frame_width / 2, 
                                self.__capture_bitmap.GetSize().GetHeight())
        if self.__result_bitmap:
            self.__SetCaptureBitmap(wx.Bitmap(self.__result_bitmap))

        _evt.Skip()
        return
    
    def __CopyBitmapToClipboard(self, _data : wx.Bitmap):
        self.__clipboard.SetData(wx.ImageDataObject(_data.ConvertToImage()))
        return
    
    def __OnGrabFrameHidden(self, _evt : wx.ShowEvent):
        if not _evt.IsShown():
            self.__TextRecognize(self.__result_bitmap)

    def __OnKeyEsc(self, evt):
        self.__grab_frame.Hide()
        if not self.__grab_frame.IsShown():
            self.__grab_frame.Close()
            self.Show()