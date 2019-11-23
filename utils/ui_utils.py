import wx
import re
import models.globals as gbl


def scale_bitmap(bitmap, width, height):
    image = wx.ImageFromBitmap(bitmap)
    image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
    result = wx.BitmapFromImage(image)
    return result


def getToolbarLabel(panel, text):
    font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                   wx.FONTWEIGHT_BOLD)

    lbl = wx.StaticText(panel, wx.ID_ANY, text)
    lbl.SetFont(font)
    lbl.SetForegroundColour('white')
    return lbl


class MonthValidator(wx.PyValidator):
    def __init__(self, name):
        wx.PyValidator.__init__(self)
        self.name = name

    def Clone(self):
        return MonthValidator(self.name)

    def Validate(self, win):
        textCtrl = self.GetWindow()
        text = textCtrl.GetValue()

        if len(text) == 0:
            wx.MessageBox('%s required!' % (self.name,), 'Oops!')
            textCtrl.SetBackgroundColour('pink')
            textCtrl.SetFocus()
            textCtrl.Refresh()
            return False
        elif not re.match(text[0:2], gbl.MONTH_PATTERN):
            wx.MessageBox('%s invalid Month!' % (self.name,), 'Oops!')
            textCtrl.SetBackgroundColour('pink')
            textCtrl.SetFocus()
            textCtrl.Refresh()
            return False
        else:
            textCtrl.SetBackgroundColour(
                wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW)
            )
            textCtrl.Refresh()
            return True

    def TransferToWindow(self):
        return True

    def TransferFromWindow(self):
        return True


class PrjNameValidator(wx.PyValidator):
    def __init__(self):
        wx.PyValidator.__init__(self)
        self.name = 'name'

    def Clone(self):
        return PrjNameValidator()

    def Validate(self, win):
        textCtrl = self.GetWindow()
        text = textCtrl.GetValue()

        if len(text) == 0:
            wx.MessageBox('%s required!' % (self.name,), 'Oops!')
            textCtrl.SetBackgroundColour('pink')
            textCtrl.SetFocus()
            textCtrl.Refresh()
            return False
        else:
            textCtrl.SetBackgroundColour(
                wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW)
            )
            textCtrl.Refresh()
            return True

class EmpNameValidator(wx.PyValidator):
    def __init__(self):
        wx.PyValidator.__init__(self)
        self.Bind(wx.EVT_CHAR, self.onChar)

    def Clone(self):
        return EmpNameValidator()

    def Validate(self, win):
        textCtrl = self.GetWindow()
        text = textCtrl.GetValue()

        