import wx
from ObjectListView import ColumnDefn
import globals as gbl
import lib.ui_lib as uil
from views.tab_panel import TabPanel
from views.employees.detail_dlg import EmpDetailDlg


class EmpTabPanel(TabPanel):

    def setProps(self):
        self.srchFld = 'Name'
        self.ownerName = 'Employee'
        self.rex = gbl.empRex

    def buildList(self):
        self.theList.SetColumns([
            ColumnDefn('Name', 'left', gbl.widestEmpName, 'name'),
            ColumnDefn('Grade', 'right', wx.LIST_AUTOSIZE_USEHEADER, 'grade'),
            ColumnDefn('Step', 'right', wx.LIST_AUTOSIZE_USEHEADER, 'step'),
            ColumnDefn('FTE', 'right', wx.LIST_AUTOSIZE_USEHEADER, 'fte'),
            ColumnDefn('Investigator', 'right', wx.LIST_AUTOSIZE_USEHEADER, 'investigator',
                           stringConverter=uil.toYN),
            ColumnDefn('Notes', 'left', 400, 'notes'),
        ])

    def getDetailDlg(self, ownerId=None):
        return EmpDetailDlg(self, -1, 'Employee Details', ownerId)
