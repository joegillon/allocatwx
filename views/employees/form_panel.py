import wx
from utils.strutils import displayValue
import models.globals as gbl
import utils.buttons as btn_lib


class EmpFormPanel(wx.Panel):
    def __init__(self, parent, empId):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(gbl.COLOR_SCHEME.pnlBg)
        layout = wx.BoxSizer(wx.VERTICAL)

        self.emp = gbl.empRex[empId] if empId else None
        self.txtName = None
        self.txtGrade = None
        self.txtStep = None
        self.txtFte = None
        self.chkInvestigator = None
        self.txtNotes = None

        tbPanel = self.buildToolbarPanel()
        frmPanel = self.buildFormPanel()

        layout.Add(tbPanel, 0, wx.ALL | wx.EXPAND, 5)
        layout.Add(frmPanel, 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(layout)

        self.txtName.SetFocus()

    def buildToolbarPanel(self):
        panel = wx.Panel(
            self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize
        )
        panel.SetBackgroundColour(wx.Colour(gbl.COLOR_SCHEME.tbBg))
        layout = wx.BoxSizer(wx.HORIZONTAL)

        dropBtn = btn_lib.toolbar_button(panel, 'Drop Employee')
        dropBtn.Bind(wx.EVT_BUTTON, self.onDropClick)

        saveBtn = btn_lib.toolbar_button(panel, 'Save Employee')
        saveBtn.Bind(wx.EVT_BUTTON, self.onSaveClick)

        layout.Add(dropBtn, 0, wx.ALL, 5)
        layout.Add(saveBtn, 0, wx.ALL, 5)

        panel.SetSizer(layout)

        return panel

    def buildFormPanel(self):
        panel = wx.Panel(
            self, wx.ID_ANY, wx.DefaultPosition, size=(-1, 375)
        )
        panel.SetBackgroundColour(wx.Colour(gbl.COLOR_SCHEME.frmBg))
        panel.SetForegroundColour('black')
        layout = wx.BoxSizer(wx.VERTICAL)

        nameLayout = wx.BoxSizer(wx.HORIZONTAL)
        lblName = wx.StaticText(panel, wx.ID_ANY, 'Employee Name: ')
        self.txtName = wx.TextCtrl(panel, wx.ID_ANY,
                                   displayValue(self.emp, 'name'),
                                   size=(500, -1))
        nameLayout.Add(lblName, 0, wx.ALL, 5)
        nameLayout.Add(self.txtName, 0, wx.ALL | wx.EXPAND, 5)
        layout.Add(nameLayout, 0, wx.ALL | wx.EXPAND, 5)

        gsfLayout = wx.BoxSizer(wx.HORIZONTAL)
        lblGrade = wx.StaticText(panel, wx.ID_ANY, 'Grade: ')
        self.txtGrade = wx.TextCtrl(panel, wx.ID_ANY,
                               str(displayValue(self.emp, 'grade')),
                               size=(50, -1))
        gsfLayout.Add(lblGrade, 0, wx.ALL, 5)
        gsfLayout.Add(self.txtGrade, 0, wx.ALL, 5)
        layout.Add(gsfLayout, 0, wx.ALL | wx.EXPAND, 5)

        lblStep = wx.StaticText(panel, wx.ID_ANY, 'Step: ')
        self.txtStep = wx.TextCtrl(panel, wx.ID_ANY,
                              str(displayValue(self.emp, 'step')), size=(50, -1))
        gsfLayout.Add(lblStep, 0, wx.ALL, 5)
        gsfLayout.Add(self.txtStep, 0, wx.ALL, 5)

        lblFte = wx.StaticText(panel, wx.ID_ANY, 'FTE: ')
        self.txtFte = wx.TextCtrl(panel, wx.ID_ANY,
                             str(displayValue(self.emp, 'fte')), size=(50, -1))
        gsfLayout.Add(lblFte, 0, wx.ALL, 5)
        gsfLayout.Add(self.txtFte, 0, wx.ALL, 5)

        lblInvestigator = wx.StaticText(panel, wx.ID_ANY, 'Investigator:')
        self.chkInvestigator = wx.CheckBox(panel, wx.ID_ANY)
        gsfLayout.Add(lblInvestigator, 0, wx.ALL, 5)
        gsfLayout.Add(self.chkInvestigator, 0, wx.ALL, 5)
        layout.Add(gsfLayout, 0, wx.ALL, 5)

        notesLayout = wx.BoxSizer(wx.VERTICAL)
        lblNotes = wx.StaticText(panel, wx.ID_ANY, 'Notes:')
        self.txtNotes = wx.TextCtrl(panel, wx.ID_ANY,
                               displayValue(self.emp, 'notes'),
                               style=wx.TE_MULTILINE, size=(500, 200))
        notesLayout.Add(lblNotes, 0, wx.ALL, 5)
        notesLayout.Add(self.txtNotes, 0, wx.ALL, 5)
        layout.Add(notesLayout, 0, wx.ALL, 5)

        panel.SetSizer(layout)

        return panel

    def onDropClick(self, event):
        dlg = wx.MessageDialog(self, 'Drop employee?', 'Just making sure',
                               wx.YES_NO | wx.ICON_QUESTION)
        reply = dlg.ShowModal()
        if reply == wx.ID_YES:
            print('drop ' + str(self.emp['id']))

    def onSaveClick(self, event):
        if self.validate():
            self.Parent.dtlPanel.activateAddBtn()
            self.Parent.Close()

    def validate(self):
        import models.validators as validators

        value = self.txtName.GetValue().upper()
        errMsg = validators.validateEmpName(value, gbl.empRex)
        if errMsg == '':
            validators.showErrMsg(self.txtName, errMsg)
            return False

        value = self.txtGrade.GetValue()
        errMsg = validators.validateGrade(value)
        if errMsg:
            validators.showErrMsg(self.txtGrade, errMsg)
            return False

        value = self.txtStep.GetValue()
        errMsg = validators.validateStep(value)
        if errMsg:
            validators.showErrMsg(self.txtStep, errMsg)
            return False

        value = self.txtFte.GetValue()
        errMsg = validators.validateFte(value)
        if errMsg:
            validators.showErrMsg(self.txtFte, errMsg)
            return False
