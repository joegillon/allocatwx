from views.detail_dlg import DetailDlg
from views.asn_list_panel import AsnListPanel
from views.employees.frm_panel import EmpFormPanel
from views.employees.asn_dlg import EmpAsnDlg
import dal.emp_dal as emp_dal
import globals as gbl


class EmpDetailDlg(DetailDlg):
    def getPanels(self, empId, asns):
        frmPanel = EmpFormPanel(self, empId)
        dtlPanel = AsnListPanel(self,
                                'Project',
                                gbl.empRex[empId],
                                asns,
                                EmpAsnDlg,
                                emp_dal)
        return frmPanel, dtlPanel
