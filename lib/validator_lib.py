import re
from collections import namedtuple
import lib.month_lib as ml
import lib.ui_lib as uil

MONTH_PATTERN = r"^[0-9]{2}(0[1-9]|1[0-2])$"
WHOLE_NAME_PATTERN = r"^[A-Z'\-]+,[\s]*[A-Z' \-]+$"
SCALE_100_PATTERN = r"^[0-9][0-9]?$|^100$"
SCALE_15_PATTERN = r"^[0-9]$|^1[0-5]$"


ProjectMatch = namedtuple('ProjectMatch', 'id values ')
EmployeeMatch = namedtuple('EmployeeMatch', 'id names')


def validatePrjName(value, match=None):
    if value is None or value == '':
        return 'Project name required!'

    if match:
        target = uil.set2compare(value)
        if target in match.values:
            if match.values[target] != match.id:
                return 'Project name not unique!'

    return None


def validatePrjNickname(value, match=None):
    if value is None or value == '':
        return 'Project nickname required!'

    if match:
        target = uil.set2compare(value)
        if target in match.values:
            if match.id == 0 or match.values[target] != match.id:
                return 'Project nickname not unique!'

    return None


def validateTimeframe(firstMonth, lastMonth):
    if not re.match(MONTH_PATTERN, firstMonth):
        return 'First month invalid!'

    if not re.match(MONTH_PATTERN, lastMonth):
        return 'Last month invalid!'

    if not ml.isValidSpan(firstMonth, lastMonth):
        return 'First Month must precede Last Month!'

    return None

def validateAsnTimeframe(firstMonth, lastMonth, prj=None):
    errMsg = validateTimeframe(firstMonth, lastMonth)
    if errMsg:
        return errMsg

    if prj:
        if not ml.isInPrjSpan(prj, firstMonth, lastMonth):
            return 'Timeframe outside project timeframe!'

    return None


def validateEmpName(value, match=None):
    if value is None or value == '':
        return 'Employee name required!'

    if match:
        if not re.match(WHOLE_NAME_PATTERN, value.upper()):
            return 'Employee name invalid!'

        target = uil.set2compare(value)
        if target in match.names:
            if match.names[target] != match.id:
                return 'Employee name not unique!'

    return None


def validateGrade(value):
    if not re.match(SCALE_15_PATTERN, value):
        return 'Grade must be number between 0-15!'
    return None


def validateStep(value):
    if not re.match(SCALE_15_PATTERN, value):
        return 'Step must be number between 0-15!'
    return None


def validateFte(value):
    if not re.match(SCALE_100_PATTERN, value):
        return 'FTE must be number between 0-100!'
    return None


def validateInvestigator(value, grade):
    if value == 1 and int(grade) < 13:
        return 'Investigator grade must be >= 13!'
    return None


def validateEffort(value):
    if value is None or value == '':
        return 'Percent effort required!'

    if not re.match(SCALE_100_PATTERN, value):
        return 'Percent effort must be number between 0-100!'

    return None


def showErrMsg(ctl, msg):
    import wx

    ctl.SetFocus()
    wx.MessageBox(msg, 'Error!', wx.ICON_EXCLAMATION | wx.OK)
