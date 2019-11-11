import wx

prjRex = []
empRex = []
asnRex = []

PANEL_BG_COLOR = wx.Colour(79, 114, 142)
TOOLBAR_BG_COLOR = wx.Colour(190, 130, 96)
LIST_BG_COLOR = wx.Colour(37, 63, 91)


def getHelpBtn(parent):
    bmp = wx.Bitmap('images/question.png', wx.BITMAP_TYPE_ANY)
    return wx.BitmapButton(parent, wx.ID_ANY, bitmap=bmp,
                           size=(bmp.GetWidth() + 5,
                                 bmp.GetHeight() + 5))


def showListHelp(event):
    msg = ("Left click to select item.\n"
           "Ctrl-left click to select multiple separate items.\n"
           "Shift-left click to select multiple contiguous items.\n"
           "Right click to see Notes.\n"
           "Double click to edit.")
    wx.MessageBox(msg, 'Help', wx.OK | wx.ICON_INFORMATION)
