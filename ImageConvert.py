import wx
from PIL.Image import Image as PilImage


def PilImage2WxImage(_pil_image:PilImage):
    '''
    转换　PIL Image 为　wxPython Image
    :param _pil_image: PIL.Image.Image
    :return: wx.Image
    '''
    wx_image = wx.Image((_pil_image.size[0], _pil_image.size[1]), 
                       _pil_image.convert('RGB').tobytes())
    return wx_image
 
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

