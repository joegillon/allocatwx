from views.detail_dlg import DetailDlg
from views.employees.form_panel import EmpFormPanel
from views.employees.asn_list_panel import EmpAsnListPanel
import globals as gbl


class EmpDetailDlg(DetailDlg):
    def getPanels(self, empId):
        emp = gbl.empRex[empId] if empId else None
        frmPanel = EmpFormPanel(self, emp)
        dtlPanel = EmpAsnListPanel(self, empId)
        return frmPanel, dtlPanel
