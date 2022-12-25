import wx
from PIL.Image import Image as PilImage
import Util

class ImageEnhanceDialog(wx.Dialog):
    def __init__(self, _parent, _raw_bitmap: wx.Bitmap, _result_bitmap: wx.Bitmap):
        super().__init__(_parent, 
                         title=u'图像增强', 
                         size=_parent.GetSize(),
                         style=wx.DEFAULT_DIALOG_STYLE)
        self.__raw_image : wx.Bitmap = _raw_bitmap
        self.__result_image: wx.Bitmap = _result_bitmap
        self.__pil_image: PilImage = Util.WxImage2PilImage(self.__raw_image.ConvertToImage())
        self.__InitUI()
    
    
    def __InitUI(self):
        BORDER = 5
        self.__image_view, image_view_sizer = self.__InitImageView()
        tuning_ctrl_sizer = self.__InitTuningControl()
        
        self.__main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.__main_sizer.Add(image_view_sizer, 0, wx.EXPAND | wx.ALL, BORDER)
        self.__main_sizer.Add(tuning_ctrl_sizer, 0, wx.EXPAND | wx.ALL, BORDER)
        
        self.SetSizer(self.__main_sizer)
        self.Layout()
        
        self.__image_view.SetBitmap(self.__result_image)
        return
    
    def __InitImageView(self):
        image_view = wx.StaticBitmap(self, wx.ID_ANY)
        image_view_sizer = wx.StaticBoxSizer(wx.VERTICAL, self, u'图像')
        image_view_sizer.Add(image_view)
        return image_view, image_view_sizer
    
    def __InitTuningControl(self):
        BORDER = 5
        label = wx.StaticText(self, wx.ID_ANY, u'对比度')
        slider = wx.Slider(self, 
                           wx.ID_ANY,
                           value=0,
                           minValue=-2,
                           maxValue=2)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(label, 0, wx.EXPAND | wx.ALL, BORDER)
        sizer.Add(slider, 1, wx.EXPAND | wx.ALL, BORDER)
        tuning_ctrl_sizer = wx.StaticBoxSizer(wx.VERTICAL, self, u'调节')
        tuning_ctrl_sizer.Add(sizer, 0, wx.EXPAND)
        return tuning_ctrl_sizer
    
    
    def GetModBitmap(self):
        mod_bitmap: wx.Bitmap = None
        
        return mod_bitmap