import wx


class ImageTuningPanel(wx.Frame):
    def __init__(self, _parent):
        super().__init__(_parent, 
                         style=
                         wx.CAPTION | 
                         wx.CLOSE_BOX | 
                         wx.FRAME_TOOL_WINDOW |
                         wx.FRAME_FLOAT_ON_PARENT |
                         wx.FRAME_NO_TASKBAR |
                         wx.CLIP_CHILDREN)

        self.__InitUi()

    def __InitUi(self):
        BORDER = 5 
        self.__main_sizer = wx.BoxSizer(wx.VERTICAL)

        contrast_sizer = wx.BoxSizer(wx.HORIZONTAL)
        contrast_label = wx.StaticText(self, wx.ID_ANY, u'对比度：')
        self.contrast_slider = wx.Slider(self, 
                                    wx.ID_ANY,
                                    value=10,
                                    minValue=0,
                                    maxValue=10,
                                    style=wx.SL_MIN_MAX_LABELS)
        contrast_sizer.Add(contrast_label, 0, wx.CENTER | wx.ALL, BORDER)
        contrast_sizer.Add(self.contrast_slider, 0, wx.EXPAND | wx.ALL, BORDER)

        self.__main_sizer.Add(contrast_sizer, 0, wx.EXPAND)
        
        self.Show()
        self.SetSizerAndFit(self.__main_sizer)
        return