import wx
import GlobalVars

def GetIcon(_icon_path : str, _icon_size : tuple) -> wx.Bitmap:
    from Resource.Icons import ICONS
    from wx.lib.embeddedimage import PyEmbeddedImage

    if _icon_path in ICONS:
        bmp = PyEmbeddedImage(ICONS[_icon_path]).GetBitmap()
        wx.Bitmap.Rescale(bmp, _icon_size)
    else:
        bmp = wx.NullBitmap
    return bmp
    

def GetMenuById(_id: int):
    for menu in GlobalVars.MENUS:
        for item in menu['menu_items']:
            if item['property']['id'] == _id:
                return item
    return None

def GetDictKey(_dict : dict, _val):
    for key, value in _dict.items():
        if value == _val:
            return key
    return None