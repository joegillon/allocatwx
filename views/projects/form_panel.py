import wx
from views.form_panel import FormPanel
import lib.ui_lib as uil
import globals as gbl
import lib.month_lib as ml
import dal.prj_dal as prj_dal

class PrjFormPanel(FormPanel):

    def setProps(self):
        self.ownerName = 'Project'
        self.dal = prj_dal
        self.rex = gbl.prjRex

        self.txtName = None
        self.txtNickname = None
        self.txtFirstMonth = None
        self.txtLastMonth = None
        self.cboPI = None
        self.cboPM = None
        self.txtNotes = None

    def getLayout(self, panel, prj):
        layout = wx.BoxSizer(wx.VERTICAL)

        nameLayout = wx.BoxSizer(wx.HORIZONTAL)
        lblName = wx.StaticText(panel, wx.ID_ANY, 'Project Name: *')
        self.txtName = wx.TextCtrl(panel, wx.ID_ANY,
                                   uil.displayValue(prj, 'name'),
                                   size=(500, -1))
        nameLayout.Add(lblName, 0, wx.ALL, 5)
        nameLayout.Add(self.txtName, 0, wx.ALL | wx.EXPAND, 5)

        layout.Add(nameLayout, 0, wx.ALL | wx.EXPAND, 5)

        nicknameLayout = wx.BoxSizer(wx.HORIZONTAL)
        lblNickname = wx.StaticText(panel, wx.ID_ANY, 'Nickname: *')
        self.txtNickname = wx.TextCtrl(panel, wx.ID_ANY,
                                       uil.displayValue(prj, 'nickname'), size=(400, -1))
        nicknameLayout.Add(lblNickname, 0, wx.ALL, 5)
        nicknameLayout.Add(self.txtNickname, 0, wx.ALL, 5)

        layout.Add(nicknameLayout, 0, wx.ALL | wx.EXPAND, 5)

        intervalLayout = wx.BoxSizer(wx.HORIZONTAL)
        lblFirstMonth = wx.StaticText(panel, wx.ID_ANY, 'First Month: *')
        value = ml.prettify(uil.displayValue(prj, 'first_month'))
        self.txtFirstMonth = uil.getMonthCtrl(panel, value)
        intervalLayout.Add(lblFirstMonth, 0, wx.ALL, 5)
        intervalLayout.Add(self.txtFirstMonth, 0, wx.ALL, 5)

        lblLastMonth = wx.StaticText(panel, wx.ID_ANY, 'Last Month: *')
        value = ml.prettify(uil.displayValue(prj, 'last_month'))
        self.txtLastMonth = uil.getMonthCtrl(panel, value)
        intervalLayout.Add(lblLastMonth, 0, wx.ALL, 5)
        intervalLayout.Add(self.txtLastMonth, 0, wx.ALL, 5)

        layout.Add(intervalLayout, 0, wx.ALL, 5)

        personsLayout = wx.BoxSizer(wx.HORIZONTAL)

        lblPI = wx.StaticText(panel, wx.ID_ANY, 'PI:')
        pis = [rec for rec in gbl.empRex.values() if rec['investigator'] == 1]
        self.cboPI = uil.ObjComboBox(panel,
                                     pis,
                                     'name',
                                     'Employee',
                                     style=wx.CB_READONLY)
        value = self.ownerRec['PiName'] \
            if self.ownerRec and self.ownerRec['PI'] else ''
        self.cboPI.SetValue(value)
        personsLayout.Add(lblPI, 0, wx.ALL, 5)
        personsLayout.Add(self.cboPI, 0, wx.ALL, 5)

        lblPM = wx.StaticText(panel, wx.ID_ANY, 'PM:')
        pms = [rec for rec in gbl.empRex.values() if rec['investigator'] == 0]
        self.cboPM = uil.ObjComboBox(panel,
                                     pms,
                                     'name',
                                     'Employee',
                                     style=wx.CB_READONLY)
        value = self.ownerRec['PmName'] \
            if self.ownerRec and self.ownerRec['PM'] else ''
        self.cboPM.SetValue(value)
        personsLayout.Add(lblPM, 0, wx.ALL, 5)
        personsLayout.Add(self.cboPM, 0, wx.ALL, 5)

        layout.Add(personsLayout, 0, wx.ALL, 5)

        notesLayout = wx.BoxSizer(wx.VERTICAL)
        lblNotes = wx.StaticText(panel, wx.ID_ANY, 'Notes:')
        self.txtNotes = wx.TextCtrl(panel, wx.ID_ANY, uil.displayValue(prj, 'notes'),
                                    style=wx.TE_MULTILINE, size=(500, 200))
        notesLayout.Add(lblNotes, 0, wx.ALL, 5)
        notesLayout.Add(self.txtNotes, 0, wx.ALL, 5)

        layout.Add(notesLayout, 0, wx.ALL, 5)

        return layout

    def getFormData(self):
        self.formData = {
            'name': self.txtName.GetValue(),
            'nickname': self.txtNickname.GetValue(),
            'first_month': ml.uglify(self.txtFirstMonth.GetValue()),
            'last_month': ml.uglify(self.txtLastMonth.GetValue()),
            'PI': self.cboPI.getSelectionId(),
            'PM': self.cboPM.getSelectionId(),
            'notes': self.txtNotes.GetValue()
        }

    def validate(self, prj=None):
        import lib.validator_lib as vl

        prj_id = prj['id'] if prj else 0
        prj_match = vl.ProjectMatch(prj_id, gbl.prjNames)

        errMsg = vl.validatePrjName(self.formData['name'], prj_match)
        if errMsg:
            vl.showErrMsg(self.txtName, errMsg)
            return False

        prj_match = vl.ProjectMatch(prj_id, gbl.prjNicknames)
        errMsg = vl.validatePrjNickname(self.formData['nickname'], prj_match)
        if errMsg:
            vl.showErrMsg(self.txtNickname, errMsg)
            return False

        errMsg = vl.validateTimeframe(
            self.formData['first_month'],
            self.formData['last_month'])
        if errMsg:
            vl.showErrMsg(self.txtFirstMonth, errMsg)
            return False

        if prj and 'asns' in prj  and prj['asns']:
            if self.formData['first_month'] < prj['first_month'] or \
                self.formData['last_month'] > prj['last_month']:
                min, max = ml.getTimeframeEdges(prj['asns'])
                if self.formData['first_month'] < min or self.formData['last_month'] > max:
                    errMsg = 'Assignment(s) out of new timeframe!'
                    vl.showErrMsg(self.txtFirstMonth, errMsg)
                    return False

        return True

    def supplementRec(self):
        if self.ownerRec['PI']:
            self.ownerRec['PiName'] = gbl.empRex[self.ownerRec['PI']]['name']
        if self.ownerRec['PM']:
            self.ownerRec['PmName'] = gbl.empRex[self.ownerRec['PM']]['name']
