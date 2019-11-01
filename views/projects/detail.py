import wx
from views.form_panel import FormPanel
from views.detail_panel import DetailPanel


class PrjDetailDlg(wx.Dialog):
    def __init__(self, parent, win_id, title, prj, asns):
        wx.Dialog.__init__(self, parent, win_id, title, size=(900, 500))

        self.frmPanel = FormPanel(self, prj)
        self.dtlPanel = DetailPanel(self, asns)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.frmPanel, 0, wx.ALL, 5)
        sizer.Add(self.dtlPanel, 0, wx.ALL, 5)

        self.SetSizer(sizer)
