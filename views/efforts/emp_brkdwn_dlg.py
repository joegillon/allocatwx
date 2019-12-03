import wx
import ObjectListView as olv
import globals as gbl
import lib.month_lib as ml


class EmployeeBreakdownDlg(wx.Dialog):
    def __init__(self, parent, winId, asns):
        wx.Dialog.__init__(self, parent, winId, size=(765, -1))
        layout = wx.BoxSizer(wx.VERTICAL)
        panel = wx.Panel(self, wx.ID_ANY)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.pnlBg)

        self.theList = None
        self.asns = asns

        tbPanel = self.buildToolbarPanel()
        lstPanel = self.buildListPanel()

        layout.Add(tbPanel, 0, wx.ALL | wx.EXPAND, 5)
        layout.Add(lstPanel, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizerAndFit(layout)

    def buildToolbarPanel(self):
        panel = wx.Panel(self, wx.ID_ANY)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.tbBg)
        layout = wx.BoxSizer(wx.HORIZONTAL)

        s = '%d assignments for %s' % (len(self.asns), self.asns[0]['employee'])
        lbl = wx.StaticText(panel, wx.ID_ANY, s)
        layout.Add(lbl, 0, wx.ALL, 5)

        panel.SetSizerAndFit(layout)

        return panel

    def buildListPanel(self):
        panel = wx.Panel(self, wx.ID_ANY)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.lstBg)
        layout = wx.BoxSizer(wx.HORIZONTAL)

        self.theList = olv.ObjectListView(panel, wx.ID_ANY,
                                          size=wx.DefaultSize,
                                          style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.theList.SetColumns([
            olv.ColumnDefn('Project', 'left', gbl.PRJ_NICKNAME_WIDTH, 'project'),
            olv.ColumnDefn('First Month', 'right', 105, 'first_month', stringConverter=ml.prettify),
            olv.ColumnDefn('Last Month', 'right', 100, 'last_month', stringConverter=ml.prettify),
            olv.ColumnDefn('% Effort', 'right', 100, 'effort')
        ])

        self.theList.SetObjects(self.asns)

        layout.Add(self.theList, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizerAndFit(layout)

        return panel
