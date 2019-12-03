import ObjectListView as olv
import wx

import globals as gbl
import lib.month_lib as ml
import lib.ui_lib as uil
from dal.dao import Dao
import dal.prj_dal as prj_dal
from views.projects.detail_dlg import PrjDetailDlg


class TabPanel(wx.Panel):
    def __init__(self, parent, dataset):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(wx.Colour(gbl.COLOR_SCHEME.pnlBg))
        layout = wx.BoxSizer(wx.VERTICAL)

        self.dataset = dataset

        # Need properties for the filters
        self.theList = None
        self.srchValue = ''

        tbPanel = self.buildToolbarPanel()
        lstPanel = self.buildListPanel(self.dataset.rex)

        layout.Add(tbPanel, 0, wx.EXPAND | wx.ALL, 5)
        layout.Add(lstPanel, 0, wx.EXPAND | wx.ALL, 5)

        self.SetSizerAndFit(layout)

    def buildToolbarPanel(self):
        panel = wx.Panel(
            self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize
        )
        panel.SetBackgroundColour(wx.Colour(gbl.COLOR_SCHEME.tbBg))
        layout = wx.BoxSizer(wx.HORIZONTAL)

        addBtn = uil.toolbar_button(panel, 'Add')
        addBtn.Bind(wx.EVT_BUTTON, self.onAddBtnClick)
        layout.Add(addBtn, 0, wx.ALL, 5)

        dropBtn = uil.toolbar_button(panel, 'Drop')
        dropBtn.Bind(wx.EVT_BUTTON, self.onDropBtnClick)
        layout.Add(dropBtn, 0, wx.ALL, 5)

        lblNameFltr = uil.getToolbarLabel(panel, self.dataset.srchName + ':')
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

    def buildListPanel(self, data):
        panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.lstBg)
        layout = wx.BoxSizer(wx.HORIZONTAL)

        self.theList = olv.ObjectListView(panel, wx.ID_ANY,
                                          size=wx.Size(-1, 550),
                                          style=wx.LC_REPORT | wx.SUNKEN_BORDER)

        font = self.theList.GetFont()
        gbl.PRJ_NICKNAME_WIDTH = \
            uil.getWidestTextExtent(font, [x['nickname'] for x in data.values()])
        nameWidth = uil.getWidestTextExtent(font, [x['name'] for x in data.values()])

        self.theList.SetColumns([
            olv.ColumnDefn('Nickname', 'left', gbl.PRJ_NICKNAME_WIDTH, 'nickname'),
            olv.ColumnDefn('First Month', 'left', 105, 'first_month', stringConverter=ml.prettify),
            olv.ColumnDefn('Last Month', 'left', 100, 'last_month', stringConverter=ml.prettify),
            olv.ColumnDefn('PI', 'left', 150, 'PiName'),
            olv.ColumnDefn('PM', 'left', 150, 'PmName'),
            olv.ColumnDefn('Name', 'left', nameWidth, 'name'),
            olv.ColumnDefn('Notes', 'left', 0, 'notes')
        ])

        self.theList.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.onDblClick)
        self.theList.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.onRightClick)

        self.theList.SetBackgroundColour(gbl.COLOR_SCHEME.lstHdr)

        self.theList.SetObjects(list(data.values()))

        layout.Add(self.theList, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(layout)

        return panel

    def onDblClick(self, event):
        obj = event.EventObject.GetSelectedObject()
        asns = self.dataset.getAsns(Dao(), obj['id'])

        dlg = PrjDetailDlg(self, wx.ID_ANY, 'Project Details', prj['id'], asns)
        dlg.ShowModal()

    def onRightClick(self, event):
        prj = event.EventObject.GetSelectedObject()
        wx.MessageBox(prj['notes'], 'Notes', wx.OK | wx.ICON_INFORMATION)

    def onAddBtnClick(self, event):
        dlg = PrjDetailDlg(self, wx.ID_ANY, 'New Project', None, None)
        dlg.ShowModal()

    def onDropBtnClick(self, event):
        ids = [x['id'] for x in self.theList.GetSelectedObjects()]
        if not ids:
            wx.MessageBox('No projects selected!', 'Oops!',
                          wx.OK | wx.ICON_ERROR)
            return
        dlg = wx.MessageDialog(self, 'Drop selected projects?', 'Just making sure',
                               wx.YES_NO | wx.ICON_QUESTION)
        reply = dlg.ShowModal()
        if reply == wx.ID_YES:
            result = Project.delete(Dao(), ids)
            print(result)

    def onFltr(self, event):
        c = chr(event.GetUnicodeKey())
        if not c.isalpha():
            if c == '\b':
                self.srchValue = self.srchValue[:-1]
        else:
            self.srchValue += c
        col = self.theList.columns[0:1]
        if event.EventObject.Parent.Name == 'notesFltr':
            col = self.theList.columns[4:1]
        self.theList.SetFilter(olv.Filter.TextSearch(
            self.theList, columns=col, text=self.srchValue))
        self.theList.RepopulateList()
        event.Skip()

    def onFltrCancel(self, event):
        event.EventObject.Clear()
        self.theList.SetFilter(None)
        self.theList.RepopulateList()
        self.srchValue = ''
