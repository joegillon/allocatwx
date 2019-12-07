from views.detail_dlg import DetailDlg
from views.projects.form_panel import PrjFormPanel
from views.projects.asn_list_panel import PrjAsnListPanel
import globals as gbl

class PrjDetailDlg(DetailDlg):
    def getPanels(self, prjId):
        prj = gbl.prjRex[prjId] if prjId else None
        frmPanel = PrjFormPanel(self, prj)
        dtlPanel = PrjAsnListPanel(self, prjId)
        return frmPanel, dtlPanel
