from views.detail_dlg import DetailDlg
from views.asn_list_panel import AsnListPanel
from views.projects.frm_panel import PrjFormPanel
from views.projects.asn_dlg import PrjAsnDlg
import dal.prj_dal as prj_dal
import globals as gbl

class PrjDetailDlg(DetailDlg):
    def getPanels(self, prjId, asns):
        frmPanel = PrjFormPanel(self, prjId)
        dtlPanel = AsnListPanel(self,
                                'Employee',
                                gbl.prjRex[prjId],
                                asns,
                                PrjAsnDlg,
                                prj_dal)
        return frmPanel, dtlPanel
