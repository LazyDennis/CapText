import wx

ICON_PATH = '.\\icon\\'
ICON_SETTING = {
    'menu_icon': (25, 25),
    'toolbar_icon': (30, 30)
}

MENUS = [
    {
        'title': u'文件(&F)',
        'menu_items':
        [
            {
                'property':
                {
                    'id': 100,
                    'text': u'新建\tCTRL+&N',
                    'helpString': u'新建截图',
                    'kind': wx.ITEM_NORMAL
                },
                'icon': u'创建_newlybuild.png',
                'handler': '__OnNew',
                'toolbartool': True
            },
            {
                'property':
                {
                    'id': 101,
                    'text': u'打开图片\tCTRL+&O',
                    'helpString': u'打开已有图片',
                    'kind': wx.ITEM_NORMAL
                },
                'icon': u'图片文件_image-files.png',
                'handler': '__OnOpenImage',
                'toolbartool': True,
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
                    'id': 102,
                    'text': u'保存截图\tCTRL+&P',
                    'helpString': u'保存当前截图',
                    'kind': wx.ITEM_NORMAL
                },
                'icon': u'图片下载_down-picture.png',
                'handler': '__OnSaveCapture',
                'toolbartool': True,
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
                    'id': 103,
                    'text': u'保存文本\tCTRL+&S',
                    'helpString': u'保存识别文本',
                    'kind': wx.ITEM_NORMAL
                },
                'icon': u'文本文件_file-text.png',
                'handler': '__OnSaveText',
                'toolbartool': True,
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
                    'id': wx.ID_SEPARATOR
                }
            },
            {
                'property':
                {
                    'id': 109,
                    'text': u'退出\tCTRL+&E',
                    'helpString': u'退出程序',
                    'kind': wx.ITEM_NORMAL
                },
                'icon': u'退出_logout.png',
                'handler': '__OnExit',
                'toolbartool': True
            }
        ]
    },
    {
        'title': u'动作(&A)',
        'menu_items':
        [  
            {
                'property':
                {
                    'id': 110,
                    'text': u'截图\tCTRL+&K',
                    'helpString': u'获取截图',
                    'kind': wx.ITEM_NORMAL
                },
                'icon': u'截图_screenshot-one.png',
                'handler': '__OnCapture',
                'toolbartool': True
            },
            {
                'property':
                {
                    'id': 111,
                    'text': u'识别\tCTRL+&R',
                    'helpString': u'识别当前截图',
                    'kind': wx.ITEM_NORMAL
                },
                'icon': u'文字识别_text-recognition.png',
                'handler': '__OnRecognize',
                'toolbartool': True
            },
            {
                'property':
                {
                    'id': wx.ID_SEPARATOR
                }
            },
            {
                'property':
                {
                    'id': 112,
                    'text': u'设定\tCTRL+&I',
                    'helpString': u'变更设定',
                    'kind': wx.ITEM_NORMAL
                },
                'icon': u'设置_setting-two.png',
                'handler': '__OnSetting',
                'toolbartool': True
            }
        ]
    },
    {
        'title': u'帮助(&H)',
        'menu_items':
        [  
            {
                'property':
                {
                    'id': 130,
                    'text': u'帮助\tCTRL+&H',
                    'helpString': u'获取帮助',
                    'kind': wx.ITEM_NORMAL
                },
                'icon': u'帮助_help.png',
                'handler': '__OnHelp',
                'toolbartool': True
            },
            {
                'property':
                {
                    'id': 131,
                    'text': u'关于',
                    'helpString': u'关于',
                    'kind': wx.ITEM_NORMAL
                },
                'icon': u'信息_info.png',
                'handler': '__OnAbout',
                'toolbartool': False
            }
        ]
    }
]

BITMAP_TYPE_MAP ={
    'bmp' : wx.BITMAP_TYPE_BMP,
    'jpg' : wx.BITMAP_TYPE_JPEG,
    'gif' : wx.BITMAP_TYPE_GIF,
    'tif' : wx.BITMAP_TYPE_TIF,
    'png' : wx.BITMAP_TYPE_PNG
}