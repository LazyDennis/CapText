import wx


class GrabFrame(wx.Frame):

    def __init__(self, parent, _screen_bitmap: wx.Bitmap):
        wx.Frame.__init__(self,
                          parent,
                          wx.ID_ANY,
                          pos=(0, 0),
                          size=wx.GetDisplaySize(),
                          style=wx.NO_BORDER | wx.STAY_ON_TOP)
        from MainFrame import Mainframe
        ###################################全局变量########################################
        self.__first_point: wx.Point = wx.Point(0, 0)  #记录截图的第一个点
        self.__last_point: wx.Point = wx.Point(0, 0)  #记录截图的最后一个点
        self.__on_capture: bool = False  #记录是否按下鼠标左键
        self.__parent_frame: Mainframe = parent
        self.__screen_bitmap: wx.Bitmap = _screen_bitmap

        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnMouseLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMouseMove)
        self.Show()

    def OnPaint(self, evt):
        dc = wx.GCDC(wx.BufferedPaintDC(self))
        self.PaintUpdate(dc)

    def PaintUpdate(self, dc):
        rect: wx.Rect = self.GetClientRect()
        color = wx.Colour(0, 0, 0, 120)

        #设置绘制截图区域时矩形的点
        minX = min(self.__first_point.x, self.__last_point.x)
        minY = min(self.__first_point.y, self.__last_point.y)
        maxX = max(self.__first_point.x, self.__last_point.x)
        maxY = max(self.__first_point.y, self.__last_point.y)

        #画出整个屏幕的截图
        dc.DrawBitmap(self.__screen_bitmap, 0, 0)

        #画出阴影部分（截取的部分不需要画）
        dc.SetPen(wx.Pen(color))
        dc.SetBrush(wx.Brush(color))
        dc.DrawRectangle(0, 0, maxX, minY)
        dc.DrawRectangle(maxX, 0, rect.width - maxX, maxY)
        dc.DrawRectangle(minX, maxY, rect.width - minX, rect.height - maxY)
        dc.DrawRectangle(0, minY, minX, rect.height - minY)

        if (self.__on_capture == True):

            #画出截图区域的边框
            dc.SetPen(wx.Pen(wx.Colour(255, 0, 0)))
            dc.SetBrush(wx.Brush(color, wx.TRANSPARENT))
            dc.DrawRectangle(minX, minY, maxX - minX, maxY - minY)

            #显示信息
            dc.SetBrush(wx.Brush(wx.Colour(255, 0, 0)))
            dc.DrawRectangleList([(minX - 2, minY - 2, 5, 5),
                                  (maxX / 2 + minX / 2 - 2, minY - 2, 5, 5),
                                  (maxX - 2, minY - 2, 5, 5),
                                  (maxX - 2, maxY / 2 + minY / 2 - 2, 5, 5),
                                  (maxX - 2, maxY - 2, 5, 5),
                                  (maxX / 2 + minX / 2 - 2, maxY - 2, 5, 5),
                                  (minX - 2, maxY - 2, 5, 5),
                                  (minX - 2, maxY / 2 + minY / 2 - 2, 5, 5)])
            color = wx.Colour(0, 0, 0, 180)
            dc.SetPen(wx.Pen(color))
            dc.SetBrush(wx.Brush(color, wx.SOLID))
            w, h = 140, 43
            s = u'区域大小：' + str(maxX - minX) + '*' + str(maxY - minY)
            s += u'\n鼠标位置：（' + str(self.__last_point.x) + ',' + str(
                self.__last_point.y) + ')'
            dc.DrawRectangle(minX, minY - h - 5 if minY - 5 > h else minY + 5,
                             w, h)
            dc.SetTextForeground(wx.Colour(255, 255, 255))
            dc.DrawText(s, minX + 5,
                        (minY - h - 5 if minY - 5 > h else minY + 5) + 5)

    def OnMouseLeftDown(self, evt):
        # self.__parent_frame.Hide()
        self.__on_capture = True
        self.__first_point = evt.GetPosition()
        self.__last_point = evt.GetPosition()

    def OnMouseLeftUp(self, evt):
        if (self.__on_capture):
            self.__last_point = evt.GetPosition()
            if (self.__first_point.x == self.__last_point.x) and \
                (self.__first_point.y == self.__last_point.y):
                wx.MessageBox(u"区域设置不正确", "Error", wx.OK | wx.ICON_ERROR, self)
                self.__on_capture = False
                self.__first_point = wx.Point(0, 0)  #记录截图的第一个点
                self.__last_point = wx.Point(0, 0)  #记录截图的最后一个点

            else:
                self.__parent_frame.ProcessGrabBitmap(
                    self.__screen_bitmap.GetSubBitmap(
                        wx.Rect(
                            min(self.__first_point.x, self.__last_point.x),
                            min(self.__first_point.y, self.__last_point.y),
                            abs(self.__first_point.x - self.__last_point.x),
                            abs(self.__first_point.y - self.__last_point.y))))

                self.Destroy()
                self.__parent_frame.Show()
                # self.__parent_frame.bmp.SaveFile(r'd:\test.jpg', wx.BITMAP_TYPE_JPEG)

    def OnMouseMove(self, evt):
        if (self.__on_capture):
            self.__last_point = evt.GetPosition()
            self.NewUpdate()

    def NewUpdate(self):
        self.RefreshRect(self.GetClientRect(), True)
        self.Update()