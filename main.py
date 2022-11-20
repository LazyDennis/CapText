import wx
from MainFrame import Mainframe


def main():
    
    app = wx.App()
    frame = Mainframe(title='CapText')
    frame.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()