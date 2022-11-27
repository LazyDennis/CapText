import wx


class GrabFrame(wx.Frame):

    def __init__(self, parent, _screen_bitmap: wx.Bitmap, size: wx.Size, pos=(0, 0)):
        wx.Frame.__init__(self,
                          parent,
                          wx.ID_ANY,
                          pos=pos,
                          size=size,
                          style=wx.NO_BORDER | wx.STAY_ON_TOP)
        from MainFrame import Mainframe
        ###################################全局变量########################################
        self.__first_point: wx.Point = wx.Point(0, 0)  #记录截图的第一个点
        self.__last_point: wx.Point = wx.Point(0, 0)  #记录截图的最后一个点
        self.__on_capture: bool = False  #记录是否按下鼠标左键
        self.__parent_frame: Mainframe = parent
        self.__screen_bitmap: wx.Bitmap = _screen_bitmap
        
        self.__keymap = {
            wx.WXK_ESCAPE: {'handler': self.__OnKeyEsc, 'id': wx.ID_ANY}
        }

        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.Bind(wx.EVT_PAINT, self.__OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.__OnMouseLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.__OnMouseLeftUp)
        self.Bind(wx.EVT_MOTION, self.__OnMouseMove)
        # self.Bind(wx.EVT_CHAR, self.__OnChar)
        self.Show()

    def __OnPaint(self, _evt):
        dc = wx.GCDC(wx.BufferedPaintDC(self))
        self.__PaintUpdate(dc)

    def __PaintUpdate(self, _dc):
        rect: wx.Rect = self.GetClientRect()
        color = wx.Colour(0, 0, 0, 120)

        #设置绘制截图区域时矩形的点
        minX = min(self.__first_point.x, self.__last_point.x)
        minY = min(self.__first_point.y, self.__last_point.y)
        maxX = max(self.__first_point.x, self.__last_point.x)
        maxY = max(self.__first_point.y, self.__last_point.y)

        #画出整个屏幕的截图
        _dc.DrawBitmap(self.__screen_bitmap, 0, 0)

        #画出阴影部分（截取的部分不需要画）
        _dc.SetPen(wx.Pen(color))
        _dc.SetBrush(wx.Brush(color))
        _dc.DrawRectangle(0, 0, maxX, minY)
        _dc.DrawRectangle(maxX, 0, rect.width - maxX, maxY)
        _dc.DrawRectangle(minX, maxY, rect.width - minX, rect.height - maxY)
        _dc.DrawRectangle(0, minY, minX, rect.height - minY)

        if (self.__on_capture == True):

            #画出截图区域的边框
            _dc.SetPen(wx.Pen(wx.Colour(255, 0, 0)))
            _dc.SetBrush(wx.Brush(color, wx.TRANSPARENT))
            _dc.DrawRectangle(minX, minY, maxX - minX, maxY - minY)

            #显示信息
            _dc.SetBrush(wx.Brush(wx.Colour(255, 0, 0)))
            _dc.DrawRectangleList([(minX - 2, minY - 2, 5, 5),
                                  (maxX / 2 + minX / 2 - 2, minY - 2, 5, 5),
                                  (maxX - 2, minY - 2, 5, 5),
                                  (maxX - 2, maxY / 2 + minY / 2 - 2, 5, 5),
                                  (maxX - 2, maxY - 2, 5, 5),
                                  (maxX / 2 + minX / 2 - 2, maxY - 2, 5, 5),
                                  (minX - 2, maxY - 2, 5, 5),
                                  (minX - 2, maxY / 2 + minY / 2 - 2, 5, 5)])
            color = wx.Colour(0, 0, 0, 180)
            _dc.SetPen(wx.Pen(color))
            _dc.SetBrush(wx.Brush(color, wx.SOLID))
            w, h = 140, 43
            s = u'区域大小：' + str(maxX - minX) + '*' + str(maxY - minY)
            s += u'\n鼠标位置：（' + str(self.__last_point.x) + ',' + str(
                self.__last_point.y) + ')'
            _dc.DrawRectangle(minX, minY - h - 5 if minY - 5 > h else minY + 5,
                             w, h)
            _dc.SetTextForeground(wx.Colour(255, 255, 255))
            _dc.DrawText(s, minX + 5,
                        (minY - h - 5 if minY - 5 > h else minY + 5) + 5)

    def __OnMouseLeftDown(self, _evt):
        # self.__parent_frame.Hide()
        self.__on_capture = True
        self.__first_point = _evt.GetPosition()
        self.__last_point = _evt.GetPosition()

    def __OnMouseLeftUp(self, _evt):
        if (self.__on_capture):
            self.__last_point = _evt.GetPosition()
            if (self.__first_point.x == self.__last_point.x) and \
                (self.__first_point.y == self.__last_point.y):
                wx.MessageBox(u"区域设置不正确", "Error", wx.OK | wx.ICON_ERROR, self)
                self.__on_capture = False
                self.__first_point = wx.Point(0, 0)  #记录截图的第一个点
                self.__last_point = wx.Point(0, 0)  #记录截图的最后一个点
                self.__parent_frame.ProcessGrabBitmap(None)

            else:
                self.__parent_frame.ProcessGrabBitmap(
                    self.__screen_bitmap.GetSubBitmap(
                        wx.Rect(
                            min(self.__first_point.x, self.__last_point.x),
                            min(self.__first_point.y, self.__last_point.y),
                            abs(self.__first_point.x - self.__last_point.x),
                            abs(self.__first_point.y - self.__last_point.y))))

                # self.Destroy()
                # self.__parent_frame.Show()
                # self.__parent_frame.bmp.SaveFile(r'd:\test.jpg', wx.BITMAP_TYPE_JPEG)

    def __OnMouseMove(self, _evt):
        if (self.__on_capture):
            self.__last_point = _evt.GetPosition()
            self.__NewUpdate()

    def __NewUpdate(self):
        self.RefreshRect(self.GetClientRect(), True)
        self.Update()
        
    def __OnChar(self, _evt):
        key_code = _evt.GetKeyCode()
        if key_code in self.__keymap:
            _evt.SetId(self.__keymap[key_code]['id'])
            self.__keymap[key_code]['handler'](_evt)
        else:
            _evt.Skip()
        return    
    
    def __OnKeyEsc(self, _evt):
        self.Hide()