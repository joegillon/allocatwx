import wx


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


class EmpNameValidator(wx.PyValidator):
    def __init__(self):
        super(EmpNameValidator, self).__init__()

    def Clone(self):
        return EmpNameValidator

    def Validate(self, win):
        textCtrl = self.GetWindow()
        text = textCtrl.GetValue()

        