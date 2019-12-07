from views.asn_dlg import AsnDlg
from views.employees.asn_form_panel import EmpAsnFormPanel


class EmpAsnDlg(AsnDlg):

    def getPanel(self, ownerId, asn):
        return EmpAsnFormPanel(self, ownerId, asn)
