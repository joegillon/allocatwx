import wx

import globals as gbl
import lib.ui_lib as uil
from dal.dao import Dao
import dal.emp_dal as emp_dal


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
        self.formData = None

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

        dropBtn = uil.toolbar_button(panel, 'Drop Employee')
        dropBtn.Bind(wx.EVT_BUTTON, self.onDropClick)

        saveBtn = uil.toolbar_button(panel, 'Save Employee')
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
        lblName = wx.StaticText(panel, wx.ID_ANY, 'Employee Name: *')
        self.txtName = wx.TextCtrl(panel, wx.ID_ANY,
                                   uil.displayValue(self.emp, 'name'),
                                   size=(500, -1))
        nameLayout.Add(lblName, 0, wx.ALL, 5)
        nameLayout.Add(self.txtName, 0, wx.ALL | wx.EXPAND, 5)
        layout.Add(nameLayout, 0, wx.ALL | wx.EXPAND, 5)

        gsfLayout = wx.BoxSizer(wx.HORIZONTAL)
        lblGrade = wx.StaticText(panel, wx.ID_ANY, 'Grade: ')
        self.txtGrade = wx.TextCtrl(panel, wx.ID_ANY,
                                    str(uil.displayValue(self.emp, 'grade')),
                                    size=(50, -1))
        gsfLayout.Add(lblGrade, 0, wx.ALL, 5)
        gsfLayout.Add(self.txtGrade, 0, wx.ALL, 5)
        layout.Add(gsfLayout, 0, wx.ALL | wx.EXPAND, 5)

        lblStep = wx.StaticText(panel, wx.ID_ANY, 'Step: ')
        self.txtStep = wx.TextCtrl(panel, wx.ID_ANY,
                                   str(uil.displayValue(self.emp, 'step')), size=(50, -1))
        gsfLayout.Add(lblStep, 0, wx.ALL, 5)
        gsfLayout.Add(self.txtStep, 0, wx.ALL, 5)

        lblFte = wx.StaticText(panel, wx.ID_ANY, 'FTE: ')
        self.txtFte = wx.TextCtrl(panel, wx.ID_ANY,
                                  str(uil.displayValue(self.emp, 'fte')), size=(50, -1))
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
                                    uil.displayValue(self.emp, 'notes'),
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
            result = emp_dal.delete(Dao(), [self.emp['id']])
            print(result)

    def onSaveClick(self, event):
        self.getFormData()

        if self.validate():
            if self.emp is None:
                result = emp_dal.add(Dao(), self.formData)
                print(result)
            else:
                result = emp_dal.update(Dao(), self.emp['id'], self.formData)
                print(result)
            self.Parent.dtlPanel.activateAddBtn()
            self.Parent.Close()

    def getFormData(self):
        self.formData['name'] = self.txtName.GetValue()
        self.formData['grade'] = self.txtGrade.GetValue()
        self.formData['step'] = self.txtStep.GetValue()
        self.formData['fte'] = self.txtFte.GetValue()
        self.formData['investigator'] = self.chkInvestigator.GetValue()
        self.formData['notes'] = self.txtNotes.GetValue()

    def validate(self):
        import lib.validator_lib as validators
        from models.employee import EmployeeMatch

        emp_id = self.emp['id'] if self.emp else 0
        emp_match = EmployeeMatch(emp_id, gbl.empNames)
        errMsg = validators.validateEmpName(self.formData['name'], emp_match)
        if errMsg == '':
            validators.showErrMsg(self.txtName, errMsg)
            return False

        errMsg = validators.validateGrade(self.formData['grade'])
        if errMsg:
            validators.showErrMsg(self.txtGrade, errMsg)
            return False

        errMsg = validators.validateStep(self.formData['step'])
        if errMsg:
            validators.showErrMsg(self.txtStep, errMsg)
            return False

        errMsg = validators.validateFte(self.formData['fte'])
        if errMsg:
            validators.showErrMsg(self.txtFte, errMsg)
            return False
