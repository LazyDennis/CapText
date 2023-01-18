import wx
from enum import Enum
from PIL import Image as PilImage
from PIL import ImageEnhance as PilImageEnhance

class ImageEnhance:
    
    __wx_image: wx.Image = None
    
    class Type(Enum):
        CONTRAST = 1
        COLOR = 2
        BRIGHTNESS = 3
        SHARPNESS = 4
        
    __methods = {
        Type.CONTRAST: PilImageEnhance.Contrast,
        Type.COLOR: PilImageEnhance.Color,
        Type.BRIGHTNESS: PilImageEnhance.Brightness,
        Type.SHARPNESS: PilImageEnhance.Sharpness
    }

    def __init__(self, _wx_image: wx.Image=None) -> None:
        self.SetWxImage(_wx_image)
        return
    
    def Enhance(self, _type: Type,
                _cur_val: int, 
                _max_val: int, 
                _min_val: int):
        
        mid_val = (_max_val - _min_val) / 2 if _min_val >= 0 else 0
        ratio = 1 / (mid_val - _min_val)
        factor = (_cur_val - _min_val) / ratio
        pil_enhance = self.__methods[_type](self.__pil_image)
        self.__pil_image = pil_enhance.enhance(factor)
        return

    def SetWxImage(self, _wx_image: wx.Image):
        self.__wx_image = _wx_image
        self.__pil_image = self.WxImage2PilImage(_wx_image)
        return
    
    def GetWxImage(self)-> wx.Image:
        self.__wx_image = self.PilImage2WxImage(self.__pil_image)
        return self.__wx_image
    
    @staticmethod
    def PilImage2WxImage(_pil_image: PilImage.Image):
        '''
        转换　PIL Image 为　wxPython Image
        :param _pil_image: PIL.Image.Image
        :return: wx.Image
        '''
        wx_image = wx.Image((_pil_image.size[0], _pil_image.size[1]), 
                        _pil_image.convert('RGB').tobytes())
        return wx_image
    
    @staticmethod
    def WxImage2PilImage(_wx_image:wx.Image):
        '''
        转换 wxPython Image 为　PIL Image 对象
        :param _wx_image: wx.Image 实例
        :return: PIL.Image.Image
        '''
        # _wx_image 的 GetData方法返回图像的字节码，通过bytes强制转换，可以直接作为frombytes的参数。
        pil_image = PilImage.frombytes('RGB', (_wx_image.GetWidth(), _wx_image.GetHeight()), 
                                    bytes(_wx_image.GetData()))
        
        return pil_image
