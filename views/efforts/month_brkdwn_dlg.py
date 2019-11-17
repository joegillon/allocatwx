import wx
from ObjectListView import ObjectListView, ColumnDefn
import models.globals as gbl


class MonthBreakdownDialog(wx.Dialog):
    def __init__(self, parent, winId, employee, month, breakdown):
        wx.Dialog.__init__(self, parent, winId, size=(565, -1))
        layout = wx.BoxSizer(wx.VERTICAL)
        panel = wx.Panel(self, wx.ID_ANY)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.pnlBg)

        self.employee = employee
        self.month = month
        self.breakdown = breakdown

        tbPanel = self.buildToolbarPanel()
        lstPanel = self.buildListPanel()

        layout.Add(tbPanel, 0, wx.ALL | wx.EXPAND, 5)
        layout.Add(lstPanel, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizerAndFit(layout)

    def buildToolbarPanel(self):
        panel = wx.Panel(self, wx.ID_ANY)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.tbBg)
        layout = wx.BoxSizer(wx.HORIZONTAL)

        s = '%s @ %s' % (self.employee, self.month)
        lbl = wx.StaticText(panel, wx.ID_ANY, s)
        layout.Add(lbl, 0, wx.ALL, 5)

        panel.SetSizerAndFit(layout)

        return panel

    def buildListPanel(self):
        panel = wx.Panel(self, wx.ID_ANY)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.lstBg)
        layout = wx.BoxSizer(wx.HORIZONTAL)

        self.olv = ObjectListView(panel, wx.ID_ANY,
                                  size=wx.DefaultSize,
                                  style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.olv.SetColumns([
            ColumnDefn('Project', 'left', gbl.PRJ_NICKNAME_WIDTH, 'project'),
            ColumnDefn('% Effort', 'right', 100, 'percent')
        ])

        self.olv.SetObjects(self.breakdown)

        layout.Add(self.olv, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizerAndFit(layout)

        return panel
