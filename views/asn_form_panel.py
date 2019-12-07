import wx
import globals as gbl
import lib.ui_lib as uil


class AsnFormPanel(wx.Panel):
    def __init__(self, parent, ownerId, asn=None):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(gbl.COLOR_SCHEME.pnlBg)
        layout = wx.BoxSizer(wx.VERTICAL)

        self.asn = asn
        self.ownerRec = None
        self.ownerName = None
        self.ownerNameFld = None
        self.assigneeName = None
        self.assigneeNameFld = None

        self.setProps(ownerId)

        self.cboOwner = None
        self.txtFirstMonth = None
        self.txtLastMonth = None
        self.txtEffort = None
        self.txtNotes = None
        self.formData = None

        tbPanel = self.buildToolbarPanel()
        frmPanel = self.buildFormPanel()

        layout.Add(tbPanel, 0, wx.ALL | wx.EXPAND, 5)
        layout.Add(frmPanel, 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(layout)

    def setProps(self, ownerId):
        raise NotImplementedError("Please Implement this method")

    def buildToolbarPanel(self):
        panel = wx.Panel(
            self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize
        )
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.tbBg)
        layout = wx.BoxSizer(wx.HORIZONTAL)

        saveBtn = uil.toolbar_button(panel, 'Save Assignment')
        saveBtn.Bind(wx.EVT_BUTTON, self.onSaveClick)

        cancelBtn = uil.toolbar_button(panel, 'Cancel')
        cancelBtn.Bind(wx.EVT_BUTTON, self.onCancelClick)

        layout.Add(saveBtn, 0, wx.ALL, 5)
        layout.Add(cancelBtn, 0, wx.ALL, 5)

        panel.SetSizer(layout)

        return panel

    def buildFormPanel(self):
        panel = wx.Panel(
            self, wx.ID_ANY, wx.DefaultPosition, size=(-1, 375)
        )
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.frmBg)
        layout = wx.BoxSizer(wx.VERTICAL)

        ownerLayout = wx.BoxSizer(wx.HORIZONTAL)
        value = '%s: %s' % (self.ownerName, self.ownerRec[self.ownerNameFld])
        lbl = wx.StaticText(panel, wx.ID_ANY, value)
        ownerLayout.Add(lbl, 0, wx.ALL | wx.EXPAND, 5)
        layout.Add(ownerLayout, 0, wx.ALL | wx.EXPAND, 5)

        assigneeLayout = wx.BoxSizer(wx.HORIZONTAL)
        value = '%s: ' % (self.assigneeName,)
        if self.asn:
            value += self.asn[self.assigneeNameFld]
        else:
            self.cboOwner = self.getComboBox(panel)
        lbl = wx.StaticText(panel, wx.ID_ANY, value)
        assigneeLayout.Add(lbl, 0, wx.ALL, 5)
        if self.cboOwner:
            assigneeLayout.Add(self.cboOwner, 0, wx.ALL | wx.EXPAND, 5)
        layout.Add(assigneeLayout, 0, wx.ALL | wx.EXPAND, 5)

        intervalLayout = wx.BoxSizer(wx.HORIZONTAL)

        lblFirstMonth = wx.StaticText(panel, wx.ID_ANY, 'First Month: *')
        intervalLayout.Add(lblFirstMonth, 0, wx.ALL, 5)
        value = self.asn['first_month'] if self.asn else ''
        self.txtFirstMonth = uil.getMonthCtrl(panel, value)
        intervalLayout.Add(self.txtFirstMonth, 0, wx.ALL, 5)

        lblLastMonth = wx.StaticText(panel, wx.ID_ANY, 'Last Month: *')
        intervalLayout.Add(lblLastMonth, 0, wx.ALL, 5)
        value = self.asn['last_month'] if self.asn else ''
        self.txtLastMonth = uil.getMonthCtrl(panel, value)
        intervalLayout.Add(self.txtLastMonth, 0, wx.ALL, 5)

        layout.Add(intervalLayout)

        effLayout = wx.BoxSizer(wx.HORIZONTAL)
        lblEffort = wx.StaticText(panel, wx.ID_ANY, '% Effort: *')
        effLayout.Add(lblEffort, 0, wx.ALL, 5)
        value = str(self.asn['effort']) if self.asn else ''
        self.txtEffort = wx.TextCtrl(panel, wx.ID_ANY, value, size=(50, -1))
        effLayout.Add(self.txtEffort, 0, wx.ALL, 5)
        layout.Add(effLayout)

        notesLayout = wx.BoxSizer(wx.VERTICAL)
        lblNotes = wx.StaticText(panel, wx.ID_ANY, 'Notes:')
        notesLayout.Add(lblNotes, 0, wx.ALL, 5)
        value = self.asn['notes'] if self.asn and self.asn['notes'] else ''
        self.txtNotes = wx.TextCtrl(panel, wx.ID_ANY, value,
                                    style=wx.TE_MULTILINE, size=(500, 200))
        notesLayout.Add(self.txtNotes, 0, wx.ALL, 5)
        layout.Add(notesLayout)

        panel.SetSizer(layout)

        return panel

    def getComboBox(self, panel):
        raise NotImplementedError("Please Implement this method")

    def onSaveClick(self, event):
        self.getFormData()

        if self.validate():
            self.processAsn()
        else:
            return

        self.Parent.Close()

    def getFormData(self):
        self.formData['owner'] = self.cboOwner.GetValue()
        self.formData['first_month'] = self.txtFirstMonth.GetValue()
        self.formData['last_month'] = self.txtLastMonth.GetValue()
        self.formData['effort'] = self.txtEffort.GetValue()
        self.formData['notes'] = self.txtNotes.GetValue()

    def validate(self):
        import lib.validator_lib as validators

        if self.cboOwner:
            if not self.formData['owner']:
                errMsg = '%s is required!' % (self.cboOwner.name,)
                validators.showErrMsg(self.cboOwner, errMsg)
                return False

        errMsg = validators.validateTimeframe(
            self.formData['first_month'],
            self.formData['last_month'])
        if errMsg:
            validators.showErrMsg(self.txtFirstMonth, errMsg)
            return False

        errMsg = validators.validateEffort(self.formData['effort'])
        if errMsg:
            validators.showErrMsg(self.txtEffort, errMsg)
            return False

        return True

    def processAsn(self):
        raise NotImplementedError("Please Implement this method")

    def onCancelClick(self, event):
        self.Parent.Close()
