import wx
import GlobalVars
from MainFrame import Mainframe


def main():
    
    app = wx.App()
    frame = Mainframe(title='CapText' + ' ' + GlobalVars.VERSION)
    frame.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()