import wx


class DetailDlg(wx.Dialog):
    def __init__(self, parent, winId, title, recId, asns):
        wx.Dialog.__init__(self, parent, winId, title, size=(1200, 500))
        layout = wx.BoxSizer(wx.HORIZONTAL)

        frmPanel, dtlPanel = self.getPanels(recId, asns)

        layout.Add(frmPanel, 0, wx.ALL, 5)
        layout.Add(dtlPanel, 0, wx.ALL, 5)

        self.SetSizer(layout)

    def getPanels(self, recId, asns):
        raise NotImplementedError("Please Implement this method")
