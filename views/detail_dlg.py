import wx


class DetailDlg(wx.Dialog):
    def __init__(self, parent, winId, title, ownerId):
        wx.Dialog.__init__(self, parent, winId, title, size=(1200, 500))
        layout = wx.BoxSizer(wx.HORIZONTAL)

        frmPanel, dtlPanel = self.getPanels(ownerId)

        layout.Add(frmPanel, 0, wx.ALL, 5)
        layout.Add(dtlPanel, 0, wx.ALL, 5)

        self.SetSizer(layout)

    def getPanels(self, ownerId):
        raise NotImplementedError("Please Implement this method")
