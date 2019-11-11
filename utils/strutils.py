import wx


def getWidestTextExtent(font, values):
    dc = wx.ScreenDC()
    dc.SetFont(font)
    result = 0
    for value in values:
        dim = dc.GetTextExtent(value)[0]
        if dim > result:
            result = dim
    return result + (result * .1)


def monthPrettify(month):
    if not month:
        return ''
    return month[2:] + '/' + month[0:2]


def displayValue(obj, attr):
    if not obj or not obj[attr]:
        return ''
    return obj[attr]
