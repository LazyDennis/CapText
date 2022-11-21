import wx
from GrabFrame import GrabFrame
from aip import AipOcr
        
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
        self.__main_sizer = wx.BoxSizer(wx.VERTICAL)
        upper_sizer = wx.BoxSizer(wx.HORIZONTAL)
        downer_sizer = wx.BoxSizer(wx.VERTICAL)
        
        upper_sizer.Add(self.__InitCapturePanel(), 1, wx.EXPAND)
        upper_sizer.Add(self.__InitTranResPanel(), 1, wx.EXPAND)
        
        downer_sizer.Add(self.__InitCaptureButton(), 0, wx.ALIGN_LEFT | wx.ALL, 10)
        
        self.__main_sizer.Add(upper_sizer, 1, wx.EXPAND)
        self.__main_sizer.Add(downer_sizer, 0, wx.EXPAND)
        
        self.SetSizer(self.__main_sizer)
        
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
    
    def __InitTranResPanel(self) -> wx.BoxSizer:
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.__text_panel = wx.Panel(self, wx.ID_ANY, style=wx.TAB_TRAVERSAL | wx.NO_BORDER)
        panel_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.__result_text = wx.TextCtrl(self.__text_panel, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_LEFT)
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

    def __OnClick(self, evt):
        self.Hide()
        while not self.IsShownOnScreen():
            # self.grab_bitmap = self.__GetScreenBmp()
            wx.Sleep(1)
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
        wx.Sleep(1)
        self.__TextReconize(_grab_bitmap)
        return
    
    def __TextReconize(self, _grab_bitmap : wx.Bitmap):
        _grab_bitmap.SaveFile('temp.jpg', wx.BITMAP_TYPE_JPEG)
        api_config = ReadConfig()
        print('got config')
        client = AipOcr(api_config['APP_ID'], api_config['API_KEY'], 
                        api_config['SECRET_KEY'])
        options = {'language_type' : 'CHN_ENG', 'paragraph' : True}
        with open('temp.jpg', 'rb') as fp:
            result = client.basicGeneral(fp.read(), options)
            print(result)
            text = ''
            for res in result['words_result']:
                text += res['words']
                text += '\n'
            self.__result_text.SetValue(text)
        return


def ReadConfig():
    import json
    with open('ApiSetting.conf', 'r') as fp:
        api_conf = json.loads(fp.read())
        return api_conf


import win32gui, win32ui, win32con, win32api
def window_capture(filename, start_point : tuple, size : tuple):
    hwnd = 0                                                        # 窗口的编号，0号表示当前活跃窗口
    hwndDC = win32gui.GetWindowDC(hwnd)                                    # 根据窗口句柄获取窗口的设备上下文DC（Device Context）
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)                           # 根据窗口的DC获取mfcDC
    saveDC = mfcDC.CreateCompatibleDC()                                  # mfcDC创建可兼容的DC
    saveBitMap = win32ui.CreateBitmap()                              # 创建bitmap准备保存图片
    MoniterDev = win32api.EnumDisplayMonitors(None, None)                  # 获取监控器信息
    w = MoniterDev[0][2][2]
    h = MoniterDev[0][2][3]
    # print(w,h)　　　#图片大小
    saveBitMap.CreateCompatibleBitmap(mfcDC, size[0], size[1])                              # 为bitmap开辟空间
    saveDC.SelectObject(saveBitMap)                                             # 高度saveDC，将截图保存到saveBitmap中
    saveDC.BitBlt((0, 0), size, mfcDC, start_point, win32con.SRCCOPY)              # 截取从左上角（0，0）长宽为（w，h）的图片
    
    saveBitMap.SaveBitmapFile(saveDC, filename)

