import wx
from views.employees.asn_list_panel import EmpAsnListPanel
from views.employees.form_panel import EmpFormPanel


class EmpDetailDlg(wx.Dialog):
    def __init__(self, parent, winId, title, empId, asns):
        wx.Dialog.__init__(self, parent, winId, title, size=(1200, 500))
        layout = wx.BoxSizer(wx.HORIZONTAL)

        self.frmPanel = EmpFormPanel(self, empId)
        self.dtlPanel = EmpAsnListPanel(self, empId, asns)

        layout.Add(self.frmPanel, 0, wx.ALL, 5)
        layout.Add(self.dtlPanel, 0, wx.ALL, 5)

        self.SetSizer(layout)
