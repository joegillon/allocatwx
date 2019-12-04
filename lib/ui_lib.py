import wx
from collections import namedtuple
import globals as gbl
from lib.custom_button import CustomButton

ColDef = namedtuple('ColDef', 'hdr just width fldName stringConverter')
TabDef = namedtuple('TabDef', 'tblName srchFld colDefs dal dlg')


def getToolbarLabel(panel, text):
    font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                   wx.FONTWEIGHT_BOLD)

    lbl = wx.StaticText(panel, wx.ID_ANY, text)
    lbl.SetFont(font)
    lbl.SetForegroundColour('white')
    return lbl


def toolbar_button(panel, label):
    btn = CustomButton(panel, wx.ID_ANY, label)
    font_normal = wx.Font(10,
                          wx.FONTFAMILY_DEFAULT,
                          wx.FONTSTYLE_NORMAL,
                          wx.FONTWEIGHT_BOLD)
    font_hover = wx.Font(10,
                         wx.FONTFAMILY_DEFAULT,
                         wx.FONTSTYLE_NORMAL,
                         wx.FONTWEIGHT_NORMAL)
    btn.set_font(font_normal, hover=font_hover)
    btn.set_foreground_color('#ffffff')
    btn.set_bg_color(gbl.COLOR_SCHEME.btnBg)
    btn.set_cursor(wx.Cursor(wx.CURSOR_HAND))
    if gbl.COLOR_SCHEME.btnGrd:
        btn.set_bg_gradient(gbl.COLOR_SCHEME.btnGrd)
    btn.set_border((1, 'white', 1))
    btn.set_padding((5, 10, 5, 10))

    return btn


def getMonthCtrl(panel, value):
    import wx.lib.masked as masked
    import lib.month_lib as ml

    ctl = masked.TextCtrl(panel, -1, mask='##/##',
                          defaultValue=ml.prettify(value),
                          size=(50, -1),
                          formatcodes='0>')
    ctl.SetFont(wx.Font(9, 70, 90, 90))
    return ctl


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


class ObjComboBox(wx.ComboBox):
    def __init__(self, parent, choices, display_fld, style=None):
        wx.ComboBox.__init__(self, parent, wx.ID_ANY, style=style)

        isDict = isinstance(choices[0], dict)
        for choice in choices:
            show = choice[display_fld] if isDict else getattr(choice, display_fld)
            self.Append(show, choice)

    def getSelectionId(self):
        if self.CurrentSelection == -1:
            return None
        return self.GetClientData(self.GetSelection())['id']


def getWidestTextExtent(font, values):
    dc = wx.ScreenDC()
    dc.SetFont(font)
    result = 0
    for value in values:
        dim = dc.GetTextExtent(value)[0]
        if dim > result:
            result = dim
    return result + (result * .1)


def displayValue(obj, attr):
    if not obj or not obj[attr]:
        return ''
    return obj[attr]


def toYN(value):
    return 'Y' if value else 'N'


def set2compare(s):
    import string

    return s.translate({ord(c): None for c in string.whitespace}).upper()
