import wx
import GlobalVars
import Util


class AboutDialog(wx.Dialog):
    BORDER = 5

    def __init__(self, parent):
        super().__init__(parent, title=u'关于', size=(400, 200))
        self.__InitUi()

        return

    def __InitUi(self):
        top_sizer = wx.BoxSizer(wx.VERTICAL)
        self.__main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.__InitBitmap()
        self.__InitText()
        top_sizer.Add(self.__main_sizer, 0, wx.ALIGN_CENTER)
        self.CenterOnParent()
        self.SetSizer(top_sizer)
        # self.Fit()
        return

    def __InitBitmap(self):
        border = self.BORDER
        bitmap_width = 100
        bitmap_height = bitmap_width
        bitmap_sizer = wx.BoxSizer(wx.VERTICAL)
        bitmap = wx.StaticBitmap(self,bitmap = Util.GetIcon('frame_icon_large', (bitmap_width, bitmap_height)))
        bitmap_sizer.Add(bitmap, 0, wx.ALIGN_RIGHT | wx.LEFT | wx.TOP | wx.BOTTOM, border)
        self.__main_sizer.Add(bitmap_sizer, 1, wx.EXPAND | wx.LEFT | wx.TOP | wx.BOTTOM, border)
        return bitmap

    def __InitText(self):
        border = self.BORDER
        def SetText(_text: str, _text_sizer: wx.Sizer, _font: wx.Font=None):
            border = self.BORDER
            text_label = wx.StaticText(self, label=_text, style=wx.ALIGN_CENTER)
            if _font:
                text_label.SetFont(_font)
            label_sizer = wx.BoxSizer(wx.VERTICAL)
            label_sizer.Add(text_label, 0, wx.ALIGN_CENTER | wx.ALL, border)
            _text_sizer.Add(label_sizer, 1, wx.EXPAND | wx.ALL, border)
            return text_label

        text_sizer = wx.BoxSizer(wx.VERTICAL)
        title_font_info = wx.FontInfo(18)
        title_font_info.Bold(True)
        title_font_info.FaceName('Consolas')
        SetText(GlobalVars.TITLE + ' v' + GlobalVars.VERSION, text_sizer, wx.Font(title_font_info))
        SetText(u'Copyright by LazyDennis. \nAll rights reserves.', text_sizer)

        self.__main_sizer.Add(text_sizer, 0, wx.ALIGN_CENTER  | wx.RIGHT | wx.TOP | wx.BOTTOM, border)
        
        return