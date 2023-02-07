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


# def __IsInRange(
#         _point: wx.Point, 
#         _ref_point: wx.Point, 
#         _range: int=GlobalVars.POINT_COMPARE_RANGE, 
#         _comp_flag: int=GlobalVars.POINT_COMPARE_XY) -> bool:
    
#     return \
#         (_comp_flag == GlobalVars.POINT_COMPARE_Y or      #如果只比较y，x的值为任意
#             _point.x in range(_ref_point.x - _range, _ref_point.x + _range + 1)) and \
#         (_comp_flag == GlobalVars.POINT_COMPARE_X or      #如果只比较经x，y的值为任意
#             _point.y in range(_ref_point.y - _range, _ref_point.y + _range + 1))
