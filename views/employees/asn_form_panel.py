import wx
from views.asn_form_panel import AsnFormPanel
import globals as gbl
import lib.ui_lib as uil


class EmpAsnFormPanel(AsnFormPanel):
    def getRec(self, empId):
        return gbl.empRex[empId] if empId else None

    def getEmpLayout(self, panel):
        empLayout = wx.BoxSizer(wx.HORIZONTAL)
        lblPrj = wx.StaticText(panel, wx.ID_ANY, 'Employee: ' + self.rec['name'])
        empLayout.Add(lblPrj, 0, wx.ALL | wx.EXPAND, 5)
        return empLayout

    def getPrjLayout(self, panel):
        prjLayout = wx.BoxSizer(wx.HORIZONTAL)

        value = 'Project: %s' % (self.asn['project'],) if self.asn else 'Project: *'
        lblPrj = wx.StaticText(panel, wx.ID_ANY, value)
        prjLayout.Add(lblPrj, 0, wx.ALL, 5)

        if not self.asn:
            names = [rec['nickname'] for rec in gbl.prjRex.values()]
            self.cboOwner = uil.ObjComboBox(panel,
                                            list(gbl.prjRex.values()),
                                            'nickname',
                                            'Project',
                                             style=wx.CB_READONLY)
            prjLayout.Add(self.cboOwner, 0, wx.ALL | wx.EXPAND, 5)

        return prjLayout

    def processAsn(self):
        from dal.dao import Dao
        import dal.asn_dal as asn_dal

        d = self.formData
        if self.asn is None:
            d['employee_id'] = self.rec['id']
            d['project_id'] = self.cboOwner.getSelectionId()
            result = asn_dal.add(Dao(), d)
            print(result)
        else:
            d['employee_id'] = self.asn['employee_id']
            d['project_id'] = self.asn['project_id']
            result = asn_dal.update(Dao(), self.asn['id'], d)
            print(result)
