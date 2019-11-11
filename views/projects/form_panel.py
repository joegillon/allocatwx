import wx
from utils.strutils import monthPrettify


class PrjFormPanel(wx.Panel):
    def __init__(self, parent, prj=None):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(wx.Colour(116, 65, 43))
        layout = wx.BoxSizer(wx.VERTICAL)

        self.prj = prj

        tbPanel = self.buildToolbarPanel()
        frmPanel = self.buildFormPanel(prj)

        layout.Add(tbPanel, 0, wx.ALL | wx.EXPAND, 5)
        layout.Add(frmPanel, 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(layout)

    def buildToolbarPanel(self):
        panel = wx.Panel(
            self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize
        )
        panel.SetBackgroundColour(wx.Colour(190, 130, 96))
        layout = wx.BoxSizer(wx.HORIZONTAL)

        dropBtn = wx.Button(panel, wx.ID_ANY, label='Drop Project')
        dropBtn.Bind(wx.EVT_BUTTON, self.onDropClick)

        saveBtn = wx.Button(panel, wx.ID_ANY, label='Save Project')
        saveBtn.Bind(wx.EVT_BUTTON, self.onSaveClick)

        layout.Add(dropBtn, 0, wx.ALL, 5)
        layout.Add(saveBtn, 0, wx.ALL, 5)

        panel.SetSizer(layout)

        return panel

    def buildFormPanel(self, prj):
        panel = wx.Panel(
            self, wx.ID_ANY, wx.DefaultPosition, size=(-1, 375)
        )
        panel.SetBackgroundColour(wx.Colour(215, 176, 149))
        panel.SetForegroundColour('black')
        layout = wx.BoxSizer(wx.VERTICAL)

        nameLayout = wx.BoxSizer(wx.HORIZONTAL)
        lblName = wx.StaticText(panel, wx.ID_ANY, 'Project Name: ')
        value = prj['name'] if prj else ''
        txtName = wx.TextCtrl(panel, wx.ID_ANY, value, size=(500, -1))
        nameLayout.Add(lblName, 0, wx.ALL, 5)
        nameLayout.Add(txtName, 0, wx.ALL | wx.EXPAND, 5)
        layout.Add(nameLayout, 0, wx.ALL | wx.EXPAND, 5)

        nicknameLayout = wx.BoxSizer(wx.HORIZONTAL)
        lblNickname = wx.StaticText(panel, wx.ID_ANY, 'Nickname: ')
        value = prj['nickname'] if prj else ''
        txtNickname = wx.TextCtrl(panel, wx.ID_ANY, value, size=(400, -1))
        nicknameLayout.Add(lblNickname, 0, wx.ALL, 5)
        nicknameLayout.Add(txtNickname, 0, wx.ALL, 5)
        layout.Add(nicknameLayout, 0, wx.ALL | wx.EXPAND, 5)

        intervalLayout = wx.BoxSizer(wx.HORIZONTAL)
        lblFirstMonth = wx.StaticText(panel, wx.ID_ANY, 'First Month: ')
        value = monthPrettify(prj['first_month']) if prj else ''
        txtFirstMonth = wx.TextCtrl(panel, wx.ID_ANY, value, size=(50, -1))
        intervalLayout.Add(lblFirstMonth, 0, wx.ALL, 5)
        intervalLayout.Add(txtFirstMonth, 0, wx.ALL, 5)

        lblLastMonth = wx.StaticText(panel, wx.ID_ANY, 'Last Month: ')
        value = monthPrettify(prj['last_month']) if prj else ''
        txtLastMonth = wx.TextCtrl(panel, wx.ID_ANY, value, size=(50, -1))
        intervalLayout.Add(lblLastMonth, 0, wx.ALL, 5)
        intervalLayout.Add(txtLastMonth, 0, wx.ALL, 5)
        layout.Add(intervalLayout, 0, wx.ALL, 5)

        notesLayout = wx.BoxSizer(wx.VERTICAL)
        lblNotes = wx.StaticText(panel, wx.ID_ANY, 'Notes:')
        value = prj['notes'] if prj and prj['notes'] else ''
        txtNotes = wx.TextCtrl(panel, wx.ID_ANY, value,
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
