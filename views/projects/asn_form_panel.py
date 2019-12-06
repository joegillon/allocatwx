import wx
from views.asn_form_panel import AsnFormPanel
import globals as gbl
import lib.ui_lib as uil


class PrjAsnFormPanel(AsnFormPanel):
    def getRec(self, prjId):
        return gbl.prjRex[prjId] if prjId else None

    def getEmpLayout(self, panel):
        empLayout = wx.BoxSizer(wx.HORIZONTAL)

        value = 'Employee: %s' % (self.asn['employee'],) if self.asn else 'Employee: *'
        lblEmp = wx.StaticText(panel, wx.ID_ANY, value)
        empLayout.Add(lblEmp, 0, wx.ALL, 5)

        if not self.asn:
            self.cboOwner = uil.ObjComboBox(panel,
                                            list(gbl.empRex.values()),
                                            'name',
                                            'Employee',
                                            style=wx.CB_READONLY)
            empLayout.Add(self.cboOwner, 0, wx.ALL | wx.EXPAND, 5)

        return empLayout

    def getPrjLayout(self, panel):
        prjLayout = wx.BoxSizer(wx.HORIZONTAL)
        lblPrj = wx.StaticText(panel, wx.ID_ANY, 'Project: ' + self.rec['nickname'])
        prjLayout.Add(lblPrj, 0, wx.ALL | wx.EXPAND, 5)
        return prjLayout

    def processAsn(self):
        from dal.dao import Dao
        import dal.asn_dal as asn_dal

        d = self.formData
        if self.asn is None:
            d['employee_id'] = self.cboOwner.getSelectionId()
            d['project_id'] = self.rec['id']
            result = asn_dal.add(Dao(), d)
            print(result)
        else:
            d['employee_id'] = self.asn['employee_id']
            d['project_id'] = self.asn['project_id']
            result = asn_dal.update(Dao(), self.asn['id'], d)
            print(result)
