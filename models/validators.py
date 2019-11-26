import re
import wx
from utils.strutils import dropAllWhitespace
from models.month import Month

MONTH_PATTERN = r"^(0?[1-9]|1[012])/[0-9]{2}$"
# MONTH_PATTERN = r"^[0-9]{2}(0?[1-9]|1[012])$"
# NAME_CHAR_PATTERN = r"[A-Z ,\'\-\(\)]"
WHOLE_NAME_PATTERN = r"^[\w'-]+,[\s]+[\w'-]+$"


def validatePrjName(value, prjRex):
    if value is None or value == '':
        return 'Project name required!'

    testNames = [dropAllWhitespace(rec['name'].upper()) for rec in prjRex.values()]
    if dropAllWhitespace(value.upper()) in testNames:
        return 'Project name taken!'

    return None


def validatePrjNickname(value, prjRex):
    if value is None or value == '':
        return 'Project nickname required!'

    testNames = [dropAllWhitespace(rec['nickname'].upper()) for rec in prjRex.values()]
    if dropAllWhitespace(value.upper()) in testNames:
        return 'Project nickname taken!'

    return None


def validateTimeframe(firstMonth, lastMonth, prj=None):
    if not re.match(MONTH_PATTERN, firstMonth):
        return 'First month invalid!'

    if not re.match(MONTH_PATTERN, lastMonth):
        return 'Last month invalid!'

    if not Month.isValidSpan(firstMonth, lastMonth):
        return 'First Month must precede Last Month!'

    if prj:
        if not Month.isInPrjSpan(prj, firstMonth, lastMonth):
            return 'Timeframe outside project timeframe!'

    return None


def validateEmpName(value, chk=None):
    if value is None or value == '':
        return 'Employee name required!'

    if chk:
        if not re.match(WHOLE_NAME_PATTERN, value.upper()):
            return 'Employee name invalid!'

    return None


def validateEffort(value):
    if value is None or value == '':
        return 'Percent effort required!'

    if value[0] == '-':
        return 'Percent effort must be between 0-100!'

    if not value.isdigit():
        return 'Percent effort must be numeric!'

    value = int(value)
    if value < 0 or value > 100:
        return 'Percent effort must be between 0-100!'

    return None


def showErrMsg(ctl, msg):
    ctl.SetFocus()
    wx.MessageBox(msg, 'Error!', wx.ICON_EXCLAMATION | wx.OK)
