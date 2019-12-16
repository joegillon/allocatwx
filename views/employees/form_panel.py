import wx
from views.form_panel import FormPanel
import lib.ui_lib as uil
import globals as gbl
import dal.emp_dal as emp_dal


class EmpFormPanel(FormPanel):

    def setProps(self):
        self.ownerName = 'Employee'
        self.dal = emp_dal
        self.rex = gbl.empRex

        self.txtName = None
        self.txtGrade = None
        self.txtStep = None
        self.txtFte = None
        self.chkInvestigator = None
        self.txtNotes = None

    def getLayout(self, panel, emp):
        import wx.lib.masked as masked

        layout = wx.BoxSizer(wx.VERTICAL)

        nameLayout = wx.BoxSizer(wx.HORIZONTAL)
        lblName = wx.StaticText(panel, wx.ID_ANY, 'Employee Name: *')
        self.txtName = wx.TextCtrl(panel, wx.ID_ANY,
                                   uil.displayValue(emp, 'name'),
                                   size=(500, -1))
        self.txtName.Bind(wx.EVT_CHAR, self.onNameChar)
        nameLayout.Add(lblName, 0, wx.ALL, 5)
        nameLayout.Add(self.txtName, 0, wx.ALL | wx.EXPAND, 5)
        layout.Add(nameLayout, 0, wx.ALL | wx.EXPAND, 5)

        gsfLayout = wx.BoxSizer(wx.HORIZONTAL)
        lblGrade = wx.StaticText(panel, wx.ID_ANY, 'Grade: ')
        self.txtGrade = masked.TextCtrl(panel, wx.ID_ANY,
                                        mask='##',
                                        size=(50, -1))
        self.txtGrade.SetValue(str(uil.displayValue(emp, 'grade')))
        gsfLayout.Add(lblGrade, 0, wx.ALL, 5)
        gsfLayout.Add(self.txtGrade, 0, wx.ALL, 5)
        layout.Add(gsfLayout, 0, wx.ALL | wx.EXPAND, 5)

        lblStep = wx.StaticText(panel, wx.ID_ANY, 'Step: ')
        self.txtStep = masked.TextCtrl(panel, wx.ID_ANY,
                                        mask='##',
                                        size=(50, -1))
        self.txtStep.SetValue(str(uil.displayValue(emp, 'step')))
        gsfLayout.Add(lblStep, 0, wx.ALL, 5)
        gsfLayout.Add(self.txtStep, 0, wx.ALL, 5)

        lblFte = wx.StaticText(panel, wx.ID_ANY, 'FTE: ')
        self.txtFte = masked.TextCtrl(panel, wx.ID_ANY,
                                        mask='###',
                                        size=(50, -1))
        self.txtFte.SetValue(str(uil.displayValue(emp, 'fte')))
        gsfLayout.Add(lblFte, 0, wx.ALL, 5)
        gsfLayout.Add(self.txtFte, 0, wx.ALL, 5)

        lblInvestigator = wx.StaticText(panel, wx.ID_ANY, 'Investigator:')
        self.chkInvestigator = wx.CheckBox(panel, wx.ID_ANY)
        if emp:
            self.chkInvestigator.SetValue(emp['investigator'])
        gsfLayout.Add(lblInvestigator, 0, wx.ALL, 5)
        gsfLayout.Add(self.chkInvestigator, 0, wx.ALL, 5)
        layout.Add(gsfLayout, 0, wx.ALL, 5)

        notesLayout = wx.BoxSizer(wx.VERTICAL)
        lblNotes = wx.StaticText(panel, wx.ID_ANY, 'Notes:')
        self.txtNotes = wx.TextCtrl(panel, wx.ID_ANY,
                                    uil.displayValue(emp, 'notes'),
                                    style=wx.TE_MULTILINE, size=(500, 200))
        notesLayout.Add(lblNotes, 0, wx.ALL, 5)
        notesLayout.Add(self.txtNotes, 0, wx.ALL, 5)
        layout.Add(notesLayout, 0, wx.ALL, 5)

        return layout

    def onNameChar(self, event):
        import re

        pattern = "[A-Z'\-, ]"
        c = chr(event.KeyCode).upper()
        if c == '\b':
            event.Skip()
            return
        if re.match(pattern, c):
            event.EventObject.AppendText(c)

    def getFormData(self):
        self.formData['name'] = self.txtName.GetValue()
        self.formData['grade'] = self.txtGrade.GetValue().strip()
        self.formData['step'] = self.txtStep.GetValue().strip()
        self.formData['fte'] = self.txtFte.GetValue().strip()
        self.formData['investigator'] = self.chkInvestigator.GetValue()
        self.formData['notes'] = self.txtNotes.GetValue()

    def validate(self, emp=None):
        import lib.validator_lib as vl
        from fuzzywuzzy import process

        emp_id = emp['id'] if emp else 0
        emp_match = vl.EmployeeMatch(emp_id, gbl.empNames)

        errMsg = vl.validateEmpName(self.formData['name'], emp_match)
        if errMsg:
            vl.showErrMsg(self.txtName, errMsg)
            return False

        possible = process.extractOne(self.formData['name'], list(emp_match.names.keys()))
        if possible[1] >= 90:
            possibleEmp = gbl.empRex[emp_match.names[possible[0]]]
            if possibleEmp['id'] != emp_match.id:
                msg = '{0}% match with {1}. Continue?'.format(
                    possible[1],
                    possibleEmp['name']
                )
                dlg = wx.MessageDialog(self, msg,
                                       'Just making sure',
                                       wx.YES_NO | wx.ICON_QUESTION)
                reply = dlg.ShowModal()
                if reply != wx.ID_YES:
                    self.txtName.SetFocus()
                    return

        errMsg = vl.validateGrade(self.formData['grade'])
        if errMsg:
            vl.showErrMsg(self.txtGrade, errMsg)
            return False

        errMsg = vl.validateStep(self.formData['step'])
        if errMsg:
            vl.showErrMsg(self.txtStep, errMsg)
            return False

        errMsg = vl.validateFte(self.formData['fte'])
        if errMsg:
            vl.showErrMsg(self.txtFte, errMsg)
            return False

        errMsg = vl.validateInvestigator(
            self.formData['investigator'], self.formData['grade']
        )
        if errMsg:
            vl.showErrMsg(self.chkInvestigator, errMsg)
            return False

        return True

    def supplementRec(self):
        pass
