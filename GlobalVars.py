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
                'handler': '__OnNew'
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
                'handler': '__OnOpenImage'
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
                'handler': '__OnSaveCapture'
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
                'handler': '__OnSaveText'
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
                    'id': 199,
                    'text': u'退出(&X)\tCTRL+&X',
                    'helpString': u'退出程序',
                    'kind': wx.ITEM_NORMAL
                },
                'icon': u'退出_logout.png',
                'handler': '__OnExit'
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
                    'id': 200,
                    'text': u'截图\tCTRL+&K',
                    'helpString': u'获取截图',
                    'kind': wx.ITEM_NORMAL
                },
                'icon': u'截图_screenshot-one.png',
                'handler': '__OnCapture'
            },
            {
                'property':
                {
                    'id': 201,
                    'text': u'识别\tCTRL+&R',
                    'helpString': u'识别当前截图',
                    'kind': wx.ITEM_NORMAL
                },
                'icon': u'文字识别_text-recognition.png',
                'handler': '__OnRecognize'
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
                    'id': 210,
                    'text': u'设定\tCTRL+&C',
                    'helpString': u'变更设定',
                    'kind': wx.ITEM_NORMAL
                },
                'icon': u'设置_setting-two.png',
                'handler': '__OnSetting'
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
                    'id': 300,
                    'text': u'帮助(&H)\tCTRL+&H',
                    'helpString': u'获取帮助',
                    'kind': wx.ITEM_NORMAL
                },
                'icon': u'帮助_help.png',
                'handler': '__OnHelp'
            },
            {
                'property':
                {
                    'id': 301,
                    'text': u'关于',
                    'helpString': u'关于',
                    'kind': wx.ITEM_NORMAL
                },
                'icon': u'信息_info.png',
                'handler': '__OnAbout'
            }
        ]
    }
]

TOOLBARS = []