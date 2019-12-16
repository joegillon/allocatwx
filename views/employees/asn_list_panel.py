from views.asn_list_panel import AsnListPanel
from views.employees.asn_dlg import EmpAsnDlg
from dal.dao import Dao
import dal.emp_dal as emp_dal
import globals as gbl

class EmpAsnListPanel(AsnListPanel):

    def setProps(self, emp_id):
        self.assignee = 'Project'
        self.dlg = EmpAsnDlg
        self.dal = emp_dal
        if emp_id:
            self.asns = emp_dal.getAsns(Dao(), emp_id)
            gbl.empRex[emp_id]['asns'] = self.asns
