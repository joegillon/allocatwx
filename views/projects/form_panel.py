import wx
from utils.strutils import displayValue
import models.globals as gbl
from models.month import Month
import utils.buttons as btn_lib


class PrjFormPanel(wx.Panel):
    def __init__(self, parent, prjId):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(gbl.COLOR_SCHEME.pnlBg)
        layout = wx.BoxSizer(wx.VERTICAL)

        self.prj = gbl.prjRex[prjId] if prjId else None
        self.txtName = None
        self.txtNickname = None
        self.txtFirstMonth = None
        self.txtLastMonth = None
        self.cboPI = None
        self.cboPM = None
        self.txtNotes = None

        tbPanel = self.buildToolbarPanel()
        frmPanel = self.buildFormPanel()

        layout.Add(tbPanel, 0, wx.ALL | wx.EXPAND, 5)
        layout.Add(frmPanel, 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(layout)

    def buildToolbarPanel(self):
        panel = wx.Panel(
            self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize
        )
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.tbBg)
        layout = wx.BoxSizer(wx.HORIZONTAL)

        dropBtn = btn_lib.toolbar_button(panel, 'Drop Project')
        dropBtn.Bind(wx.EVT_BUTTON, self.onDropClick)

        saveBtn = btn_lib.toolbar_button(panel,  'Save Project', ok=True)
        saveBtn.Bind(wx.EVT_BUTTON, self.onSaveClick)

        layout.Add(dropBtn, 0, wx.ALL, 5)
        layout.Add(saveBtn, 0, wx.ALL, 5)

        panel.SetSizer(layout)

        return panel

    def buildFormPanel(self):
        panel = wx.Panel(
            self, wx.ID_ANY, wx.DefaultPosition, size=(-1, 375)
        )
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.frmBg)
        panel.SetForegroundColour('black')
        layout = wx.BoxSizer(wx.VERTICAL)

        nameLayout = wx.BoxSizer(wx.HORIZONTAL)
        lblName = wx.StaticText(panel, wx.ID_ANY, 'Project Name: ')
        self.txtName = wx.TextCtrl(panel, wx.ID_ANY,
                              displayValue(self.prj, 'name'),
                              size=(500, -1))
        nameLayout.Add(lblName, 0, wx.ALL, 5)
        nameLayout.Add(self.txtName, 0, wx.ALL | wx.EXPAND, 5)
        layout.Add(nameLayout, 0, wx.ALL | wx.EXPAND, 5)

        nicknameLayout = wx.BoxSizer(wx.HORIZONTAL)
        lblNickname = wx.StaticText(panel, wx.ID_ANY, 'Nickname: ')
        self.txtNickname = wx.TextCtrl(panel, wx.ID_ANY,
                                  displayValue(self.prj, 'nickname'), size=(400, -1))
        nicknameLayout.Add(lblNickname, 0, wx.ALL, 5)
        nicknameLayout.Add(self.txtNickname, 0, wx.ALL, 5)
        layout.Add(nicknameLayout, 0, wx.ALL | wx.EXPAND, 5)

        intervalLayout = wx.BoxSizer(wx.HORIZONTAL)
        lblFirstMonth = wx.StaticText(panel, wx.ID_ANY, 'First Month: ')
        value = Month.prettify(displayValue(self.prj, 'first_month'))
        self.txtFirstMonth = Month.getMonthCtrl(panel, value)
        intervalLayout.Add(lblFirstMonth, 0, wx.ALL, 5)
        intervalLayout.Add(self.txtFirstMonth, 0, wx.ALL, 5)

        lblLastMonth = wx.StaticText(panel, wx.ID_ANY, 'Last Month: ')
        value = Month.prettify(displayValue(self.prj, 'last_month'))
        self.txtLastMonth = Month.getMonthCtrl(panel, value)
        intervalLayout.Add(lblLastMonth, 0, wx.ALL, 5)
        intervalLayout.Add(self.txtLastMonth, 0, wx.ALL, 5)
        layout.Add(intervalLayout, 0, wx.ALL, 5)

        personsLayout = wx.BoxSizer(wx.HORIZONTAL)
        lblPI = wx.StaticText(panel, wx.ID_ANY, 'PI:')
        pis = [emp['name'] for emp in gbl.empRex.values() if emp['investigator'] == 1]
        self.cboPI = wx.ComboBox(panel, wx.ID_ANY,
                            style=wx.CB_READONLY,
                            choices=pis,
                            value=self.prj['PiName'] if self.prj else '')
        personsLayout.Add(lblPI, 0, wx.ALL, 5)
        personsLayout.Add(self.cboPI, 0, wx.ALL, 5)
        lblPM = wx.StaticText(panel, wx.ID_ANY, 'PM:')
        pms = [emp['name'] for emp in gbl.empRex.values() if emp['investigator'] == 0 ]
        self.cboPM = wx.ComboBox(panel, wx.ID_ANY,
                            style=wx.CB_READONLY,
                            choices=pms,
                            value=self.prj['PmName'] if self.prj else '' )
        personsLayout.Add(lblPM, 0, wx.ALL, 5)
        personsLayout.Add(self.cboPM, 0, wx.ALL, 5)
        layout.Add(personsLayout, 0, wx.ALL, 5)

        notesLayout = wx.BoxSizer(wx.VERTICAL)
        lblNotes = wx.StaticText(panel, wx.ID_ANY, 'Notes:')
        self.txtNotes = wx.TextCtrl(panel, wx.ID_ANY, displayValue(self.prj, 'notes'),
                               style=wx.TE_MULTILINE, size=(500, 200))
        notesLayout.Add(lblNotes, 0, wx.ALL, 5)
        notesLayout.Add(self.txtNotes, 0, wx.ALL, 5)
        layout.Add(notesLayout, 0, wx.ALL, 5)

        panel.SetSizer(layout)

        return panel

    def onDropClick(self, event):
        dlg = wx.MessageDialog(self, 'Drop project?', 'Just making sure',
                               wx.YES_NO | wx.ICON_QUESTION)
        reply = dlg.ShowModal()
        if reply == wx.ID_YES:
            print('drop ' + str(self.prj['id']))

    def onSaveClick(self, event):
        if self.validate():
            self.Parent.dtlPanel.activateAddBtn()
            self.Parent.EndModal(wx.ID_OK)

    def validate(self):
        import re

        value = self.txtName.GetValue()
        if value == '':
            self.txtName.SetFocus()
            wx.MessageBox('Project Name required!', 'Error!',
                          wx.ICON_EXCLAMATION | wx.OK)
            return False

        if value in gbl.prjNames:
            self.txtName.SetFocus()
            wx.MessageBox('Project Name taken!', 'Error!',
                          wx.ICON_EXCLAMATION | wx.OK)
            return False

        value = self.txtNickname.GetValue()
        if value == '':
            self.txtNickname.SetFocus()
            wx.MessageBox('Project Nickname required!', 'Error!',
                      wx.ICON_EXCLAMATION | wx.OK)
            return False

        if value.upper() in gbl.prjNicknames:
            self.txtNickname.SetFocus()
            wx.MessageBox('Project Nickname taken!', 'Error!',
                          wx.ICON_EXCLAMATION | wx.OK)
            return False

        first_month = self.txtFirstMonth.GetValue()
        if not re.match(gbl.MONTH_PATTERN, first_month):
            self.txtFirstMonth.SetFocus()
            wx.MessageBox('First Month invalid!', 'Error!',
                          wx.ICON_EXCLAMATION | wx.OK)
            return False

        last_month = self.txtLastMonth.GetValue()
        if not re.match(gbl.MONTH_PATTERN, last_month):
            self.txtLastMonth.SetFocus()
            wx.MessageBox('Last Month invalid!', 'Error!',
                          wx.ICON_EXCLAMATION | wx.OK)
            return False

        if not Month.isValidSpan(first_month, last_month):
            self.txtFirstMonth.SetFocus()
            wx.MessageBox('First Month must precede Last Month!', 'Error!',
                          wx.ICON_EXCLAMATION | wx.OK)
            return False

        return True