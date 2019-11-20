import wx
from utils.strutils import displayValue
import models.globals as gbl
from models.month import Month
import utils.buttons as btn_lib


class PrjFormPanel(wx.Panel):
    def __init__(self, parent, prj=None):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(gbl.COLOR_SCHEME.pnlBg)
        layout = wx.BoxSizer(wx.VERTICAL)

        self.prj = prj

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

        saveBtn = btn_lib.toolbar_button(panel, 'Save Project')
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
        txtName = wx.TextCtrl(panel, wx.ID_ANY,
                              displayValue(self.prj, 'name'), size=(500, -1))
        nameLayout.Add(lblName, 0, wx.ALL, 5)
        nameLayout.Add(txtName, 0, wx.ALL | wx.EXPAND, 5)
        layout.Add(nameLayout, 0, wx.ALL | wx.EXPAND, 5)

        nicknameLayout = wx.BoxSizer(wx.HORIZONTAL)
        lblNickname = wx.StaticText(panel, wx.ID_ANY, 'Nickname: ')
        txtNickname = wx.TextCtrl(panel, wx.ID_ANY,
                                  displayValue(self.prj, 'nickname'), size=(400, -1))
        nicknameLayout.Add(lblNickname, 0, wx.ALL, 5)
        nicknameLayout.Add(txtNickname, 0, wx.ALL, 5)
        layout.Add(nicknameLayout, 0, wx.ALL | wx.EXPAND, 5)

        intervalLayout = wx.BoxSizer(wx.HORIZONTAL)
        lblFirstMonth = wx.StaticText(panel, wx.ID_ANY, 'First Month: ')
        value = Month.prettify(displayValue(self.prj, 'first_month'))
        txtFirstMonth = Month.getMonthCtrl(panel, value)
        intervalLayout.Add(lblFirstMonth, 0, wx.ALL, 5)
        intervalLayout.Add(txtFirstMonth, 0, wx.ALL, 5)

        lblLastMonth = wx.StaticText(panel, wx.ID_ANY, 'Last Month: ')
        value = Month.prettify(displayValue(self.prj, 'last_month'))
        txtLastMonth = Month.getMonthCtrl(panel, value)
        intervalLayout.Add(lblLastMonth, 0, wx.ALL, 5)
        intervalLayout.Add(txtLastMonth, 0, wx.ALL, 5)
        layout.Add(intervalLayout, 0, wx.ALL, 5)

        personsLayout = wx.BoxSizer(wx.HORIZONTAL)
        lblPI = wx.StaticText(panel, wx.ID_ANY, 'PI:')
        pis = [emp['name'] for emp in gbl.empRex if emp['investigator'] == 1]
        cboPI = wx.ComboBox(panel, wx.ID_ANY,
                            choices=pis, value=self.prj['PiName'])
        personsLayout.Add(lblPI, 0, wx.ALL, 5)
        personsLayout.Add(cboPI, 0, wx.ALL, 5)
        lblPM = wx.StaticText(panel, wx.ID_ANY, 'PM:')
        pms = [emp['name'] for emp in gbl.empRex if emp['investigator'] == 0 ]
        cboPM = wx.ComboBox(panel, wx.ID_ANY,
                            choices=pms, value=self.prj['PmName'])
        personsLayout.Add(lblPM, 0, wx.ALL, 5)
        personsLayout.Add(cboPM, 0, wx.ALL, 5)
        layout.Add(personsLayout, 0, wx.ALL, 5)

        notesLayout = wx.BoxSizer(wx.VERTICAL)
        lblNotes = wx.StaticText(panel, wx.ID_ANY, 'Notes:')
        txtNotes = wx.TextCtrl(panel, wx.ID_ANY, displayValue(self.prj, 'notes'),
                               style=wx.TE_MULTILINE, size=(500, 200))
        notesLayout.Add(lblNotes, 0, wx.ALL, 5)
        notesLayout.Add(txtNotes, 0, wx.ALL, 5)
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
        print('save ' + str(self.prj['id']))
        self.Parent.dtlPanel.activateAddBtn()
