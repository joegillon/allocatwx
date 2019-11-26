import wx
import models.globals as gbl
from models.month import Month
from utils.strutils import displayValue
import utils.buttons as btn_lib


class EmpAsnFormPanel(wx.Panel):
    def __init__(self, parent, empId, asn=None):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(gbl.COLOR_SCHEME.pnlBg)
        layout = wx.BoxSizer(wx.VERTICAL)

        self.emp = gbl.empRex[empId] if empId else None
        self.asn = asn
        self.cboPrj = None
        self.txtFirstMonth = None
        self.txtLastMonth = None
        self.txtEffort = None
        self.txtNotes = None

        tbPanel = self.buildToolbarPanel()
        frmPanel = self.buildFormPanel(empId)

        layout.Add(tbPanel, 0, wx.ALL | wx.EXPAND, 5)
        layout.Add(frmPanel, 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(layout)

    def buildToolbarPanel(self):
        panel = wx.Panel(
            self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize
        )
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.tbBg)
        layout = wx.BoxSizer(wx.HORIZONTAL)

        saveBtn = btn_lib.toolbar_button(panel, 'Save Assignment')
        saveBtn.Bind(wx.EVT_BUTTON, self.onSaveClick)

        cancelBtn = btn_lib.toolbar_button(panel, 'Cancel')
        cancelBtn.Bind(wx.EVT_BUTTON, self.onCancelClick)

        layout.Add(saveBtn, 0, wx.ALL, 5)
        layout.Add(cancelBtn, 0, wx.ALL, 5)

        panel.SetSizer(layout)

        return panel

    def buildFormPanel(self, empName):
        panel = wx.Panel(
            self, wx.ID_ANY, wx.DefaultPosition, size=(-1, 375)
        )
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.frmBg)
        layout = wx.BoxSizer(wx.VERTICAL)

        empLayout = wx.BoxSizer(wx.HORIZONTAL)
        lblPrj = wx.StaticText(panel, wx.ID_ANY, 'Employee: ' + self.emp['name'])
        empLayout.Add(lblPrj, 0, wx.ALL | wx.EXPAND, 5)
        layout.Add(empLayout)

        prjLayout = wx.BoxSizer(wx.HORIZONTAL)
        value = 'Project: %s' % displayValue(self.asn, 'project')
        lblPrj = wx.StaticText(panel, wx.ID_ANY, value)
        prjLayout.Add(lblPrj, 0, wx.ALL, 5)
        if not self.asn:
            names = [rec['nickname'] for rec in gbl.prjRex.values()]
            self.cboPrj = wx.ComboBox(panel, wx.ID_ANY,
                                      pos=wx.DefaultPosition,
                                      size=wx.DefaultSize,
                                      style=wx.CB_READONLY,
                                      choices=names
                                      )
            prjLayout.Add(self.cboPrj, 0, wx.ALL | wx.EXPAND, 5)
        layout.Add(prjLayout)

        intervalLayout = wx.BoxSizer(wx.HORIZONTAL)

        lblFirstMonth = wx.StaticText(panel, wx.ID_ANY, 'First Month: ')
        intervalLayout.Add(lblFirstMonth, 0, wx.ALL, 5)
        value = self.asn['first_month'] if self.asn else ''
        self.txtFirstMonth = Month.getMonthCtrl(panel, value)
        intervalLayout.Add(self.txtFirstMonth, 0, wx.ALL, 5)

        lblLastMonth = wx.StaticText(panel, wx.ID_ANY, 'Last Month: ')
        intervalLayout.Add(lblLastMonth, 0, wx.ALL, 5)
        value = self.asn['last_month'] if self.asn else ''
        self.txtLastMonth = Month.getMonthCtrl(panel, value)
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
        if self.validate():
            print('save ' + str(self.asn['id']))
        else:
            return
        self.Parent.Close()

    def validate(self):
        import models.validators as validators

        if self.cboPrj:
            value = self.cboPrj.GetValue()
            errMsg = validators.validatePrjNickname(value)
            if errMsg:
                validators.showErrMsg(self.cboPrj, errMsg)
                return False

        first_month = self.txtFirstMonth.GetValue()
        last_month = self.txtLastMonth.GetValue()
        errMsg = validators.validateTimeframe(first_month, last_month)
        if errMsg:
            validators.showErrMsg(self.txtFirstMonth, errMsg)
            return False

        value = self.txtEffort.GetValue()
        errMsg = validators.validateEffort(value)
        if errMsg:
            validators.showErrMsg(self.txtEffort, errMsg)
            return False

        return True

    def onCancelClick(self, event):
        self.Parent.Close()
