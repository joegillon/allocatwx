from views.asn_dlg import AsnDlg
from views.projects.asn_form_panel import PrjAsnFormPanel


class PrjAsnDlg(AsnDlg):

    def getPanel(self, prjId, asn):
        return PrjAsnFormPanel(self, prjId, asn)
