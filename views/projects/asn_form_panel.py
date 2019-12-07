import wx
from views.asn_form_panel import AsnFormPanel
import globals as gbl
import lib.ui_lib as uil


class PrjAsnFormPanel(AsnFormPanel):
    def setProps(self, prjId):
        self.ownerRec = gbl.prjRex[prjId] if prjId else None
        self.ownerName = 'Project'
        self.ownerNameFld = 'nickname'
        self.assigneeName = 'Employee'
        self.assigneeNameFld = 'employee'

    def getComboBox(self, panel):
        return uil.ObjComboBox(panel,
                               list(gbl.empRex.values()),
                               'name',
                               'Employee',
                               style=wx.CB_READONLY)

    def processAsn(self):
        from dal.dao import Dao
        import dal.asn_dal as asn_dal

        d = self.formData
        if self.asn is None:
            d['employee_id'] = self.cboOwner.getSelectionId()
            d['project_id'] = self.ownerRec['id']
            result = asn_dal.add(Dao(), d)
            print(result)
        else:
            d['employee_id'] = self.asn['employee_id']
            d['project_id'] = self.asn['project_id']
            result = asn_dal.update(Dao(), self.asn['id'], d)
            print(result)
