from ObjectListView import ColumnDefn
import globals as gbl
import dal.prj_dal as prj_dal
import lib.month_lib as ml
from views.projects.detail_dlg import PrjDetailDlg

class PrjTabDef(object):
    def __init__(self):
        self.tblName = 'Project'
        self.srchFld = 'nickname'
        self.colDefs = [
            ColumnDefn('Nickname', 'left', gbl.widestNickname, 'nickname'),
            ColumnDefn('First Month', 'left', 105, 'first_month', stringConverter=ml.prettify),
            ColumnDefn('Last Month', 'left', 100, 'last_month', stringConverter=ml.prettify),
            ColumnDefn('PI', 'left', 150, 'PiName'),
            ColumnDefn('PM', 'left', 150, 'PmName'),
            ColumnDefn('Name', 'left', gbl.widestPrjName, 'name'),
            ColumnDefn('Notes', 'left', 0, 'notes')
        ]
        self.dal = prj_dal
        self.dlg = PrjDetailDlg
