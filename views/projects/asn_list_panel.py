import wx
import ObjectListView as olv
import globals as gbl
import lib.month_lib as ml
import lib.ui_lib as uil
from views.projects.asn_dlg import PrjAsnDlg


class PrjAsnListPanel(wx.Panel):
    def __init__(self, parent, prjId, asns):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(gbl.COLOR_SCHEME.pnlBg)
        layout = wx.BoxSizer(wx.VERTICAL)

        self.prj = gbl.prjRex[prjId] if prjId else None
        self.theList = None
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

        self.addBtn = uil.toolbar_button(panel, 'Add Assignment')
        self.addBtn.Bind(wx.EVT_BUTTON, self.onAddBtnClick)
        if not self.prj:
            self.addBtn.Disable()
        layout.Add(self.addBtn, 0, wx.ALL, 5)

        dropBtn = uil.toolbar_button(panel, 'Drop Assignments')
        dropBtn.Bind(wx.EVT_BUTTON, self.onDropBtnClick)
        layout.Add(dropBtn, 0, wx.ALL, 5)

        hlpBtn = uil.getHelpBtn(panel)
        hlpBtn.Bind(wx.EVT_BUTTON, uil.showListHelp)
        layout.Add(hlpBtn, 0, wx.ALL, 5)

        panel.SetSizer(layout)

        return panel

    def buildListPanel(self, data):
        panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.lstBg)
        layout = wx.BoxSizer(wx.HORIZONTAL)

        self.theList = olv.ObjectListView(panel, wx.ID_ANY,
                                          size=wx.Size(-1, 375),
                                          style=wx.LC_REPORT | wx.SUNKEN_BORDER)

        self.theList.SetColumns([
            olv.ColumnDefn('Employee', 'left', 200, 'employee'),
            olv.ColumnDefn('First Month', 'left', 105, 'first_month',
                           stringConverter=ml.prettify),
            olv.ColumnDefn('Last Month', 'left', 100, 'last_month',
                           stringConverter=ml.prettify),
            olv.ColumnDefn('Effort', 'left', 100, 'effort'),
        ])

        self.theList.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.onRightClick)
        self.theList.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.onDblClick)

        self.theList.SetObjects(data)

        layout.Add(self.theList, 1, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(layout)

        return panel

    def onRightClick(self, event):
        asn = self.theList.GetSelectedObject()
        msg = asn['notes'] if asn['notes'] else 'No notes'
        wx.MessageBox(msg, 'Notes', wx.OK | wx.ICON_INFORMATION)

    def onDblClick(self, event):
        asn = event.EventObject.GetSelectedObject()
        dlg = PrjAsnDlg(self, -1, 'Assignment Details', self.prj['id'], asn)
        dlg.ShowModal()

    def onAddBtnClick(self, event):
        dlg = PrjAsnDlg(self, -1, 'New Assignment', self.prj['id'], None)
        dlg.ShowModal()

    def onDropBtnClick(self, event):
        from dal.dao import Dao
        from models.project import Project

        ids = [x['id'] for x in self.theList.GetSelectedObjects()]
        if not ids:
            wx.MessageBox('No assignments selected!', 'Oops!',
                          wx.OK | wx.ICON_ERROR)
            return
        dlg = wx.MessageDialog(self, 'Drop selected assignments?', 'Just making sure',
                               wx.YES_NO | wx.ICON_QUESTION)
        reply = dlg.ShowModal()
        if reply == wx.ID_YES:
            result = Project.delete(Dao(), ids)
            print(result)

    def activateAddBtn(self):
        self.addBtn.Enable()
