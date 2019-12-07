import wx


class AsnDlg(wx.Dialog):
    def __init__(self, parent, winId, title, ownerId, asn):
        wx.Dialog.__init__(self, parent, winId, title, size=(500, 400))
        layout = wx.BoxSizer(wx.VERTICAL)

        panel = self.getPanel(ownerId, asn)

        layout.Add(panel, 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(layout)

    def getPanel(self, ownerId, asn):
        raise NotImplementedError("Please Implement this method")
