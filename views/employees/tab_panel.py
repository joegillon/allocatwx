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
            ColumnDefn('Grade', 'right', 105, 'grade'),
            ColumnDefn('Step', 'right', 100, 'step'),
            ColumnDefn('FTE', 'right', 100, 'fte'),
            ColumnDefn('Notes', 'left', 0, 'notes'),
            ColumnDefn('Investigator', 'right', 120, 'investigator',
                           stringConverter=uil.toYN)
        ])
        self.theList.SetObjects(list(self.rex.values()))

    def getAsnsDlg(self, ownerId=None):
        return EmpDetailDlg(self, -1, 'Employee Details', ownerId)
