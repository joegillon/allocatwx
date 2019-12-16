from views.asn_list_panel import AsnListPanel
from views.projects.asn_dlg import PrjAsnDlg
from dal.dao import Dao
import dal.prj_dal as prj_dal
import globals as gbl


class PrjAsnListPanel(AsnListPanel):

    def setProps(self, prj_id):
        self.assignee = 'Employee'
        self.dlg = PrjAsnDlg
        self.dal = prj_dal
        if prj_id:
            self.asns = prj_dal.getAsns(Dao(), prj_id)
            gbl.prjRex[prj_id]['asns'] = self.asns
