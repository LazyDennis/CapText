import wx

def GetIcon(_icon_path : str, _icon_size : tuple):
    import os
    if os.path.exists(_icon_path):
        image = wx.Image(_icon_path)
        image.Rescale(_icon_size[0], _icon_size[1])
        return wx.Bitmap(image)
    else:
        return None