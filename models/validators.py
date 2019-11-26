import re
import wx
from utils.strutils import dropAllWhitespace
from models.month import Month

MONTH_PATTERN = r"^(0?[1-9]|1[012])/[0-9]{2}$"
WHOLE_NAME_PATTERN = r"^[A-Z'\-]+,[\s]*[A-Z' \-]+$"
SCALE_100_PATTERN = r"^[0-9][0-9]?$|^100$"
SCALE_15_PATTERN = r"^[0-9]$|^1[0-5]$"


def validatePrjName(value, prjRex=None):
    if value is None or value == '':
        return 'Project name required!'

    if prjRex:
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


def validateEmpName(value, empRex=None):
    if value is None or value == '':
        return 'Employee name required!'

    if empRex:
        if not re.match(WHOLE_NAME_PATTERN, value.upper()):
            return 'Employee name invalid!'

        testNames = [dropAllWhitespace(rec['name'].upper()) for rec in empRex.values()]
        if dropAllWhitespace(value.upper()) in testNames:
            return 'Employee name taken!'

    return None


def validateGrade(value):
    if value and not re.match(SCALE_15_PATTERN, value):
        return 'Grade must be number between 0-15!'
    return None


def validateStep(value):
    if value and not re.match(SCALE_15_PATTERN, value):
        return 'Step must be number between 0-15!'
    return None


def validateFte(value):
    if value and not re.match(SCALE_100_PATTERN, value):
        return 'FTE must be number between 0-100!'
    return None


def validateInvestigator(value):
    pass


def validateEffort(value):
    if value is None or value == '':
        return 'Percent effort required!'

    if not re.match(SCALE_100_PATTERN, value):
        return 'Percent effort must be number between 0-100!'

    return None


def showErrMsg(ctl, msg):
    ctl.SetFocus()
    wx.MessageBox(msg, 'Error!', wx.ICON_EXCLAMATION | wx.OK)
