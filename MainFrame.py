import wx
from GrabFrame import GrabFrame
from aip import AipOcr
from api import APP_ID, API_KEY, SECRET_KEY
from io import BytesIO
import Util

import GlobalVars

class Mainframe(wx.Frame):
    __main_sizer : wx.BoxSizer
    __capture_panel : wx.Panel
    __text_panel : wx.Panel
    __capture_button : wx.Button
    __grab_frame : GrabFrame
    __capture_bitmap : wx.StaticBitmap
    __result_text : wx.TextCtrl
    __result_bitmap : wx.Bitmap
    
    def __init__(self, title):
        super().__init__(None, 
                         title=title, 
                         size=wx.Size(wx.GetDisplaySize().GetWidth() * 0.5,
                                      wx.GetDisplaySize().GetHeight() * 0.5))
        
        self.__InitUi()

        self.grab_bitmap : wx.Bitmap = None
        self.__result_bitmap: wx.Bitmap = None
        
    def __InitUi(self):
        self.__InitMenu()
        self.__main_sizer = wx.BoxSizer(wx.VERTICAL)
        upper_sizer = wx.BoxSizer(wx.HORIZONTAL)
        downer_sizer = wx.BoxSizer(wx.VERTICAL)
        
        upper_sizer.Add(self.__InitCapturePanel(), 1, wx.EXPAND)
        upper_sizer.Add(self.__InitReconizeResPanel(), 1, wx.EXPAND)
        
        downer_sizer.Add(self.__InitCaptureButton(), 0, wx.ALIGN_LEFT | wx.ALL, 10)
        # downer_sizer.Add(self.__InitReconizeButton(), 0, wx.ALIGN_LEFT | wx.ALL, 10)
        
        self.__main_sizer.Add(upper_sizer, 1, wx.EXPAND)
        self.__main_sizer.Add(downer_sizer, 0, wx.EXPAND)
        
        self.SetSizer(self.__main_sizer)

        self.CreateStatusBar()

    def __InitMenu(self):
        import os
        self.menu_bar = wx.MenuBar()

        for menu_info in GlobalVars.MENUS:
            menu = wx.Menu()
            for item in menu_info['menu_items']:
                menu_item = wx.MenuItem(**item['property'])
                if 'icon' in item and item['icon']:
                    icon_path = GlobalVars.ICON_PATH + item['icon']
                    if os.path.exists(icon_path):
                        menu_item.SetBitmap(
                            Util.GetIcon(
                                icon_path, GlobalVars.ICON_SETTING['menu_icon']))
                menu.Append(menu_item)
            self.menu_bar.Append(menu, menu_info['title'])
        
        self.SetMenuBar(self.menu_bar)
        return
        
    def __InitCapturePanel(self) -> wx.BoxSizer:
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.__capture_panel = wx.Panel(self, wx.ID_ANY, style=wx.TAB_TRAVERSAL | wx.NO_BORDER)
        panel_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.__capture_bitmap = wx.StaticBitmap(self.__capture_panel)
        # self.__capture_bitmap.SetScaleMode(wx.StaticBitmap.Scale_AspectFit)
        panel_sizer.Add(self.__capture_bitmap, 1, wx.EXPAND)
        self.__capture_panel.SetSizer(panel_sizer)
        
        sizer.Add(self.__capture_panel, 1, wx.EXPAND)
        
        return sizer
    
    def __InitReconizeResPanel(self) -> wx.BoxSizer:
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.__text_panel = wx.Panel(self, wx.ID_ANY, style=wx.TAB_TRAVERSAL | wx.NO_BORDER)
        panel_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.__result_text = wx.TextCtrl(self.__text_panel, style=wx.TE_MULTILINE | wx.TE_LEFT)
        panel_sizer.Add(self.__result_text, 1, wx.EXPAND)
        self.__text_panel.SetSizer(panel_sizer)
        
        sizer.Add(self.__text_panel, 1, wx.EXPAND)        
        
        return sizer
    
    def __InitCaptureButton(self) -> wx.BoxSizer:
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.__capture_button = wx.Button(self, wx.ID_ANY, u'截图')
        sizer.Add(self.__capture_button, 0, wx.EXPAND)
        self.__capture_button.Bind(wx.EVT_BUTTON, self.__OnClick)
        return sizer

    def __InitReconizeButton(self) -> wx.BoxSizer:
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.__reconize_button = wx.Button(self, wx.ID_ANY, u'识别')
        sizer.Add(self.__reconize_button, 0, wx.EXPAND)
        self.__reconize_button.Bind(wx.EVT_BUTTON, self.__OnReconize)
        return sizer

    def __OnClick(self, evt):
        self.Hide()
        while not self.IsShownOnScreen():
            # self.grab_bitmap = self.__GetScreenBmp()
            # wx.Sleep(1)
            wx.MilliSleep(200)
            screen_bitmap = self.__GetScreenBmp()
            self.__grab_frame: GrabFrame = GrabFrame(self, screen_bitmap)
            break

    def __GetScreenBmp(self):
        s: wx.Size = wx.GetDisplaySize()
        bmp: wx.Bitmap = wx.Bitmap(s.x, s.y)
        dc = wx.ScreenDC()
        memdc = wx.MemoryDC()
        memdc.SelectObject(bmp)
        memdc.Blit(0,0, s.x, s.y, dc, 0,0)
        memdc.SelectObject(wx.NullBitmap)
        return bmp
    
    def ProcessGrabBitmap(self, _grab_bitmap : wx.Bitmap):
        self.__grab_frame.Destroy()
        self.__capture_bitmap.SetScaleMode(wx.StaticBitmap.Scale_AspectFit)
        self.__capture_bitmap.SetBitmap(_grab_bitmap)
        self.__capture_panel.Layout()
        self.__capture_panel.Refresh()
        # wx.Sleep(0.5)
        self.__TextReconize(_grab_bitmap)
        # self.__result_bitmap = _grab_bitmap
        return

    def __OnReconize(self, evt):
        self.__TextReconize(self.__result_bitmap)
    
    def __TextReconize(self, _grab_bitmap : wx.Bitmap):
        temp_img = BytesIO()
        image : wx.Image = _grab_bitmap.ConvertToImage()
        image.SaveFile(temp_img, wx.BITMAP_TYPE_JPEG)
        client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
        options = {'language_type' : 'CHN_ENG', 'paragraph' : True}
        result = client.basicGeneral(temp_img.getvalue(), options)
        print(result)
        text = ''
        for res in result['words_result']:
            text += res['words']
            text += '\n'
        self.__result_text.SetValue(text)
        return

