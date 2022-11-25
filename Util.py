import wx
import GlobalVars

def GetIcon(_icon_path : str, _icon_size : tuple):
    import os
    if os.path.exists(_icon_path):
        image = wx.Image(_icon_path)
        image.Rescale(_icon_size[0], _icon_size[1])
        return wx.Bitmap(image)
    else:
        return wx.NullBitmap

def GetMenuById(id: int):
    for menu in GlobalVars.MENUS:
        for item in menu['menu_items']:
            if item['property']['id'] == id:
                return item
    return None

