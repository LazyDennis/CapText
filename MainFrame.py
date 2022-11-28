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
    __is_ext_set: bool
    
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
        self.__InitUi()

    def __InitUi(self):
        # self.SetBackgroundStyle(wx.BG_STYLE_SYSTEM)
        # self.SetForegroundColour('#FF0000')
        icon_bundle = wx.IconBundle()
        icon_bundle.AddIcon(wx.Icon(Util.GetIcon(
            'frame_icon_large', GlobalVars.ICON_SETTING['frame_icon_large'])))
        icon_bundle.AddIcon(wx.Icon(Util.GetIcon(
            'frame_icon_small', GlobalVars.ICON_SETTING['frame_icon_small'])))
        
        self.SetIcons(icon_bundle)
        self.__menu_bar = self.__InitMenu()
        self.__toolbar = self.__InitToolBar()
        self.__main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.__main_sizer.Add(self.__InitCapturePanel(), 1, wx.EXPAND)
        self.__main_sizer.Add(self.__InitRecognizeResPanel(), 1, wx.EXPAND)

        self.SetSizer(self.__main_sizer)
        self.__status_bar: wx.StatusBar = self.CreateStatusBar()
        
        # color = wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW)
        # self.__menu_bar.SetBackgroundColour(color)
        # self.__toolbar.SetBackgroundColour(color)
        # self.SetBackgroundColour(color)
        # self.__status_bar.SetBackgroundColour(color)

        self.Bind(wx.EVT_SIZE, self.__OnResize)        

    def __InitMenu(self):
        menu_bar = wx.MenuBar()

        for menu_info in GlobalVars.MENUS:
            menu = wx.Menu()
            for item in menu_info['menu_items']:
                menu_item = wx.MenuItem(**item['property'])
                if 'icon' in item and item['icon']:
                    menu_item.SetBitmap(
                        Util.GetIcon(item['icon'],
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
                        icon_bmp = Util.GetIcon(
                            item['icon'], GlobalVars.ICON_SETTING['toolbar_icon'])
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
        if path:
            open_image = wx.Bitmap(path)
            try:
                self.__result_bitmap = wx.Bitmap(open_image)
                self.__SetCaptureBitmap(open_image)
            except:
                wx.MessageBox(u'打开图片文件失败！', u'错误', style= wx.OK | wx.CENTER | wx.ICON_ERROR)
                # return
        return

    def __OnSaveCapture(self, _evt: wx.Event):
        id = _evt.GetId()
        # bitmap: wx.Bitmap = self.__capture_bitmap.GetBitmap()
        if self.__result_bitmap and self.__result_bitmap != wx.NullBitmap:
            path: str = self.__OpenDialog(id)
            if path:
                bitmap_type = path[-3::].lower()
                if bitmap_type not in GlobalVars.BITMAP_TYPE_MAP:
                    bitmap_type = 'jpg'
                    path += '.' + bitmap_type
            self.__result_bitmap.SaveFile(path, GlobalVars.BITMAP_TYPE_MAP[bitmap_type])
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

    def __OnExit(self, _evt):
        wx.Exit()
        return

    def __OnCapture(self, _evt):
        displays = []
        display_pos_x_min = 0
        display_pos_y_min = 0
        display_pos_x_max = 0
        display_pos_y_max = 0
        for i in range(wx.Display.GetCount()):
            display = wx.Display(i)
            displays.append(display)
            pos_x, pos_y, width, height = display.GetGeometry()
            display_pos_x_min = pos_x if pos_x < display_pos_x_min else display_pos_x_min
            display_pos_y_min = pos_y if pos_y < display_pos_y_min else display_pos_y_min
            pos_x += width
            pos_y += height
            display_pos_x_max = pos_x if pos_x > display_pos_x_max else display_pos_x_max
            display_pos_y_max = pos_y if pos_y > display_pos_y_max else display_pos_y_max
            
        display_sum_width = display_pos_x_max - display_pos_x_min
        display_sum_heigth = display_pos_y_max - display_pos_y_min
            
        self.Hide()
        if not self.IsShown():
            wx.MilliSleep(250)
            screen_bitmap = self.__GetScreenBmp(
                wx.Size(display_sum_width, display_sum_heigth),
                wx.Point(display_pos_x_min, display_pos_y_min))
            self.__grab_frame: GrabFrame = GrabFrame(
                self, screen_bitmap, 
                (display_sum_width, display_sum_heigth),
                (display_pos_x_min, display_pos_y_min))
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
        if key_code in self.__keymap:
            _evt.SetId(self.__keymap[key_code]['id'])
            self.__keymap[key_code]['handler'](_evt)
        else:
            _evt.Skip()
        return

    def __GetScreenBmp(self, _display_size : wx.Size, _dispaly_pos : wx.Point):
        bmp: wx.Bitmap = wx.Bitmap(_display_size.x, _display_size.y)
        dc = wx.ScreenDC()
        memdc = wx.MemoryDC()
        memdc.SelectObject(bmp)
        memdc.Blit(0, 0, _display_size.x, _display_size.y, dc, _dispaly_pos.x, _dispaly_pos.y)
        memdc.SelectObject(wx.NullBitmap)
        return bmp

    def __TextRecognize(self, _grab_bitmap: wx.Bitmap):
        temp_img = BytesIO()
        image: wx.Image = _grab_bitmap.ConvertToImage()
        image.SaveFile(temp_img, wx.BITMAP_TYPE_JPEG)
        
        from TextReconize import TextReconThread
        self.__text_reco = TextReconThread(temp_img, self)
        self.__text_reco.start()

        return

    def ProcessGrabBitmap(self, _grab_bitmap: wx.Bitmap):
        self.Show()
        if _grab_bitmap:
            self.__result_bitmap = wx.Bitmap(_grab_bitmap)
            # self.__CopyBitmapToClipboard(self.__result_bitmap)
            self.__SetCaptureBitmap(_grab_bitmap)
        self.__grab_frame.Close()
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
    
    # def __CopyBitmapToClipboard(self, _data : wx.Bitmap):
    #     self.__clipboard.SetData(wx.ImageDataObject(_data.ConvertToImage()))
    #     return
    
    def __OnGrabFrameHidden(self, _evt : wx.ShowEvent):
        if not _evt.IsShown() and self.__result_bitmap:
            self.__TextRecognize(self.__result_bitmap)
        return

    def __OnKeyEsc(self, evt):
        self.__grab_frame.Hide()
        if not self.__grab_frame.IsShown():
            self.Show()
            self.__grab_frame.Close()
        return
    
    def SetText(self, _text: str):
        self.__result_text.SetValue(_text)
        return