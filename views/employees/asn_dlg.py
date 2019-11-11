import wx
from views.employees.asn_form_panel import EmpAsnFormPanel


class EmpAsnDlg(wx.Dialog):
    def __init__(self, parent, winId, title, empName, asn):
        wx.Dialog.__init__(self, parent, winId, title, size=(500, 400))
        layout = wx.BoxSizer(wx.VERTICAL)

        panel = EmpAsnFormPanel(self, empName, asn)

        layout.Add(panel, 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(layout)
