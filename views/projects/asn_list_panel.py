import wx
from ObjectListView import ObjectListView, ColumnDefn
from models.month import Month
from views.projects.asn_dlg import PrjAsnDlg
import models.globals as gbl
import utils.buttons as btn_lib


class PrjAsnListPanel(wx.Panel):
    def __init__(self, parent, prjNickname, asns):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(gbl.COLOR_SCHEME.pnlBg)
        layout = wx.BoxSizer(wx.VERTICAL)

        self.prjNickname = prjNickname
        self.olv = None
        self.op = None
        self.addBtn = None

        tbPanel = self.buildToolbarPanel()
        lstPanel = self.buildListPanel(asns)

        layout.Add(tbPanel, 0, wx.ALL | wx.EXPAND, 5)
        layout.Add(lstPanel, 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizerAndFit(layout)

    def buildToolbarPanel(self):
        panel = wx.Panel(
            self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize
        )
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.tbBg)
        layout = wx.BoxSizer(wx.HORIZONTAL)

        self.addBtn = btn_lib.toolbar_button(panel, 'Add Assignment')
        self.addBtn.Bind(wx.EVT_BUTTON, self.onAddBtnClick)
        if not self.prjNickname:
            self.addBtn.Disable()
        layout.Add(self.addBtn, 0, wx.ALL, 5)

        dropBtn = btn_lib.toolbar_button(panel, 'Drop Assignments')
        dropBtn.Bind(wx.EVT_BUTTON, self.onDropBtnClick)
        layout.Add(dropBtn, 0, wx.ALL, 5)

        hlpBtn = gbl.getHelpBtn(panel)
        hlpBtn.Bind(wx.EVT_BUTTON, gbl.showListHelp)
        layout.Add(hlpBtn, 0, wx.ALL, 5)

        panel.SetSizer(layout)

        return panel

    def buildListPanel(self, data):
        panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.lstBg)
        layout = wx.BoxSizer(wx.HORIZONTAL)

        olv = ObjectListView(panel, wx.ID_ANY,
                             size=wx.Size(-1, 375),
                             style=wx.LC_REPORT | wx.SUNKEN_BORDER)

        olv.SetColumns([
            ColumnDefn('Employee', 'left', 200, 'employee'),
            ColumnDefn('First Month', 'left', 105, 'first_month', stringConverter=Month.prettify),
            ColumnDefn('Last Month', 'left', 100, 'last_month', stringConverter=Month.prettify),
            ColumnDefn('Effort', 'left', 100, 'effort'),
        ])

        olv.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.onRightClick)
        olv.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.onDblClick)

        olv.SetObjects(data)
        self.olv = olv

        layout.Add(olv, 1, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(layout)

        return panel

    def onRightClick(self, event):
        asn = self.olv.GetSelectedObject()
        msg = asn['notes'] if asn['notes'] else 'No notes'
        wx.MessageBox(msg, 'Notes', wx.OK | wx.ICON_INFORMATION)

    def onDblClick(self, event):
        asn = event.EventObject.GetSelectedObject()
        dlg = PrjAsnDlg(self, -1, 'Assignment Details', self.prjNickname, asn)
        dlg.ShowModal()

    def onAddBtnClick(self, event):
        dlg = PrjAsnDlg(self, -1, 'New Assignment', self.prjNickname, None)
        dlg.ShowModal()

    def onDropBtnClick(self, event):
        ids = [x['id'] for x in self.olv.GetSelectedObjects()]
        if not ids:
            wx.MessageBox('No assignments selected!', 'Oops!',
                          wx.OK | wx.ICON_ERROR)
            return
        dlg = wx.MessageDialog(self, 'Drop selected assignments?', 'Just making sure',
                               wx.YES_NO | wx.ICON_QUESTION)
        reply = dlg.ShowModal()
        if reply == wx.ID_YES:
            print(ids)

    def activateAddBtn(self):
        self.addBtn.Enable()
