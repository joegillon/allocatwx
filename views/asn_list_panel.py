import wx
import ObjectListView as olv
import globals as gbl
import lib.month_lib as ml
import lib.ui_lib as uil


class AsnListPanel(wx.Panel):
    def __init__(self, parent, tblName, rec, asns, dlg, dal):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(gbl.COLOR_SCHEME.pnlBg)
        layout = wx.BoxSizer(wx.VERTICAL)

        self.tblName = tblName
        self.rec = rec
        self.dlg = dlg
        self.dal = dal
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
        if not self.rec:
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
            olv.ColumnDefn(self.tblName, 'left', 200, self.tblName.lower()),
            olv.ColumnDefn('First Month', 'left', 105, 'first_month', stringConverter=ml.prettify),
            olv.ColumnDefn('Last Month', 'left', 100, 'last_month', stringConverter=ml.prettify),
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
        dlg = self.dlg(self, -1, 'Assignment Details', self.rec['id'], asn)
        dlg.ShowModal()

    def onAddBtnClick(self, event):
        dlg = self.dlg(self, -1, 'New Assignment', self.rec['id'], None)
        dlg.ShowModal()

    def onDropBtnClick(self, event):
        from dal.dao import Dao

        ids = [x['id'] for x in self.theList.GetSelectedObjects()]
        if not ids:
            wx.MessageBox('No assignments selected!', 'Oops!',
                          wx.OK | wx.ICON_ERROR)
            return
        dlg = wx.MessageDialog(self, 'Drop selected assignments?', 'Just making sure',
                               wx.YES_NO | wx.ICON_QUESTION)
        reply = dlg.ShowModal()
        if reply == wx.ID_YES:
            result = self.dal.delete(Dao(), ids)
            print(result)

    def activateAddBtn(self):
        self.addBtn.Enable()
