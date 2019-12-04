from ObjectListView import ColumnDefn
import globals as gbl
import dal.emp_dal as emp_dal
import lib.ui_lib as uil
from views.employees.detail_dlg import EmpDetailDlg

class EmpTabDef(object):
    def __init__(self):
        self.tblName = 'Employee'
        self.srchFld = 'name'
        self.colDefs = [
            ColumnDefn('Name', 'left', gbl.widestEmpName, 'name'),
            ColumnDefn('Grade', 'right', 105, 'grade'),
            ColumnDefn('Step', 'right', 100, 'step'),
            ColumnDefn('FTE', 'right', 100, 'fte'),
            ColumnDefn('Notes', 'left', 0, 'notes'),
            ColumnDefn('Investigator', 'right', 120, 'investigator',
                           stringConverter=uil.toYN)
        ]
        self.dal = emp_dal
        self.dlg = EmpDetailDlg
