import wx
from utils.custom_button import CustomButton
from models.globals import COLOR_SCHEME


def toolbar_button(panel, label):
    btn = CustomButton(panel, -1, label)
    font_normal = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.FONTWEIGHT_BOLD)
    font_hover = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
    btn.set_font(font_normal, hover=font_hover)
    btn.set_foreground_color('#ffffff')
    btn.set_bg_color(COLOR_SCHEME.btnBg)
    btn.set_cursor(wx.Cursor(wx.CURSOR_HAND))
    if COLOR_SCHEME.btnGrd:
        btn.set_bg_gradient(COLOR_SCHEME.btnGrd)
    btn.set_border((1, 'white', 1))
    btn.set_padding((5, 10, 5, 10))

    return btn
