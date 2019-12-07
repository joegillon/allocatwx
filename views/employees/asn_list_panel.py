from views.asn_list_panel import AsnListPanel
from views.employees.asn_dlg import EmpAsnDlg
import dal.emp_dal as emp_dal


class EmpAsnListPanel(AsnListPanel):

    def setProps(self, empId):
        self.assignee = 'Project'
        self.dlg = EmpAsnDlg
        self.dal = emp_dal
