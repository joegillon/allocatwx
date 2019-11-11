import wx
from views.projects.asn_form_panel import PrjAsnFormPanel


class PrjAsnDlg(wx.Dialog):
    def __init__(self, parent, winId, title, prjNickname, asn):
        wx.Dialog.__init__(self, parent, winId, title, size=(500, 400))
        layout = wx.BoxSizer(wx.VERTICAL)

        panel = PrjAsnFormPanel(self, prjNickname, asn)

        layout.Add(panel, 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(layout)
