import wx
from views.form_panel import FormPanel
import lib.ui_lib as uil
import globals as gbl
import dal.emp_dal as emp_dal


class EmpFormPanel(FormPanel):

    def setProps(self):
        self.ownerName = 'Employee'
        self.dal = emp_dal

        self.txtName = None
        self.txtGrade = None
        self.txtStep = None
        self.txtFte = None
        self.chkInvestigator = None
        self.txtNotes = None

    def getLayout(self, panel, emp):
        layout = wx.BoxSizer(wx.VERTICAL)

        nameLayout = wx.BoxSizer(wx.HORIZONTAL)
        lblName = wx.StaticText(panel, wx.ID_ANY, 'Employee Name: *')
        self.txtName = wx.TextCtrl(panel, wx.ID_ANY,
                                   uil.displayValue(emp, 'name'),
                                   size=(500, -1))
        nameLayout.Add(lblName, 0, wx.ALL, 5)
        nameLayout.Add(self.txtName, 0, wx.ALL | wx.EXPAND, 5)
        layout.Add(nameLayout, 0, wx.ALL | wx.EXPAND, 5)

        gsfLayout = wx.BoxSizer(wx.HORIZONTAL)
        lblGrade = wx.StaticText(panel, wx.ID_ANY, 'Grade: ')
        self.txtGrade = wx.TextCtrl(panel, wx.ID_ANY,
                                    str(uil.displayValue(emp, 'grade')),
                                    size=(50, -1))
        gsfLayout.Add(lblGrade, 0, wx.ALL, 5)
        gsfLayout.Add(self.txtGrade, 0, wx.ALL, 5)
        layout.Add(gsfLayout, 0, wx.ALL | wx.EXPAND, 5)

        lblStep = wx.StaticText(panel, wx.ID_ANY, 'Step: ')
        self.txtStep = wx.TextCtrl(panel, wx.ID_ANY,
                                   str(uil.displayValue(emp, 'step')), size=(50, -1))
        gsfLayout.Add(lblStep, 0, wx.ALL, 5)
        gsfLayout.Add(self.txtStep, 0, wx.ALL, 5)

        lblFte = wx.StaticText(panel, wx.ID_ANY, 'FTE: ')
        self.txtFte = wx.TextCtrl(panel, wx.ID_ANY,
                                  str(uil.displayValue(emp, 'fte')), size=(50, -1))
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
                                    uil.displayValue(emp, 'notes'),
                                    style=wx.TE_MULTILINE, size=(500, 200))
        notesLayout.Add(lblNotes, 0, wx.ALL, 5)
        notesLayout.Add(self.txtNotes, 0, wx.ALL, 5)
        layout.Add(notesLayout, 0, wx.ALL, 5)

        return layout

    def getFormData(self):
        self.formData['name'] = self.txtName.GetValue()
        self.formData['grade'] = self.txtGrade.GetValue()
        self.formData['step'] = self.txtStep.GetValue()
        self.formData['fte'] = self.txtFte.GetValue()
        self.formData['investigator'] = self.chkInvestigator.GetValue()
        self.formData['notes'] = self.txtNotes.GetValue()

    def validate(self, emp=None):
        import lib.validator_lib as vl

        emp_id = emp['id'] if emp else 0
        emp_match = vl.EmployeeMatch(emp_id, gbl.empNames)

        errMsg = vl.validateEmpName(self.formData['name'], emp_match)
        if errMsg == '':
            vl.showErrMsg(self.txtName, errMsg)
            return False

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
