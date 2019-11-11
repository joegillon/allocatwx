import wx
import models.globals as gbl


class PrjAsnFormPanel(wx.Panel):
    def __init__(self, parent, prjName, asn=None):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(wx.Colour(116, 65, 43))
        layout = wx.BoxSizer(wx.VERTICAL)

        self.asn = asn
        self.cboEmp = None
        self.txtFirstMonth = None
        self.txtLastMonth = None
        self.txtEffort = None
        self.txtNotes = None

        tbPanel = self.buildToolbarPanel()
        frmPanel = self.buildFormPanel(prjName)

        layout.Add(tbPanel, 0, wx.ALL | wx.EXPAND, 5)
        layout.Add(frmPanel, 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(layout)

    def buildToolbarPanel(self):
        panel = wx.Panel(
            self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize
        )
        panel.SetBackgroundColour(wx.Colour(190, 130, 96))
        layout = wx.BoxSizer(wx.HORIZONTAL)

        saveBtn = wx.Button(panel, wx.ID_ANY, label='Save Assignment')
        saveBtn.Bind(wx.EVT_BUTTON, self.onSaveClick)

        cancelBtn = wx.Button(panel, wx.ID_ANY, label='Cancel')
        cancelBtn.Bind(wx.EVT_BUTTON, self.onCancelClick)

        layout.Add(saveBtn, 0, wx.ALL, 5)
        layout.Add(cancelBtn, 0, wx.ALL, 5)

        panel.SetSizer(layout)

        return panel

    def buildFormPanel(self, prjName):
        panel = wx.Panel(
            self, wx.ID_ANY, wx.DefaultPosition, size=(-1, 375)
        )
        panel.SetBackgroundColour(wx.Colour(215, 176, 149))
        layout = wx.BoxSizer(wx.VERTICAL)

        prjLayout = wx.BoxSizer(wx.HORIZONTAL)
        lblPrj = wx.StaticText(panel, wx.ID_ANY, 'Project: ' + prjName)
        prjLayout.Add(lblPrj, 0, wx.ALL | wx.EXPAND, 5)
        layout.Add(prjLayout)

        empLayout = wx.BoxSizer(wx.HORIZONTAL)
        value = 'Employee: ' + (self.asn['employee'] if self.asn else '')
        lblEmp = wx.StaticText(panel, wx.ID_ANY, value)
        empLayout.Add(lblEmp, 0, wx.ALL, 5)
        if not self.asn:
            names = [rec['name'] for rec in gbl.empRex]
            self.cboEmp = wx.ComboBox(panel, wx.ID_ANY,
                                      pos=wx.DefaultPosition,
                                      size=wx.DefaultSize,
                                      style=wx.CB_READONLY,
                                      choices=names
                                      )
            empLayout.Add(self.cboEmp, 0, wx.ALL | wx.EXPAND, 5)
        layout.Add(empLayout)

        intervalLayout = wx.BoxSizer(wx.HORIZONTAL)

        lblFirstMonth = wx.StaticText(panel, wx.ID_ANY, 'First Month: ')
        intervalLayout.Add(lblFirstMonth, 0, wx.ALL, 5)
        value = self.asn['first_month'] if self.asn else ''
        self.txtFirstMonth = wx.TextCtrl(panel, wx.ID_ANY, value, size=(50, -1))
        intervalLayout.Add(self.txtFirstMonth, 0, wx.ALL, 5)

        lblLastMonth = wx.StaticText(panel, wx.ID_ANY, 'Last Month: ')
        intervalLayout.Add(lblLastMonth, 0, wx.ALL, 5)
        value = self.asn['last_month'] if self.asn else ''
        self.txtLastMonth = wx.TextCtrl(panel, wx.ID_ANY, value, size=(50, -1))
        intervalLayout.Add(self.txtLastMonth, 0, wx.ALL, 5)

        layout.Add(intervalLayout)

        effLayout = wx.BoxSizer(wx.HORIZONTAL)
        lblEffort = wx.StaticText(panel, wx.ID_ANY, '% Effort: ')
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

    def onSaveClick(self, event):
        if self.asn:
            print('save ' + str(self.asn['id']))
        self.Parent.Close()

    def onCancelClick(self, event):
        self.Parent.Close()
