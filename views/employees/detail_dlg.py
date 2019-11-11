import wx
from views.employees.asn_list_panel import EmpAsnListPanel
from views.employees.form_panel import EmpFormPanel


class EmpDetailDlg(wx.Dialog):
    def __init__(self, parent, winId, title, emp, asns):
        wx.Dialog.__init__(self, parent, winId, title, size=(1200, 500))
        layout = wx.BoxSizer(wx.HORIZONTAL)

        self.frmPanel = EmpFormPanel(self, emp)
        self.dtlPanel = EmpAsnListPanel(self, emp['name'] if emp else '', asns)

        layout.Add(self.frmPanel, 0, wx.ALL, 5)
        layout.Add(self.dtlPanel, 0, wx.ALL, 5)

        self.SetSizer(layout)
