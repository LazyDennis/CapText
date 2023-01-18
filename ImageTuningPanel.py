import wx
import GlobalVars
from ImageEnhance import ImageEnhance


class ImageTuningPanel(wx.Dialog):
    sliders_settings = GlobalVars.SLIDER_SETTING
    sliders: dict = {}

    def __init__(self, _parent, _tool, _pos=wx.DefaultPosition):
        super().__init__(_parent,
                         style=wx.CAPTION |
                         #  wx.CLOSE_BOX |
                         wx.FRAME_TOOL_WINDOW |
                         wx.FRAME_FLOAT_ON_PARENT |
                         wx.FRAME_NO_TASKBAR,  # |
                         #  wx.CLIP_CHILDREN,
                         pos=_pos)
        self.slider_methods = {
            'contrast': ImageEnhance.Type.CONTRAST,
            'color': ImageEnhance.Type.COLOR,
            'brightness': ImageEnhance.Type.BRIGHTNESS,
            'sharpness': ImageEnhance.Type.SHARPNESS
        }
        self.__tool: wx.ToolBarToolBase = _tool
        self.__tool.SetToggle(True)
        self.__tool.Toggle(True)
        self.__InitUi()
        # self.Bind(wx.EVT_CLOSE, self.__OnClose)

    def __InitUi(self):
        self.__main_sizer = wx.BoxSizer(wx.VERTICAL)

        slider_sizer = self.__InitSliders()

        self.__main_sizer.Add(slider_sizer, 0, wx.EXPAND)
        self.__default_button = self.__InitButton()

        self.Show()
        self.SetSizerAndFit(self.__main_sizer)
        return

    def __InitSliders(self):
        BORDER = 5
        slider_sizer = wx.BoxSizer(wx.VERTICAL)
        for sl_key, sl_val in self.sliders_settings.items():
            sl_sizer = wx.BoxSizer(wx.HORIZONTAL)
            label = wx.StaticText(self, wx.ID_ANY, sl_val['text'])
            slider = wx.Slider(self, **sl_val['property'])
            text_ctrl = wx.TextCtrl(self,
                                    value=str(slider.GetValue()),
                                    size=(30, -1),
                                    style=wx.TE_PROCESS_ENTER)
            sl_sizer.AddMany([
                (label, 0, wx.ALIGN_CENTER | wx.ALL, BORDER),
                (slider, 0, wx.EXPAND | wx.ALL, BORDER),
                (text_ctrl, 0, wx.ALIGN_CENTER | wx.ALL, BORDER)
            ])
            slider_sizer.Add(sl_sizer, 0, wx.EXPAND)
            self.sliders[sl_key] = {'slider': slider, 'text_ctrl': text_ctrl}
            slider.Bind(wx.EVT_SLIDER, lambda evt,
                        sl_key=sl_key: self.__OnSlide(_evt=evt, _slkey=sl_key))
            text_ctrl.Bind(wx.EVT_TEXT_ENTER, lambda evt,
                           sl_key=sl_key: self.__OnTextEnter(evt, sl_key))
        return slider_sizer

    def __InitButton(self):
        button = wx.Button(self, wx.ID_ANY, u'复原')
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(button, 0, wx.ALIGN_CENTER)
        self.__main_sizer.Add(sizer, 0, wx.EXPAND)
        button.Bind(wx.EVT_BUTTON, self.__OnSetDefault)
        return button

    def __OnSlide(self, _evt, _slkey):
        value = self.sliders[_slkey]['slider'].GetValue()
        self.sliders[_slkey]['text_ctrl'].SetValue(str(value))
        raw_bitmap: wx.Bitmap = self.Parent.GetRawBitmap()
        if raw_bitmap:
            image_enhance = ImageEnhance(raw_bitmap.ConvertToImage())
            for sl_key, sl_val in self.sliders.items():
                max_val = sl_val['slider'].GetMax()
                min_val = sl_val['slider'].GetMin()
                val = sl_val['slider'].GetValue()
                image_enhance.Enhance(
                    self.slider_methods[_slkey], val, max_val, min_val)            
            self.Parent.SetResultBitmap(
                image_enhance.GetWxImage().ConvertToBitmap())
            self.Parent.SetCaptureBitmap(self.Parent.GetResultBitmap())
        return

    def __OnTextEnter(self, _evt, _slkey):
        value = self.sliders[_slkey]['text_ctrl'].GetValue()
        slider = self.sliders[_slkey]['slider']
        slider.SetValue(int(value))
        self.__OnSlide(_evt, _slkey)
        return

    def __OnSetDefault(self, _evt):
        self.SetDefault()

    def SetDefault(self):
        raw_bitmap: wx.Bitmap = self.Parent.GetRawBitmap()
        self.Parent.SetResultBitmap(wx.Bitmap(raw_bitmap))
        self.Parent.SetCaptureBitmap(
            wx.Bitmap(raw_bitmap if raw_bitmap else wx.NullBitmap))
        for key, val in self.sliders.items():
            default_value = self.sliders_settings[key]['property']['value']
            val['slider'].SetValue(default_value)
            val['text_ctrl'].SetValue(str(default_value))
        return

    def GetTool(self) -> wx.ToolBarToolBase:
        return self.__tool

    # def __OnClose(self, _evt):
    #     # self.Hide()
    #     print(self.__tool.IsToggled())
    #     print(self.__tool.Toggle(False))
    #     print(self.__tool.SetToggle(False))
    #     _evt.Veto()
    #     return
