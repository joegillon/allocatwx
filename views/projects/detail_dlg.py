import wx
from views.projects.asn_list_panel import PrjAsnListPanel
from views.projects.form_panel import PrjFormPanel


class PrjDetailDlg(wx.Dialog):
    def __init__(self, parent, winId, title, prj, asns):
        wx.Dialog.__init__(self, parent, winId, title, size=(1200, 500))
        layout = wx.BoxSizer(wx.HORIZONTAL)

        self.frmPanel = PrjFormPanel(self, prj)
        self.dtlPanel = PrjAsnListPanel(self, prj['nickname'] if prj else '', asns)

        layout.Add(self.frmPanel, 0, wx.ALL, 5)
        layout.Add(self.dtlPanel, 0, wx.ALL, 5)

        self.SetSizer(layout)
