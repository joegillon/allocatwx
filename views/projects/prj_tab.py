import wx
from ObjectListView import ObjectListView, ColumnDefn, Filter
from views.projects.detail_dlg import PrjDetailDlg
from models.project import Project
import models.globals as gbl
from utils.strutils import getWidestTextExtent
from models.month import Month
import utils.buttons as btn_lib


class PrjTab(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(wx.Colour(gbl.COLOR_SCHEME.pnlBg))
        layout = wx.BoxSizer(wx.VERTICAL)

        # Need properties for the filters
        self.olv = None
        self.srchValue = ''

        tbPanel = self.buildToolbarPanel()
        lstPanel = self.buildListPanel(gbl.prjRex)

        layout.Add(tbPanel, 0, wx.EXPAND | wx.ALL, 5)
        layout.Add(lstPanel, 0, wx.EXPAND | wx.ALL, 5)

        self.SetSizerAndFit(layout)

    def buildToolbarPanel(self):
        panel = wx.Panel(
            self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize
        )
        panel.SetBackgroundColour(wx.Colour(gbl.COLOR_SCHEME.tbBg))
        layout = wx.BoxSizer(wx.HORIZONTAL)

        font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                       wx.FONTWEIGHT_BOLD)

        addBtn = btn_lib.toolbar_button(panel, 'Add Project')
        addBtn.Bind(wx.EVT_BUTTON, self.onAddBtnClick)
        layout.Add(addBtn, 0, wx.ALL, 5)

        dropBtn = btn_lib.toolbar_button(panel, 'Drop Projects')
        dropBtn.Bind(wx.EVT_BUTTON, self.onDropBtnClick)
        layout.Add(dropBtn, 0, wx.ALL, 5)

        lblNickFltr = wx.StaticText(panel, wx.ID_ANY, 'Nickname:')
        lblNickFltr.SetFont(font)
        lblNickFltr.SetForegroundColour(wx.Colour(gbl.COLOR_SCHEME.tbFg))
        layout.Add(lblNickFltr, 0, wx.ALL, 5)

        nickFltr = wx.SearchCtrl(panel, wx.ID_ANY, '', style=wx.TE_PROCESS_ENTER, name='nickFltr')
        nickFltr.ShowCancelButton(True)
        nickFltr.Bind(wx.EVT_CHAR, self.onFltr)
        nickFltr.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, self.onFltrCancel)
        layout.Add(nickFltr, 0, wx.ALL, 5)

        lblNotesFltr = wx.StaticText(panel, wx.ID_ANY, 'Notes')
        lblNotesFltr.SetFont(font)
        lblNotesFltr.SetForegroundColour(wx.Colour(gbl.COLOR_SCHEME.tbFg))
        layout.Add(lblNotesFltr, 0, wx.ALL, 5)

        notesFltr = wx.SearchCtrl(panel, wx.ID_ANY, style=wx.TE_PROCESS_ENTER, name='notesFltr')
        notesFltr.ShowCancelButton(True)
        notesFltr.Bind(wx.EVT_CHAR, self.onFltr)
        notesFltr.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, self.onFltrCancel)
        layout.Add(notesFltr, 0, wx.ALL, 5)

        hlpBtn = gbl.getHelpBtn(panel)
        hlpBtn.Bind(wx.EVT_BUTTON, gbl.showListHelp)
        layout.Add(hlpBtn, 0, wx.ALL, 5)

        panel.SetSizerAndFit(layout)

        return panel

    def buildListPanel(self, data):
        panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.lstBg)
        layout = wx.BoxSizer(wx.HORIZONTAL)

        self.olv = ObjectListView(panel, wx.ID_ANY,
                                  size=wx.Size(-1, 550),
                                  style=wx.LC_REPORT | wx.SUNKEN_BORDER)

        font = self.olv.GetFont()
        gbl.PRJ_NICKNAME_WIDTH = getWidestTextExtent(font, [x['nickname'] for x in data])
        nameWidth = getWidestTextExtent(font, [x['name'] for x in data])

        self.olv.SetColumns([
            ColumnDefn('Nickname', 'left', gbl.PRJ_NICKNAME_WIDTH, 'nickname'),
            ColumnDefn('First Month', 'left', 105, 'first_month', stringConverter=Month.prettify),
            ColumnDefn('Last Month', 'left', 100, 'last_month', stringConverter=Month.prettify),
            ColumnDefn('PI', 'left', 150, 'PiName'),
            ColumnDefn('PM', 'left', 150, 'PmName'),
            ColumnDefn('Name', 'left', nameWidth, 'name'),
            ColumnDefn('Notes', 'left', 0, 'notes')
        ])

        self.olv.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.onDblClick)
        self.olv.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.onRightClick)

        self.olv.SetBackgroundColour(gbl.COLOR_SCHEME.lstHdr)

        self.olv.SetObjects(data)

        layout.Add(self.olv, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(layout)

        return panel

    def onDblClick(self, event):
        prj = event.EventObject.GetSelectedObject()
        asns = Project.getAsns(prj['id'])

        dlg = PrjDetailDlg(self, wx.ID_ANY, 'Project Details', prj, asns)
        dlg.ShowModal()

    def onRightClick(self, event):
        prj = event.EventObject.GetSelectedObject()
        wx.MessageBox(prj['notes'], 'Notes', wx.OK | wx.ICON_INFORMATION)

    def onAddBtnClick(self, event):
        dlg = PrjDetailDlg(self, wx.ID_ANY, 'New Project', None, None)
        dlg.ShowModal()

    def onDropBtnClick(self, event):
        ids = [x['id'] for x in self.olv.GetSelectedObjects()]
        if not ids:
            wx.MessageBox('No projects selected!', 'Oops!',
                          wx.OK | wx.ICON_ERROR)
            return
        dlg = wx.MessageDialog(self, 'Drop selected projects?', 'Just making sure',
                               wx.YES_NO | wx.ICON_QUESTION)
        reply = dlg.ShowModal()
        if reply == wx.ID_YES:
            print(ids)

    def onFltr(self, event):
        c = chr(event.GetUnicodeKey())
        if not c.isalpha():
            if c == '\b':
                self.srchValue = self.srchValue[:-1]
        else:
            self.srchValue += c
        col = self.olv.columns[0:1]
        if event.EventObject.Parent.Name == 'notesFltr':
            col = self.olv.columns[4:1]
        self.olv.SetFilter(Filter.TextSearch(
            self.olv, columns=col, text=self.srchValue))
        self.olv.RepopulateList()
        event.Skip()

    def onFltrCancel(self, event):
        event.EventObject.Clear()
        self.olv.SetFilter(None)
        self.olv.RepopulateList()
        self.srchValue = ''
