import wx
import ObjectListView as olv
import globals as gbl
import lib.ui_lib as uil


class TabPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(wx.Colour(gbl.COLOR_SCHEME.pnlBg))
        layout = wx.BoxSizer(wx.VERTICAL)

        # Need properties for the filters
        self.theList = None
        self.srchTarget = ''
        self.srchFld = ''
        self.ownerName = ''
        self.rex = {}

        self.setProps()

        tbPanel = self.buildToolbarPanel()
        lstPanel = self.buildListPanel()

        layout.Add(tbPanel, 0, wx.EXPAND | wx.ALL, 5)
        layout.Add(lstPanel, 0, wx.EXPAND | wx.ALL, 5)

        self.SetSizerAndFit(layout)

    def setProps(self):
        raise NotImplementedError("Please Implement this method")

    def buildToolbarPanel(self):
        panel = wx.Panel(
            self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize
        )
        panel.SetBackgroundColour(wx.Colour(gbl.COLOR_SCHEME.tbBg))
        layout = wx.BoxSizer(wx.HORIZONTAL)

        addBtn = uil.toolbar_button(panel, 'Add ' + self.ownerName)
        addBtn.Bind(wx.EVT_BUTTON, self.onAddBtnClick)
        layout.Add(addBtn, 0, wx.ALL, 5)

        dropBtn = uil.toolbar_button(panel, 'Drop ' + self.ownerName + '(s)')
        dropBtn.Bind(wx.EVT_BUTTON, self.onDropBtnClick)
        layout.Add(dropBtn, 0, wx.ALL, 5)

        lblNameFltr = uil.getToolbarLabel(panel, self.srchFld + ':')
        lblNameFltr.SetForegroundColour(wx.Colour(gbl.COLOR_SCHEME.tbFg))
        layout.Add(lblNameFltr, 0, wx.ALL, 5)
        nameFltr = wx.SearchCtrl(panel, wx.ID_ANY, '',
                                 style=wx.TE_PROCESS_ENTER, name='nameFltr')
        nameFltr.ShowCancelButton(True)
        nameFltr.Bind(wx.EVT_CHAR, self.onFltr)
        nameFltr.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, self.onFltrCancel)
        layout.Add(nameFltr, 0, wx.ALL, 5)

        lblNotesFltr = uil.getToolbarLabel(panel, 'Notes')
        lblNotesFltr.SetForegroundColour(wx.Colour(gbl.COLOR_SCHEME.tbFg))
        layout.Add(lblNotesFltr, 0, wx.ALL, 5)

        notesFltr = wx.SearchCtrl(panel, wx.ID_ANY,
                                  style=wx.TE_PROCESS_ENTER, name='notesFltr')
        notesFltr.ShowCancelButton(True)
        notesFltr.Bind(wx.EVT_CHAR, self.onFltr)
        notesFltr.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, self.onFltrCancel)
        layout.Add(notesFltr, 0, wx.ALL, 5)

        hlpBtn = uil.getHelpBtn(panel)
        hlpBtn.Bind(wx.EVT_BUTTON, uil.showListHelp)
        layout.Add(hlpBtn, 0, wx.ALL, 5)

        panel.SetSizerAndFit(layout)

        return panel

    def buildListPanel(self):
        panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.lstBg)
        layout = wx.BoxSizer(wx.HORIZONTAL)

        self.theList = olv.ObjectListView(panel, wx.ID_ANY,
                                          size=wx.Size(-1, 600),
                                          style=wx.LC_REPORT | wx.SUNKEN_BORDER)

        self.buildList()

        self.theList.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.onDblClick)
        self.theList.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.onRightClick)

        self.theList.SetBackgroundColour(gbl.COLOR_SCHEME.lstHdr)

        layout.Add(self.theList, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(layout)

        self.loadList(list(self.rex.values()))

        return panel

    def buildList(self):
        raise NotImplementedError("Please Implement this method")

    def loadList(self, data):
        sorted_data = sorted(data, key=lambda i: i[self.srchFld.lower()])
        self.theList.SetObjects(sorted_data)

    def onDblClick(self, event):
        owner = event.EventObject.GetSelectedObject()
        dlg = self.getDetailDlg(owner['id'])
        dlg.ShowModal()

    def getDetailDlg(self, ownerId=None):
        raise NotImplementedError("Please Implement this method")

    def onRightClick(self, event):
        obj = event.EventObject.GetSelectedObject()
        wx.MessageBox(obj['notes'], 'Notes', wx.OK | wx.ICON_INFORMATION)

    def onAddBtnClick(self, event):
        dlg = self.getDetailDlg()
        dlg.ShowModal()

    def onDropBtnClick(self, event):
        ids = [x['id'] for x in self.theList.GetSelectedObjects()]
        if not ids:
            msg = 'No records selected!'
            wx.MessageBox(msg, 'Oops!',
                          wx.OK | wx.ICON_ERROR)
            return
        msg = 'Drop selected records?'
        dlg = wx.MessageDialog(self, msg, 'Just making sure',
                               wx.YES_NO | wx.ICON_QUESTION)
        reply = dlg.ShowModal()
        if reply == wx.ID_YES:
            result = self.dropRex(ids)
            print(result)

    def dropRex(self, ids):
        raise NotImplementedError("Please Implement this method")

    def onFltr(self, event):
        c = chr(event.GetUnicodeKey())
        if not c.isalpha():
            if c == '\b':
                self.srchTarget = self.srchTarget[:-1]
        else:
            self.srchTarget += c
        col = self.theList.columns[0:1]
        if event.EventObject.Parent.Name == 'notesFltr':
            col = self.theList.columns[4:1]
        self.theList.SetFilter(olv.Filter.TextSearch(
            self.theList, columns=col, text=self.srchTarget))
        self.theList.RepopulateList()
        event.Skip()

    def onFltrCancel(self, event):
        event.EventObject.Clear()
        self.theList.SetFilter(None)
        self.theList.RepopulateList()
        self.srchTarget = ''
