import wx
from datetime import date, timedelta, datetime


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
    if len(month) != 4:
        return month
    return month[2:] + '/' + month[0:2]


def monthUglify(month):
    if len(month) != 5:
        return month
    return month[3:] + month[0:2]


def displayValue(obj, attr):
    if not obj or not obj[attr]:
        return ''
    return obj[attr]


def toYN(value):
    return 'Y' if value else 'N'


def datePlus(d, nmonths):
    return (d + timedelta(nmonths * 365 / 12)).strftime('%m/%y')

def d2myr(d):
    return d.strftime('%m/%y')

def myr2d(myr):
    return datetime.strptime(myr, '%m/%y')
