import wx
import Service.TextReconize as TextReconize
import api

TITLE = 'CapText'

MAIN_VERSION = 1
SUB_VERSION = 6
MINOR_VERSION = '0b'
VERSION = str(MAIN_VERSION) + '.' + str(SUB_VERSION) + '.' + str(MINOR_VERSION)

SETTING_FILE = 'Setting.conf'

ICON_SETTING = {
    'frame_icon_large': (32, 32),
    'frame_icon_small': (16, 16),
    'menu_icon': (25, 25),
    'toolbar_icon': (30, 30)
}

ID_NEW = 100
ID_OPEN = 101
ID_SAVE_CAPTURE = 102
ID_SAVE_TEXT = 103
ID_SHOW = 108 
ID_EXIT = 109
ID_CAPTURE = 110
ID_PIC_ENHANCE = 113
ID_RECONIZE = 111
ID_SETTING = 112
ID_HELP = 130
ID_ABOUT = 131
MENUS = [
    {
        'title': u'文件(&F)',
        'show_on_screen': True,
        'menu_items':
        [
            {
                'property':
                {
                    'id': ID_NEW,
                    'text': u'新建\tCTRL+&N',
                    'helpString': u'新建截图',
                    'kind': wx.ITEM_NORMAL
                },
                'show_on_screen': True,
                'icon': u'创建_newlybuild.png',
                'handler': '__OnNew',
                'toolbartool': True,
                'menutool': True
            },
            {
                'property':
                {
                    'id': ID_OPEN,
                    'text': u'打开图片\tCTRL+&O',
                    'helpString': u'打开已有图片',
                    'kind': wx.ITEM_NORMAL
                },
                'show_on_screen': True,
                'icon': u'图片文件_image-files.png',
                'handler': '__OnOpenImage',
                'toolbartool': True,
                'menutool': True,
                'dialog':
                {
                    'message': u'打开图片',
                    'wildcard': u'支持的图像文件(*.bmp;*.jpg;*.gif;*.tif;*.png)|*.bmp;*.jpg;*.gif;*.tif;*.png',
                    'style': wx.FD_OPEN | wx.FD_PREVIEW
                }
            },
            {
                'property':
                {
                    'id': ID_SAVE_CAPTURE,
                    'text': u'保存截图\tCTRL+&P',
                    'helpString': u'保存当前截图',
                    'kind': wx.ITEM_NORMAL
                },
                'show_on_screen': True,
                'icon': u'图片下载_down-picture.png',
                'handler': '__OnSaveCapture',
                'toolbartool': True,
                'menutool': True,
                'dialog':
                {
                    'message': u'保存当前截图',
                    'wildcard': u'位图文件(*.bmp)|*.bmp|'+\
                                u'JPEG文件(*.jpg)|*.jpg|'+\
                                u'动画文件(*.gif)|*.gif|'+\
                                u'TIFF文件(*.tif)|*.tif|'+\
                                u'PNG文件(*.png)|*.png',
                    'style': wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
                }
            },
            {
                'property':
                {
                    'id': ID_SAVE_TEXT,
                    'text': u'保存文本\tCTRL+&S',
                    'helpString': u'保存识别文本',
                    'kind': wx.ITEM_NORMAL
                },
                'show_on_screen': True,
                'icon': u'文本文件_file-text.png',
                'handler': '__OnSaveText',
                'toolbartool': True,
                'menutool': True,
                'dialog':
                {
                    'message': u'保存识别文本',
                    'wildcard': u'文本文件(*.txt)|*.txt',
                    'style': wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
                }
            },
            {
                'property':
                {
                    'id': ID_SHOW,
                    'text': u'显示程序',
                    'helpString': u'显示程序',
                    'kind': wx.ITEM_NORMAL
                },
                'show_on_screen': True,
                'icon': None,
                'handler': '__OnShow',
                'toolbartool': False,
                'menutool': False,
                'iconmenu': True
            },
            {
                'property':
                {
                    'id': wx.ID_SEPARATOR
                },
                'show_on_screen': True,
                'iconmenu': True
            },
            {
                'property':
                {
                    'id': ID_EXIT,
                    'text': u'退出\tCTRL+&E',
                    'helpString': u'退出程序',
                    'kind': wx.ITEM_NORMAL
                },
                'show_on_screen': True,
                'icon': u'退出_logout.png',
                'handler': '__OnExit',
                'toolbartool': True,
                'menutool': True,
                'iconmenu': True
            }
        ]
    },
    {
        'title': u'动作(&A)',
        'show_on_screen': True,
        'menu_items':
        [  
            {
                'property':
                {
                    'id': ID_CAPTURE,
                    'text': u'截图\tCTRL+&W',
                    'helpString': u'获取截图',
                    'kind': wx.ITEM_NORMAL
                },
                'show_on_screen': True,
                'icon': u'截图_screenshot-one.png',
                'handler': '__OnCapture',
                'toolbartool': True,
                'menutool': True,
                'iconmenu': True
            },
            {
                'property':
                {
                    'id': ID_PIC_ENHANCE,
                    'text': u'图像增强\tCTRL+&T',
                    'helpString': u'调整图像',
                    'kind': wx.ITEM_NORMAL
                },
                'show_on_screen': True,
                'icon': u'均衡器_equalizer.png',
                'handler': '__OnImageEnhance',
                'toolbartool': True,
                'menutool': True,
            },
            {
                'property':
                {
                    'id': ID_RECONIZE,
                    'text': u'识别\tCTRL+&R',
                    'helpString': u'识别当前截图',
                    'kind': wx.ITEM_NORMAL
                },
                'show_on_screen': True,
                'icon': u'文字识别_text-recognition.png',
                'handler': '__OnRecognize',
                'toolbartool': True,
                'menutool': True
            },
            {
                'property':
                {
                    'id': wx.ID_SEPARATOR
                },
                'show_on_screen': True,
            },
            {
                'property':
                {
                    'id': ID_SETTING,
                    'text': u'设定\tCTRL+&I',
                    'helpString': u'变更设定',
                    'kind': wx.ITEM_NORMAL
                },
                'show_on_screen': True,
                'icon': u'设置_setting-two.png',
                'handler': '__OnSetting',
                'toolbartool': True,
                'menutool': True,
                'iconmenu': True
            }
        ]
    },
    {
        'title': u'帮助(&H)',
        'show_on_screen': True,
        'menu_items':
        [  
            {
                'property':
                {
                    'id': ID_HELP,
                    'text': u'帮助\tCTRL+&H',
                    'helpString': u'获取帮助',
                    'kind': wx.ITEM_NORMAL
                },
                'show_on_screen': False,
                'icon': u'帮助_help.png',
                'handler': '__OnHelp',
                'toolbartool': True,
                'menutool': True
            },
            {
                'property':
                {
                    'id': ID_ABOUT,
                    'text': u'关于',
                    'helpString': u'关于',
                    'kind': wx.ITEM_NORMAL
                },
                'show_on_screen': True,
                'icon': u'信息_info.png',
                'handler': '__OnAbout',
                'toolbartool': True,
                'menutool': True
            }
        ]
    }
]

SLIDER_SETTING = {
    'contrast': {
        'show': True,
        'text': u'对比度',
        # 'ratio': 10,
        'property':{
            'value': 0,
            'minValue': -50,
            'maxValue': 50,
            'style': wx.SL_MIN_MAX_LABELS
        }
    },
    'color': {
        'show': True,
        'text': u'颜   色',
        # 'ratio': 10,
        'property':{
            'value': 0,
            'minValue': -50,
            'maxValue': 50,
            'style': wx.SL_MIN_MAX_LABELS
        }
    },
    'brightness': {
        'show': True,
        'text': u'亮   度',
        # 'ratio': 10,
        'property':{
            'value': 0,
            'minValue': -50,
            'maxValue': 50,
            'style': wx.SL_MIN_MAX_LABELS
        }
    },
    'sharpness': {
        'show': True,
        'text': u'锐   度',
        # 'ratio': 10,
        'property':{
            'value': 0,
            'minValue': -50,
            'maxValue': 50,
            'style': wx.SL_MIN_MAX_LABELS
        }
    }
}

BITMAP_TYPE_MAP ={
    'bmp' : wx.BITMAP_TYPE_BMP,
    'jpg' : wx.BITMAP_TYPE_JPEG,
    'gif' : wx.BITMAP_TYPE_GIF,
    'tif' : wx.BITMAP_TYPE_TIF,
    'png' : wx.BITMAP_TYPE_PNG
}

RECONIZE_LANGUAGE = {
    '中英混合（默认）': 'CHN_ENG',
    '日文': 'JAP'
}

RECONIZE_TYPE = {
    '百度' : 1
}

RECONIZE_METHOD = {
    1: {
        '_reconize_method': TextReconize.BaiduOcr,
        '_args': {
            '_appid': api.APP_ID,
            '_apikey':  api.API_KEY,
            '_secretkey':  api.SECRET_KEY,
            '_options': {
                'language_type': 'CHN_ENG',
                'paragraph': True
            }
        }
    }
}

CAPTURE_ALL_DISPLAY = 0
CAPTURE_CURRENT_DISPLAY = 1
CAPTURE_DISPLAY_SETTING = {
    CAPTURE_ALL_DISPLAY: u'截取所有屏幕',
    CAPTURE_CURRENT_DISPLAY: u'截取当前屏幕'
}

CLOSE_TO_TASKBAR = 0
CLOSE_TO_EXIT = 1
CLOSE_USER_SELECT = 2
CLOSE_SETTING = {
    CLOSE_TO_TASKBAR: u'最小化到系统托盘',
    CLOSE_TO_EXIT: u'退出' + TITLE,
    CLOSE_USER_SELECT: u'退出时选择'
}

DEFAULT_SETTING = {
            'hotkey': 'D',
            'language_type': RECONIZE_LANGUAGE[u'中英混合（默认）'],
            'capture_all_display': CAPTURE_ALL_DISPLAY, # 0 for all, 1 for current
            'close_setting': CLOSE_USER_SELECT, # True for close to taskbar, False for close to exit
            'minimize_to_taskbar': False
}

from enum import Enum, unique

# @unique
# class CursorSizeType(Enum):
#     DEFAULT = 10
#     MOVE = 11
#     NWSE = 12
#     NESW = 13
#     WE = 14
#     NS = 15

@unique
class RectanglePositon(Enum):
    EXTERNAL = 20
    INTERNAL = 21
    LEFT = 22
    RIGHT = 23
    TOP = 24
    BOTTOM = 25
    TOPLEFT = 26
    TOPRIGHT = 27
    BOTTOMLEFT = 28
    BOTTOMRIGHT = 29

# POINT_COMPARE_RANGE = 10    #x、y方向上的范围
# POINT_COMPARE_X = 0x1   #只比较X坐标
# POINT_COMPARE_Y = 0X2   #只比较y坐标
# POINT_COMPARE_XY = POINT_COMPARE_X | POINT_COMPARE_Y #X、y都比较