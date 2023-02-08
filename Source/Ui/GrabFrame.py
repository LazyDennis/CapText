import wx

from Ui.CaptureToolFrame import CaptureToolFrame
from GlobalVars import RectanglePositon as RectPos


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
        self.__rect_is_drawn: bool = False #记录是否已画截图区域
        self.__parent_frame: Mainframe = parent
        self.__screen_bitmap: wx.Bitmap = _screen_bitmap
        self.__capture_rect: wx.Rect = wx.Rect()
        
        self.__rect_pos = RectPos.EXTERNAL
        self.__on_rect_adjust = False #截图区域大小调整中
        self.__tool_frame = None
        
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
        self.Bind(wx.EVT_LEFT_DCLICK, self.__OnMouseDoubleClick)
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
        
        color = wx.Colour(0, 0, 0, 120)
        _dc.SetPen(wx.Pen(color))
        _dc.SetBrush(wx.Brush(color))

        if self.__on_rect_draw or self.__rect_is_drawn:
            if not self.__rect_is_drawn:
                self.__last_point = self.__mouse_pos
                # print('rect on draw, last point: ', self.__last_point)
                minX = min(self.__first_point.x, self.__last_point.x)
                minY = min(self.__first_point.y, self.__last_point.y)
                maxX = max(self.__first_point.x, self.__last_point.x)
                maxY = max(self.__first_point.y, self.__last_point.y)
                self.__capture_rect.SetTopLeft((minX, minY))
                self.__capture_rect.SetBottomRight((maxX, maxY))  
                pass
                
            elif self.__on_rect_adjust:
                if self.__rect_pos == RectPos.INTERNAL:
                    # print('internal_adjust')
                    self.__last_point = self.__mouse_pos
                    rect_topleft: wx.Point = self.__capture_rect.GetTopLeft()
                    rect_bottomright: wx.Point = self.__capture_rect.GetBottomRight()
                    minX = rect_topleft.x + self.__last_point.x - self.__first_point.x
                    minY = rect_topleft.y + self.__last_point.y - self.__first_point.y
                    maxX = rect_bottomright.x + self.__last_point.x - self.__first_point.x
                    maxY = rect_bottomright.y + self.__last_point.y - self.__first_point.y
                    # print((minX, minY), (maxX, maxY), self.__capture_rect.GetSize(), self.__screen_bitmap.GetSize())
                    
                    if minX < 0:
                        minX = 0
                        maxX = self.__capture_rect.GetWidth() - 1
                    if minY < 0:
                        minY = 0
                        maxY = self.__capture_rect.GetHeight() - 1
                    if maxX > self.__screen_bitmap.GetWidth():
                        # print('maxX > screenbitmap.width')
                        maxX = self.__screen_bitmap.GetWidth()
                        minX = maxX - self.__capture_rect.GetWidth() + 1
                    if maxY > self.__screen_bitmap.GetHeight():
                        # print('maxX > screenbitmap.height')
                        maxY = self.__screen_bitmap.GetHeight()
                        minY = maxY - self.__capture_rect.GetHeight() + 1
                    # print((minX, minY), (maxX, maxY), self.__capture_rect.GetSize())
                    self.__capture_rect.SetTopLeft((minX, minY))
                    self.__capture_rect.SetBottomRight((maxX, maxY))  
                    self.__first_point = self.__last_point
                    pass
                else:
                    if self.__rect_pos == RectPos.EXTERNAL:
                        # print('external_adjust')
                        self.__on_rect_draw = True
                        self.__rect_is_drawn = False
                        self.__on_rect_adjust = False
                        pass

                    elif self.__rect_pos == RectPos.LEFT:
                        # print('left_adjust')
                        self.__last_point = wx.Point(
                            self.__mouse_pos.x, 
                            self.__capture_rect.GetTop()
                        )
                        pass
                    elif self.__rect_pos == RectPos.RIGHT:
                        # print('right_adjust')
                        self.__last_point = wx.Point(
                            self.__mouse_pos.x,
                            self.__capture_rect.GetBottom()
                        )
                        pass
                    elif self.__rect_pos == RectPos.TOP:
                        # print('top_adjust')
                        self.__last_point = wx.Point(
                            self.__capture_rect.GetLeft(),
                            self.__mouse_pos.y
                        )
                        pass
                    elif self.__rect_pos == RectPos.BOTTOM:
                        # print('bottom_adjust')
                        self.__last_point = wx.Point(
                            self.__capture_rect.GetRight(),
                            self.__mouse_pos.y
                        )
                        pass
                    elif self.__rect_pos == RectPos.TOPLEFT:
                        # print('topleft_adjust')
                        self.__last_point = self.__mouse_pos
                        pass
                    elif self.__rect_pos == RectPos.BOTTOMRIGHT:
                        # print('bottomright_adjust')
                        self.__last_point = self.__mouse_pos
                        pass
                    elif self.__rect_pos == RectPos.TOPRIGHT:
                        # print('topright_adjust')
                        self.__last_point = self.__mouse_pos
                        pass
                    elif self.__rect_pos == RectPos.BOTTOMLEFT:
                        # print('bottomleft_adjust')
                        self.__last_point = self.__mouse_pos
                        pass

                    minX = min(self.__first_point.x, self.__last_point.x)
                    minY = min(self.__first_point.y, self.__last_point.y)
                    maxX = max(self.__first_point.x, self.__last_point.x)
                    maxY = max(self.__first_point.y, self.__last_point.y)
                    # print((minX, minY), (maxX, maxY))
                    self.__capture_rect.SetTopLeft((minX, minY))
                    self.__capture_rect.SetBottomRight((maxX, maxY))    
                    
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

        #画出信息区域
        self.__DrawInfo(_dc)
        
        return

    def __DrawInfo(self, _dc: wx.DC):
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

        return

    def __OnMouseLeftDown(self, _evt: wx.MouseEvent):
        if self.__rect_is_drawn:
            self.__on_rect_adjust = True
        
            if self.__rect_pos == RectPos.EXTERNAL:
                # print('external_adjust')
                self.__on_rect_draw = True
                self.__rect_is_drawn = False
                self.__on_rect_adjust = False
                self.__first_point = _evt.GetPosition()
                # topleft_x = min(self.__first_point.x, self.__last_point.x)
                # topleft_y = min(self.__first_point.y, self.__last_point.y)
                # bottomright_x = max(self.__first_point.x, self.__last_point.x)
                # bottomright_y = max(self.__first_point.y, self.__last_point.y)

            elif self.__rect_pos == RectPos.INTERNAL:
                # print('internal_adjust')
                self.__first_point = _evt.GetPosition()
                pass
            elif self.__rect_pos == RectPos.LEFT:
                # print('leftup left_adjust')
                self.__first_point = self.__capture_rect.GetBottomRight()
                pass
            elif self.__rect_pos == RectPos.RIGHT:
                # print('leftup right_adjust')
                self.__first_point = self.__capture_rect.GetTopLeft()
                pass
            elif self.__rect_pos == RectPos.TOP:
                # print('leftup top_adjust')
                self.__first_point = self.__capture_rect.GetBottomRight()
                pass
            elif self.__rect_pos == RectPos.BOTTOM:
                # print('leftup bottom_adjust')
                self.__first_point = self.__capture_rect.GetTopLeft()
                pass
            elif self.__rect_pos == RectPos.TOPLEFT:
                # print('leftup topleft_adjust')
                self.__first_point = self.__capture_rect.GetBottomRight()
                pass
            elif self.__rect_pos == RectPos.BOTTOMRIGHT:
                # print('leftup bottomright_adjust')
                self.__first_point = self.__capture_rect.GetTopLeft()
                pass
            elif self.__rect_pos == RectPos.TOPRIGHT:
                # print('leftup topright_adjust')
                self.__first_point = self.__capture_rect.GetBottomLeft()
                pass
            elif self.__rect_pos == RectPos.BOTTOMLEFT:
                self.__first_point = self.__capture_rect.GetTopRight()
                pass
        else:
            self.__on_rect_draw = True
            self.__first_point = _evt.GetPosition()
            # print('rect_on_draw, first point: ', self.__first_point)

        return
    
    def __OnMouseLeftUp(self, _evt: wx.MouseEvent):
        self.__on_rect_draw = False
        self.__rect_is_drawn = True
        self.__on_rect_adjust = False
        
        if self.__tool_frame is None:
            self.__tool_frame = CaptureToolFrame(self)
        self.__SetToolFramePosition()
        return
    
    def __SetToolFramePosition(self):
        # pos: wx.Point = self.__tool_frame.GetPosition() #TODO: 调整位置
        tool_frame_size: wx.Size = self.__tool_frame.GetSize()
        # print(tool_frame_size, self.__capture_rect.Get())
        tool_frame_pos = wx.Point()
        if (self.GetSize().GetHeight() > 
            self.__capture_rect.GetBottom() + tool_frame_size.GetHeight() + 5):
            tool_frame_pos.x = self.__capture_rect.GetRight() - tool_frame_size.GetWidth()
            tool_frame_pos.y = self.__capture_rect.GetBottom() + 5
        elif (0 < 
              self.__capture_rect.GetTop() - tool_frame_size.GetHeight() - 5):
            tool_frame_pos.x = self.__capture_rect.GetRight() - tool_frame_size.GetWidth()
            tool_frame_pos.y = self.__capture_rect.GetTop() - tool_frame_size.GetHeight() - 5
        elif (self.GetSize().GetWidth() >
              self.__capture_rect.GetRight() + tool_frame_size.GetWidth() + 5):
            tool_frame_pos.x = self.__capture_rect.GetRight() + 5
            tool_frame_pos.y = self.__capture_rect.GetBottom() - tool_frame_size.GetHeight() - 5
        elif (0 <
              self.__capture_rect.GetLeft() - tool_frame_size.GetWidth() - 5):
            tool_frame_pos.x = self.__capture_rect.GetLeft() - tool_frame_size.GetWidth() - 5
            tool_frame_pos.y = self.__capture_rect.GetBottom() - tool_frame_size.GetHeight()
        else:
            tool_frame_pos.x = self.__capture_rect.GetRight() - tool_frame_size.GetWidth() - 5
            tool_frame_pos.y = self.__capture_rect.GetBottom() - tool_frame_size.GetHeight() - 5
        
        tool_frame_pos.x += self.GetPosition().x
        tool_frame_pos.y += self.GetPosition().y
        
        self.__tool_frame.SetPosition(tool_frame_pos)
        self.__tool_frame.Raise()
        # print(self.__tool_frame.GetPosition(), self.GetPosition())
        
        return
    
    def __OnMouseDoubleClick(self, _evt: wx.MouseEvent):
        if not self.__capture_rect.IsEmpty():
            self.GetCapture()
            # self.Close()
        return
    
    def GetCapture(self):
        if self.__capture_rect.IsEmpty():
            self.__parent_frame.ProcessGrabBitmap(None)
        else:
            self.__parent_frame.ProcessGrabBitmap(
                self.__screen_bitmap.GetSubBitmap(self.__capture_rect))

    def __OnMouseMove(self, _evt: wx.MouseEvent):
        POINT_RANGE = 5
        self.__mouse_pos: wx.Point = _evt.GetPosition()
        if self.__on_rect_draw:
            self.__last_point = self.__mouse_pos
        elif self.__rect_is_drawn and not self.__on_rect_adjust:
            # self.__mouse_pos: wx.Point = _evt.GetPosition()
            topleft_x, topleft_y = self.__capture_rect.GetTopLeft()
            bottomright_x, bottomright_y = self.__capture_rect.GetBottomRight()
            mouse_x, mouse_y = self.__mouse_pos.Get()
            
            # print((topleft_x, topleft_y), (bottomright_x, bottomright_y), self.__mouse_pos)
            if (mouse_x in range(topleft_x - POINT_RANGE, topleft_x + POINT_RANGE + 1) and 
                mouse_y in range(topleft_y - POINT_RANGE, topleft_y + POINT_RANGE + 1)):
                # print('mouse at topleft')
                self.__rect_pos = RectPos.TOPLEFT                
                self.SetCursor(wx.Cursor(wx.CURSOR_SIZENWSE))
            elif (mouse_x in range(bottomright_x - POINT_RANGE, bottomright_x + POINT_RANGE + 1) and 
                  mouse_y in range(bottomright_y - POINT_RANGE, bottomright_y + POINT_RANGE + 1)):
                # print('mouse at bottomright')
                self.__rect_pos = RectPos.BOTTOMRIGHT                
                self.SetCursor(wx.Cursor(wx.CURSOR_SIZENWSE))
            elif (mouse_x in range(topleft_x - POINT_RANGE, topleft_x + POINT_RANGE + 1) and 
                  mouse_y in range(bottomright_y - POINT_RANGE, bottomright_y + POINT_RANGE + 1)):
                # print('mouse at bottomleft')
                self.__rect_pos = RectPos.BOTTOMLEFT                
                self.SetCursor(wx.Cursor(wx.CURSOR_SIZENESW))            
            elif (mouse_x in range(bottomright_x - POINT_RANGE, bottomright_x + POINT_RANGE + 1) and 
                  mouse_y in range(topleft_y - POINT_RANGE, topleft_y + POINT_RANGE + 1)):
                # print('mouse at topright')
                self.__rect_pos = RectPos.TOPRIGHT                
                self.SetCursor(wx.Cursor(wx.CURSOR_SIZENESW))
            elif (mouse_x in range(topleft_x - POINT_RANGE, topleft_x + POINT_RANGE + 1) and 
                  mouse_y in range(topleft_y + POINT_RANGE + 1, bottomright_y - POINT_RANGE)):
                # print('mouse at left')
                self.__rect_pos = RectPos.LEFT                
                self.SetCursor(wx.Cursor(wx.CURSOR_SIZEWE))                 
            elif (mouse_x in range(bottomright_x - POINT_RANGE, bottomright_x + POINT_RANGE + 1) and
                  mouse_y in range(topleft_y + POINT_RANGE + 1, bottomright_y - POINT_RANGE)):
                # print('mouse at right')
                self.__rect_pos = RectPos.RIGHT                
                self.SetCursor(wx.Cursor(wx.CURSOR_SIZEWE))
            elif (mouse_y in range(topleft_y - POINT_RANGE, topleft_y + POINT_RANGE + 1) and
                  mouse_x in range(topleft_x + POINT_RANGE + 1, bottomright_x - POINT_RANGE)):
                # print('mouse at top')
                self.__rect_pos = RectPos.TOP                
                self.SetCursor(wx.Cursor(wx.CURSOR_SIZENS))
            elif (mouse_y in range(bottomright_y - POINT_RANGE, bottomright_y + POINT_RANGE + 1) and
                  mouse_x in range(topleft_x + POINT_RANGE + 1, bottomright_x - POINT_RANGE)):
                # print('mouse at bottom')
                self.__rect_pos = RectPos.BOTTOM                
                self.SetCursor(wx.Cursor(wx.CURSOR_SIZENS))
            elif (mouse_x in range(topleft_x + POINT_RANGE + 1, bottomright_x - POINT_RANGE) and 
                  mouse_y in range(topleft_y + POINT_RANGE + 1, bottomright_y - POINT_RANGE)):
                # print('mouse at internal')
                self.__rect_pos = RectPos.INTERNAL                
                self.SetCursor(wx.Cursor(wx.CURSOR_SIZING))
            else:
                # print('mouse at external')
                self.__rect_pos = RectPos.EXTERNAL                
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