from views.asn_list_panel import AsnListPanel
from views.projects.asn_dlg import PrjAsnDlg
import dal.prj_dal as prj_dal


class PrjAsnListPanel(AsnListPanel):

    def setProps(self, prjId):
        self.assignee = 'Employee'
        self.dlg = PrjAsnDlg
        self.dal = prj_dal
