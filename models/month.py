from datetime import date, timedelta, datetime
import re

MONTH_FORMAT = '%m/%y'


class Month(object):
    def __init__(self, value):
        value = self.uglify(value)
        self.month = value[0:2]
        self.year = value[3:]

    @staticmethod
    def prettify(month):
        if len(month) != 4:
            return month
        return month[2:] + '/' + month[0:2]

    @staticmethod
    def uglify(month):
        if len(month) != 5:
            return month
        return month[3:] + month[0:2]

    @staticmethod
    def split(month):
        if len(month) != 4:
            return ''
        return month[3:], month[0:2]

    @staticmethod
    def getMonths(startMonth, thruMonth):
        from dateutil.relativedelta import relativedelta as rd

        start_date = Month.month2d(startMonth)
        thru_date = Month.month2d(thruMonth)
        months = []
        while start_date <= thru_date:
            months.append(Month.d2month(start_date))
            start_date = start_date + rd(months=1)
        return months

    @staticmethod
    def datePlus(d, nmonths):
        return (d + timedelta(nmonths * 365 / 12)).strftime(MONTH_FORMAT)

    @staticmethod
    def d2month(d):
        return d.strftime(MONTH_FORMAT)

    @staticmethod
    def month2d(month):
        return datetime.strptime(month, MONTH_FORMAT)

    @staticmethod
    def isValid(s):
        return re.match("^([0]*[1-9]|1[0-2])\/[0-9]{2}$", s)

    @staticmethod
    def isValidSpan(first, last):
        return last >= first

    @staticmethod
    def isInPrjSpan(prj, first_month, last_month):
        if first_month < prj['first_month']:
            return False
        return last_month <= prj['last_month']

    @staticmethod
    def getMonthCtrl(panel, value):
        from wx import Font
        import wx.lib.masked as masked

        ctl = masked.TextCtrl(panel, -1, mask='##/##',
                               defaultValue=Month.prettify(value),
                               size=(50, -1))
        ctl.SetFont(Font(9, 70, 90, 90))
        return ctl
