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


def displayValue(obj, attr):
    if not obj or not obj[attr]:
        return ''
    return obj[attr]


def toYN(value):
    return 'Y' if value else 'N'

def set2compare(s):
    import string

    return s.translate({ord(c): None for c in string.whitespace}).upper()
