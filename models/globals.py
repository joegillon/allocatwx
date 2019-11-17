import wx
from collections import namedtuple

prjRex = []
empRex = []
asnRex = []

Skin = namedtuple('Skin', [
    'pnlBg', 'tbBg', 'tbFg', 'lstBg', 'lstHdr', 'lstSel',
    'frmBg', 'btnBg', 'btnGrd', 'grdLblBg', 'grdCellBg',
])

SKINS = {
    'Antique': Skin(
        pnlBg='#6e7376',
        tbBg='#155765',
        tbFg='white',
        lstBg='#6e7376',
        lstHdr='#57652a',
        lstSel='#ab9353',
        frmBg='#f7f7f7',
        btnBg='#155765',
        btnGrd='',
        grdLblBg='#6d7993',
        grdCellBg='white'
    ),
    'Forest': Skin(
        pnlBg='#015249',
        tbBg='#57bc90',
        tbFg='white',
        lstBg='#015249',
        lstHdr='#a5a5af',
        lstSel='#a5a5af',
        frmBg='wheat',
        btnBg='#57bc90',
        btnGrd=('#57bc90', '#008080'),
        grdLblBg='#d5d5d5',
        grdCellBg='#6d7993'
    ),
    'Dusty': Skin(
        pnlBg='#9099a2',
        tbBg='#96858f',
        tbFg='white',
        lstBg='#6d7993',
        lstHdr='#a5a5af',
        lstSel='#a5a5af',
        frmBg='#d5d5d5',
        btnBg='#96858f',
        btnGrd='',
        grdLblBg='#d5d5d5',
        grdCellBg='#6d7993'
    ),
    'QED': Skin(
        pnlBg='#173843',
        tbBg='#3fb0ac',
        tbFg='white',
        lstBg='#dddfd4',
        lstHdr='#fae596',
        lstSel='#173843',
        frmBg='#dddfd4',
        btnBg='#3fb0ac',
        btnGrd='',
        grdLblBg='#fae596',
        grdCellBg='#dddfd4'
    ),
    'Saints': Skin(
        pnlBg='#373737',
        tbBg='#c0b283',
        tbFg='white',
        lstBg='#f4f4f4',
        lstHdr='#dcd0c0',
        lstSel='#173843',
        frmBg='#f4f4f4',
        btnBg='#c0b283',
        btnGrd='',
        grdLblBg='#dcd0c0',
        grdCellBg='#f4f4f4'
    ),
    'Light': Skin(
        pnlBg='white',
        tbBg='#cbe4e7',
        tbFg='NAVY',
        lstBg='#e5f9fa',
        lstHdr='#cbe4e7',
        lstSel='#173843',
        frmBg='#e5f9fa',
        btnBg='#6eb6ff',
        btnGrd=('#6eb6ff', 'blue'),
        grdLblBg='#cbe4e7',
        grdCellBg='#e5f9fa'
    ),
    'Mauve': Skin(
        pnlBg='#c2d4d8',
        tbBg='#b0aac2',
        tbFg='white',
        lstBg='#f2efe8',
        lstHdr='#dbe9d8',
        lstSel='#173843',
        frmBg='#f2efe8',
        btnBg='#b0aac2',
        btnGrd='',
        grdLblBg='#dbe9d8',
        grdCellBg='#f2efe8'
    ),
    'Monkey': Skin(
        pnlBg='#a8b6bf',
        tbBg='#7d4627',
        tbFg='white',
        lstBg='#edd9c0',
        lstHdr='#c9d8c5',
        lstSel='#173843',
        frmBg='#edd9c0',
        btnBg='#7d4627',
        btnGrd='',
        grdLblBg='#c9d8c5',
        grdCellBg='#edd9c0'
    ),
    'Sandy': Skin(
        pnlBg='#d5a458',
        tbBg='#0f2043',
        tbFg='white',
        lstBg='white',
        lstHdr='#79cedc',
        lstSel='#173843',
        frmBg='white',
        btnBg='#0f2043',
        btnGrd='',
        grdLblBg='#79cedc',
        grdCellBg='white'
    ),
    'Tan': Skin(
        pnlBg='#07889b',
        tbBg='#eeaa7b',
        tbFg='white',
        lstBg='white',
        lstHdr='#66b9bf',
        lstSel='#173843',
        frmBg='white',
        btnBg='#eeaa7b',
        btnGrd='',
        grdLblBg='#66b9bf',
        grdCellBg='white'
    ),
    'Seafoam': Skin(
        pnlBg='#003B46',
        tbBg='#07575B',
        tbFg='white',
        lstBg='#C4DFE6',
        lstHdr='#66A5AD',
        lstSel='#173843',
        frmBg='#C4DFE6',
        btnBg='#66A5AD',
        btnGrd='',
        grdLblBg='#66A5AD',
        grdCellBg='#C4DFE6'
    ),
}
COLOR_SCHEME = SKINS['Seafoam']

EMP_NAME_WIDTH = 0
PRJ_NICKNAME_WIDTH = 0

def getHelpBtn(parent):
    bmp = wx.Bitmap('images/question.png', wx.BITMAP_TYPE_ANY)
    return wx.BitmapButton(parent, wx.ID_ANY, bitmap=bmp,
                           size=(bmp.GetWidth() + 5,
                                 bmp.GetHeight() + 5))


def showListHelp(event):
    msg = ("Left click to select item.\n"
           "Ctrl-left click to select multiple separate items.\n"
           "Shift-left click to select multiple contiguous items.\n"
           "Right click to see Notes.\n"
           "Double click to edit.")
    wx.MessageBox(msg, 'Help', wx.OK | wx.ICON_INFORMATION)
