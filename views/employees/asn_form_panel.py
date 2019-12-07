import wx
from views.asn_form_panel import AsnFormPanel
import globals as gbl
import lib.ui_lib as uil


class EmpAsnFormPanel(AsnFormPanel):
    def setProps(self, empId):
        self.ownerRec = gbl.empRex[empId] if empId else None
        self.ownerName = 'Employee'
        self.ownerNameFld = 'name'
        self.assigneeName = 'Project'
        self.assigneeNameFld = 'project'

    def getComboBox(self, panel):
        return uil.ObjComboBox(panel,
                               list(gbl.prjRex.values()),
                               'nickname',
                               'Project',
                               style=wx.CB_READONLY)

    def processAsn(self):
        from dal.dao import Dao
        import dal.asn_dal as asn_dal

        d = self.formData
        if self.asn is None:
            d['employee_id'] = self.ownerRec['id']
            d['project_id'] = self.cboOwner.getSelectionId()
            result = asn_dal.add(Dao(), d)
            print(result)
        else:
            d['employee_id'] = self.asn['employee_id']
            d['project_id'] = self.asn['project_id']
            result = asn_dal.update(Dao(), self.asn['id'], d)
            print(result)
