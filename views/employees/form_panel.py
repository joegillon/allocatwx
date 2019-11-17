import wx
from utils.strutils import monthPrettify, displayValue
import models.globals as gbl
import utils.buttons as btn_lib


class EmpFormPanel(wx.Panel):
    def __init__(self, parent, emp=None):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(gbl.COLOR_SCHEME.pnlBg)
        layout = wx.BoxSizer(wx.VERTICAL)

        self.emp = emp

        tbPanel = self.buildToolbarPanel()
        frmPanel = self.buildFormPanel()

        layout.Add(tbPanel, 0, wx.ALL | wx.EXPAND, 5)
        layout.Add(frmPanel, 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(layout)

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
        txtName = wx.TextCtrl(panel, wx.ID_ANY,
                              displayValue(self.emp, 'name'), size=(500, -1))
        nameLayout.Add(lblName, 0, wx.ALL, 5)
        nameLayout.Add(txtName, 0, wx.ALL | wx.EXPAND, 5)
        layout.Add(nameLayout, 0, wx.ALL | wx.EXPAND, 5)

        gsfLayout = wx.BoxSizer(wx.HORIZONTAL)
        lblGrade = wx.StaticText(panel, wx.ID_ANY, 'Grade: ')
        txtGrade = wx.TextCtrl(panel, wx.ID_ANY,
                               str(displayValue(self.emp, 'grade')), size=(50, -1))
        gsfLayout.Add(lblGrade, 0, wx.ALL, 5)
        gsfLayout.Add(txtGrade, 0, wx.ALL, 5)
        layout.Add(gsfLayout, 0, wx.ALL | wx.EXPAND, 5)

        lblStep = wx.StaticText(panel, wx.ID_ANY, 'Step: ')
        txtStep = wx.TextCtrl(panel, wx.ID_ANY,
                              str(displayValue(self.emp, 'step')), size=(50, -1))
        gsfLayout.Add(lblStep, 0, wx.ALL, 5)
        gsfLayout.Add(txtStep, 0, wx.ALL, 5)

        lblFte = wx.StaticText(panel, wx.ID_ANY, 'FTE: ')
        txtFte = wx.TextCtrl(panel, wx.ID_ANY,
                             str(displayValue(self.emp, 'fte')), size=(50, -1))
        gsfLayout.Add(lblFte, 0, wx.ALL, 5)
        gsfLayout.Add(txtFte, 0, wx.ALL, 5)
        layout.Add(gsfLayout, 0, wx.ALL, 5)

        notesLayout = wx.BoxSizer(wx.VERTICAL)
        lblNotes = wx.StaticText(panel, wx.ID_ANY, 'Notes:')
        txtNotes = wx.TextCtrl(panel, wx.ID_ANY,
                               displayValue(self.emp, 'notes'),
                               style=wx.TE_MULTILINE, size=(500, 200))
        notesLayout.Add(lblNotes, 0, wx.ALL, 5)
        notesLayout.Add(txtNotes, 0, wx.ALL, 5)
        layout.Add(notesLayout, 0, wx.ALL, 5)

        panel.SetSizer(layout)

        return panel

    def onDropClick(self, event):
        dlg = wx.MessageDialog(self, 'Drop employee?', 'Just making sure',
                               wx.YES_NO | wx.ICON_QUESTION)
        reply = dlg.ShowModal()
        if reply == wx.ID_YES:
            print('drop ' + str(self.prj['id']))

    def onSaveClick(self, event):
        print('save ' + str(self.emp['id']))
        self.Parent.dtlPanel.activateAddBtn()
