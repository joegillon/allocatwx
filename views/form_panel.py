import wx
from utils.strutils import monthPrettify


class FormPanel(wx.Panel):
    def __init__(self, parent, prj):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(wx.Colour(116, 65, 43))

        tbPanel = wx.Panel(
            self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize
        )
        tbPanel.SetBackgroundColour(wx.Colour(190, 130, 96))
        dropBtn = wx.Button(tbPanel, wx.ID_ANY, label='Drop Project')
        # dropBtn.Bind()

        saveBtn = wx.Button(tbPanel, wx.ID_ANY, label='Save Project')
        # saveBtn.Bind()

        tbSizer = wx.BoxSizer(wx.HORIZONTAL)
        tbSizer.Add(dropBtn, 0, wx.ALL, 5)
        tbSizer.Add(saveBtn, 0, wx.ALL, 5)
        tbPanel.SetSizer(tbSizer)

        frmPanel = wx.Panel(
            self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize
        )
        frmPanel.SetBackgroundColour(wx.Colour(215, 176, 149))
        frmPanel.SetForegroundColour('black')

        lblName = wx.StaticText(frmPanel, wx.ID_ANY, 'Project Name: ')
        self.txtName = wx.TextCtrl(frmPanel, wx.ID_ANY, '', size=(500, -1))
        nameSizer = wx.BoxSizer(wx.HORIZONTAL)
        nameSizer.Add(lblName, 0, wx.ALL, 5)
        nameSizer.Add(self.txtName, 0, wx.ALL | wx.EXPAND, 5)

        lblNickname = wx.StaticText(frmPanel, wx.ID_ANY, 'Nickname: ')
        self.txtNickname = wx.TextCtrl(frmPanel, wx.ID_ANY, '', size=(400, -1))
        nicknameSizer = wx.BoxSizer(wx.HORIZONTAL)
        nicknameSizer.Add(lblNickname, 0, wx.ALL, 5)
        nicknameSizer.Add(self.txtNickname, 0, wx.ALL, 5)

        lblFirstMonth = wx.StaticText(frmPanel, wx.ID_ANY, 'First Month: ')
        self.txtFirstMonth = wx.TextCtrl(frmPanel, wx.ID_ANY, '', size=(50, -1))
        lblLastMonth = wx.StaticText(frmPanel, wx.ID_ANY, 'Last Month: ')
        self.txtLastMonth = wx.TextCtrl(frmPanel, wx.ID_ANY, '', size=(50, -1))
        monthSizer = wx.BoxSizer(wx.HORIZONTAL)
        monthSizer.Add(lblFirstMonth, 0, wx.ALL, 5)
        monthSizer.Add(self.txtFirstMonth, 0, wx.ALL, 5)
        monthSizer.Add(lblLastMonth, 0, wx.ALL, 5)
        monthSizer.Add(self.txtLastMonth, 0, wx.ALL, 5)

        lblNotes = wx.StaticText(frmPanel, wx.ID_ANY, 'Notes:')
        self.txtNotes = wx.TextCtrl(frmPanel, wx.ID_ANY, '',
                                    style=wx.TE_MULTILINE, size=(500, 200))
        notesSizer = wx.BoxSizer(wx.VERTICAL)
        notesSizer.Add(lblNotes, 0, wx.ALL, 5)
        notesSizer.Add(self.txtNotes, 0, wx.ALL, 5)

        frmSizer = wx.BoxSizer(wx.VERTICAL)
        frmSizer.Add(nameSizer, 0, wx.ALL | wx.EXPAND, 5)
        frmSizer.Add(nicknameSizer, 0, wx.ALL | wx.EXPAND, 5)
        frmSizer.Add(monthSizer, 0, wx.ALL, 5)
        frmSizer.Add(notesSizer, 0, wx.ALL, 5)
        frmPanel.SetSizer(frmSizer)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(tbPanel, 0, wx.ALL, 5)
        sizer.Add(frmPanel, 0, wx.ALL | wx.EXPAND, 5)
        self.SetSizer(sizer)

        if prj:
            self.load(prj)

    def load(self, prj):
        self.txtName.SetValue(prj['name'])
        self.txtNickname.SetValue(prj['nickname'])
        self.txtFirstMonth.SetValue(monthPrettify(prj['first_month']))
        self.txtLastMonth.SetValue(monthPrettify(prj['last_month']))
        self.txtNotes.SetValue(prj['notes'])
