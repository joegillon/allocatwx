from ObjectListView import ColumnDefn
import globals as gbl
import lib.month_lib as ml
from views.tab_panel import TabPanel
from views.projects.detail_dlg import PrjDetailDlg


class PrjTabPanel(TabPanel):

    def setProps(self):
        self.srchFld = 'Nickname'
        self.ownerName = 'Project'
        self.rex = gbl.prjRex

    def buildList(self):
        self.theList.SetColumns([
            ColumnDefn('Nickname', 'left', gbl.widestNickname, 'nickname'),
            ColumnDefn('First Month', 'left', 105, 'first_month', stringConverter=ml.prettify),
            ColumnDefn('Last Month', 'left', 100, 'last_month', stringConverter=ml.prettify),
            ColumnDefn('PI', 'left', 150, 'PiName'),
            ColumnDefn('PM', 'left', 150, 'PmName'),
            ColumnDefn('Name', 'left', gbl.widestPrjName, 'name'),
            ColumnDefn('Notes', 'left', 0, 'notes')
        ])

    def getDetailDlg(self, ownerId=None):
        return PrjDetailDlg(self, -1, 'Project Details', ownerId)
