import wx

from Ui.CaptureToolFrame import CaptureToolFrame


CURSOR_SIZE_DEFAULT = 0
CURSOR_SIZE_MOVE = 1
CURSOR_SIZE_NWSE = 2
CURSOR_SIZE_NESW = 3
CURSOR_SIZE_WE = 4
CURSOR_SIZE_NS = 5

class GrabFrame(wx.Frame):

    def __init__(self, parent, _screen_bitmap: wx.Bitmap, size: wx.Size, pos: wx.Position=(0, 0)):
        super().__init__(None,
                         wx.ID_ANY,
                         pos=pos,
                         size=size,
                         style=wx.NO_BORDER | wx.STAY_ON_TOP | wx.WANTS_CHARS)
        from Ui.MainFrame import Mainframe
        ###################################全局变量########################################
        self.__first_point: wx.Point = wx.Point(0, 0)  #记录截图的第一个点
        self.__last_point: wx.Point = wx.Point(0, 0)  #记录截图的最后一个点
        self.__mouse_pos: wx.Point = wx.Point(0, 0) #记录鼠位置
        self.__on_rect_draw: bool = False  #记录是否是否在画截图区域
        self.__rect_drawn: bool = False #记录是否已画截图区域
        self.__parent_frame: Mainframe = parent
        self.__screen_bitmap: wx.Bitmap = _screen_bitmap
        self.__capture_rect: wx.Rect = wx.Rect()
        self.__size_type = CURSOR_SIZE_DEFAULT
        
        self.__keymap = {
            wx.WXK_ESCAPE: {
                'handler': self.Exit,
                'id': wx.ID_ANY
            }
        }

        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.Bind(wx.EVT_PAINT, self.__OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.__OnMouseLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.__OnMouseLeftUp)
        self.Bind(wx.EVT_MOTION, self.__OnMouseMove)
        self.Bind(wx.EVT_CHAR, self.__OnChar)
        self.Bind(wx.EVT_RIGHT_UP, self.Exit)
        self.Raise()
        self.Show()

    def __OnPaint(self, _evt):
        dc = wx.GCDC(wx.BufferedPaintDC(self))
        self.__PaintUpdate(dc)

    def __PaintUpdate(self, _dc: wx.GCDC):
        rect: wx.Rect = self.GetClientRect()
        
        #画出整个屏幕的截图
        _dc.DrawBitmap(self.__screen_bitmap, 0, 0)        
        
        #画出信息区域
        color = wx.Colour(0, 0, 0, 180)
        _dc.SetPen(wx.Pen(color))
        _dc.SetBrush(wx.Brush(color, wx.SOLID))
        info_text = '(' + str(self.__mouse_pos.x) + ', ' + str(
            self.__mouse_pos.y) + ')'
        info_width, info_height = _dc.GetTextExtent(info_text) #信息区域大小
        
        _dc.SetTextForeground(wx.Colour(255, 255, 255))

        info_x = self.__mouse_pos.x + 20 \
                if self.__mouse_pos.x + info_width + 20 < self.__screen_bitmap.GetSize().GetWidth() \
                else self.__mouse_pos.x - info_width - 5
        info_y = self.__mouse_pos.y + 20 \
                if self.__mouse_pos.y + info_height + 20 < self.__screen_bitmap.GetSize().GetHeight() \
                else self.__mouse_pos.y - info_height
        _dc.DrawRectangle(info_x, info_y, info_width, info_height)
        _dc.DrawText(info_text, info_x, info_y)

        
        color = wx.Colour(0, 0, 0, 120)
        _dc.SetPen(wx.Pen(color))
        _dc.SetBrush(wx.Brush(color))

        if self.__on_rect_draw or self.__rect_drawn:
            if self.__on_rect_draw:
                if self.__size_type == CURSOR_SIZE_DEFAULT:
                    lefttop_x = min(self.__first_point.x, self.__last_point.x)
                    lefttop_y = min(self.__first_point.y, self.__last_point.y)
                    bottomright_x = max(self.__first_point.x, self.__last_point.x)
                    bottomright_y = max(self.__first_point.y, self.__last_point.y)
                    
                    self.__capture_rect.SetTopLeft((lefttop_x, lefttop_y))
                    self.__capture_rect.SetBottomRight((bottomright_x, bottomright_y))
                elif self.__size_type == CURSOR_SIZE_MOVE:
                    pass
                elif self.__size_type == CURSOR_SIZE_NWSE:
                    pass
                elif self.__size_type == CURSOR_SIZE_NESW:
                    pass
                elif self.__size_type == CURSOR_SIZE_WE:
                    pass
                elif self.__size_type == CURSOR_SIZE_NS:
                    pass
                
                
            #设置绘制截图区域时矩形的点                
            
            minX, minY = self.__capture_rect.GetTopLeft()
            maxX, maxY = self.__capture_rect.GetBottomRight()
            
            #画出阴影部分（截取的部分不需要画）
            _dc.DrawRectangle(0, 0, maxX, minY)
            _dc.DrawRectangle(maxX, 0, rect.width - maxX, maxY)
            _dc.DrawRectangle(minX, maxY, rect.width - minX, rect.height - maxY)
            _dc.DrawRectangle(0, minY, minX, rect.height - minY)

            #画出截图区域的边框
            _dc.SetPen(wx.Pen(wx.Colour(255, 0, 0)))
            _dc.SetBrush(wx.Brush(color, wx.TRANSPARENT))
            _dc.DrawRectangle(self.__capture_rect)

            #显示信息
            _dc.SetBrush(wx.Brush(wx.Colour(255, 0, 0)))
            #画 8个方块点
            _dc.DrawRectangleList([(minX - 2, minY - 2, 5, 5),
                                  (maxX / 2 + minX / 2 - 2, minY - 2, 5, 5),
                                  (maxX - 2, minY - 2, 5, 5),
                                  (maxX - 2, maxY / 2 + minY / 2 - 2, 5, 5),
                                  (maxX - 2, maxY - 2, 5, 5),
                                  (maxX / 2 + minX / 2 - 2, maxY - 2, 5, 5),
                                  (minX - 2, maxY - 2, 5, 5),
                                  (minX - 2, maxY / 2 + minY / 2 - 2, 5, 5)])
        else:
            _dc.DrawRectangle(rect)
        return

    def __OnMouseLeftDown(self, _evt: wx.MouseEvent):
        self.__first_point = _evt.GetPosition()
        self.__rect_drawn = False
        self.__on_rect_draw = True
       
        # if self.__size_type == CURSOR_SIZE_DEFAULT:
        #     self.__first_point = self.__mouse_pos
        # elif self.__size_type == CURSOR_SIZE_MOVE:
        #     self.__mouse_pos = _evt.GetPosition()
        # elif self.__size_type == CURSOR_SIZE_NWSE:
        #     pass
        # elif self.__size_type == CURSOR_SIZE_NESW:
        #     pass
        # elif self.__size_type == CURSOR_SIZE_WE:
        #     pass
        # elif self.__size_type == CURSOR_SIZE_NS:
        #     pass
        
        return
    
    def __OnMouseLeftUp(self, _evt: wx.MouseEvent):
        self.__on_rect_draw = False
        self.__rect_drawn = True
        self.__last_point = _evt.GetPosition()
        self.__tool_frame = CaptureToolFrame(self, self.__capture_rect.GetBottomRight())
        pos: wx.Point = self.__tool_frame.GetPosition() #TODO: 调整位置
        size: wx.Size = self.__tool_frame.GetSize()
        self.__tool_frame.SetPosition(wx.Point(pos.x - size.width, pos.y + 5))
    
        return
    
    def GetCapture(self):
        if (self.__first_point.x == self.__last_point.x) and \
            (self.__first_point.y == self.__last_point.y):
            wx.MessageBox(u"区域设置不正确", "Error", wx.OK | wx.ICON_ERROR, self)
            self.__on_rect_draw = False
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

    def __OnMouseMove(self, _evt: wx.MouseEvent):
        POINT_RANGE = 5
        self.__last_point = _evt.GetPosition()
        if self.__rect_drawn:
            self.__mouse_pos: wx.Point = _evt.GetPosition()
            topleft_x, topleft_y = self.__capture_rect.GetTopLeft()
            bottomright_x, bottomright_y = self.__capture_rect.GetBottomRight()
            mouse_x, mouse_y = self.__mouse_pos.Get()
            
            if (mouse_x in range(topleft_x - POINT_RANGE, topleft_x + POINT_RANGE) and 
                                   mouse_y in range(topleft_y - POINT_RANGE, topleft_y + POINT_RANGE)) or \
                                  (mouse_x in range(bottomright_x - POINT_RANGE + 1, bottomright_x + POINT_RANGE + 1) and 
                                   mouse_y in range(bottomright_y - POINT_RANGE + 1, bottomright_y + POINT_RANGE + 1)):
                self.__size_type = CURSOR_SIZE_NWSE
                self.SetCursor(wx.Cursor(wx.CURSOR_SIZENWSE))
            elif (mouse_x in range(topleft_x - POINT_RANGE, topleft_x + POINT_RANGE) and 
                                   mouse_y in range(bottomright_y - POINT_RANGE + 1, bottomright_y + POINT_RANGE + 1)) or \
                                  (mouse_x in range(bottomright_x - POINT_RANGE + 1, bottomright_x + POINT_RANGE + 1) and 
                                   mouse_y in range(topleft_y - POINT_RANGE, topleft_y + POINT_RANGE)):
                self.__size_type = CURSOR_SIZE_NESW
                self.SetCursor(wx.Cursor(wx.CURSOR_SIZENESW))
            elif (mouse_x in range(topleft_x - POINT_RANGE, topleft_x + POINT_RANGE) or 
                                 mouse_x in range(bottomright_x - POINT_RANGE + 1, bottomright_x + POINT_RANGE + 1)) \
                                 and mouse_y in range(topleft_y + POINT_RANGE, bottomright_y - POINT_RANGE + 1):
                self.__size_type = CURSOR_SIZE_WE
                self.SetCursor(wx.Cursor(wx.CURSOR_SIZEWE))
            elif (mouse_y in range(topleft_y - POINT_RANGE, topleft_y + POINT_RANGE) or
                                 mouse_y in range(bottomright_y - POINT_RANGE + 1, bottomright_y + POINT_RANGE + 1)) \
                                 and mouse_x in range(topleft_x + POINT_RANGE, bottomright_x - POINT_RANGE + 1):
                self.__size_type = CURSOR_SIZE_NS
                self.SetCursor(wx.Cursor(wx.CURSOR_SIZENS))
            elif mouse_x in range(topleft_x + POINT_RANGE, bottomright_x + POINT_RANGE + 1) and \
                                  mouse_y in range(topleft_y + POINT_RANGE, bottomright_y + POINT_RANGE + 1):
                self.__size_type = CURSOR_SIZE_MOVE
                self.SetCursor(wx.Cursor(wx.CURSOR_SIZING))
            else:
                self.__size_type = CURSOR_SIZE_DEFAULT
                self.SetCursor(wx.Cursor(wx.CURSOR_DEFAULT))
            

        self.RefreshRect(self.GetClientRect(), True)
        self.Update()
        return

    def __OnChar(self, _evt: wx.KeyEvent):
        key_code = _evt.GetKeyCode()
        # print(self.__class__, '.__Onchar: ', key_code)
        if key_code in self.__keymap:
            _evt.SetId(self.__keymap[key_code]['id'])
            self.__keymap[key_code]['handler'](_evt)
        else:
            _evt.Skip()
        return

    def Exit(self, _evt=None):
        self.Hide()
        if not self.IsShown():
            self.__parent_frame.Show()
            self.__parent_frame.ShowTuningPanel()
            self.__parent_frame.SetResultBitmap(None)
            self.Close()
        return    