import wx
from ObjectListView import ObjectListView, ColumnDefn, Filter
from views.projects.detail import PrjDetailDlg
from models.project import Project
from utils.strutils import getWidestTextDimension, monthPrettify


class PrjTab(wx.Panel):
    def __init__(self, parent, data):
            wx.Panel.__init__(self, parent, size=(900, 500))
            self.SetBackgroundColour(wx.Colour(79, 114, 142))

            self.op = None
            self.olv = None

            tbPanel = self.buildToolbarPanel()
            lstPanel = self.buildListPanel(data)

            frameSizer = wx.BoxSizer(wx.VERTICAL)
            frameSizer.Add(tbPanel, 0, wx.EXPAND | wx.ALL, 10)
            frameSizer.Add(lstPanel, 0, wx.EXPAND | wx.ALL, 10)

            self.SetSizerAndFit(frameSizer)

    def buildToolbarPanel(self):
        tbPanel = wx.Panel(
            self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize
        )
        tbPanel.SetBackgroundColour(wx.Colour(190, 130, 96))

        font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                       wx.FONTWEIGHT_BOLD)
        tbPanel.SetFont(font)
        tbPanel.SetForegroundColour('white')

        addBtn = wx.Button(tbPanel, wx.ID_ANY, label='Add Project',
                           pos=wx.DefaultPosition,
                           size=wx.DefaultSize,
                           style=0)
        addBtn.Bind(wx.EVT_BUTTON, self.on_addBtn_click)

        lblNickFltr = wx.StaticText(tbPanel, wx.ID_ANY, 'Nickname')
        nickFltr = wx.SearchCtrl(tbPanel, wx.ID_ANY, '', style=wx.TE_PROCESS_ENTER)
        nickFltr.ShowCancelButton(True)
        nickFltr.Bind(wx.EVT_TEXT_ENTER, self.onNickFltr)
        nickFltr.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, self.onFltrCancel)

        lblNotesFltr = wx.StaticText(tbPanel, wx.ID_ANY, 'Notes')
        notesFltr = wx.SearchCtrl(tbPanel, wx.ID_ANY, style=wx.TE_PROCESS_ENTER)
        notesFltr.ShowCancelButton(True)
        notesFltr.Bind(wx.EVT_TEXT_ENTER, self.onNotesFltr)
        notesFltr.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, self.onFltrCancel)

        tbSizer = wx.BoxSizer(wx.HORIZONTAL)
        tbSizer.Add(addBtn, 0, wx.ALL, 5)
        tbSizer.Add(lblNickFltr, 0, wx.ALL, 5)
        tbSizer.Add(nickFltr, 0, wx.ALL, 5)
        tbSizer.Add(lblNotesFltr, 0, wx.ALL, 5)
        tbSizer.Add(notesFltr, 0, wx.ALL, 5)

        tbPanel.SetSizer(tbSizer)

        return tbPanel

    def buildListPanel(self, data):
        listPanel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize)
        listPanel.SetBackgroundColour(wx.Colour(37, 63, 91))

        olv = ObjectListView(listPanel, wx.ID_ANY,
                             size=wx.Size(-1, 550),
                             style=wx.LC_REPORT | wx.SUNKEN_BORDER)

        font = olv.GetFont()
        nickWidth = getWidestTextDimension(
            [x['nickname'] for x in data],
            font.GetFaceName(), font.GetPointSize()
        )
        nameWidth = getWidestTextDimension(
            [x['name'] for x in data],
            font.GetFaceName(), font.GetPointSize()
        )

        olv.SetColumns([
            ColumnDefn('Nickname', 'left', nickWidth, 'nickname'),
            ColumnDefn('First Month', 'left', 105, 'first_month', stringConverter=monthPrettify),
            ColumnDefn('Last Month', 'left', 100, 'last_month', stringConverter=monthPrettify),
            ColumnDefn('Name', 'left', nameWidth, 'name'),
            ColumnDefn('Notes', 'left', 0, 'notes')
        ])

        olv.Bind(wx.EVT_LEFT_DOWN, self.left_click)
        olv.Bind(wx.EVT_RIGHT_DOWN, self.right_click)
        olv.Bind(wx.EVT_LIST_ITEM_SELECTED, self.selected)

        olv.SetObjects(data)
        self.olv = olv

        lstSizer = wx.BoxSizer(wx.HORIZONTAL)
        lstSizer.Add(olv, 1, wx.ALL | wx.EXPAND, 5)

        listPanel.SetSizer(lstSizer)

        return listPanel

    def selected(self, event):
        item = event.EventObject.GetSelectedObject()
        if self.op == 'left':
            asns = Project.getAsns(item['id'])

            dlg = PrjDetailDlg(self, -1, 'Project Details', item, asns)
            dlg.ShowModal()
            return

        wx.MessageBox(item['notes'], 'Notes', wx.OK | wx.ICON_INFORMATION)

    def left_click(self, event):
        self.op = 'left'
        event.Skip()

    def right_click(self, event):
        self.op = 'right'
        event.Skip()

    def on_addBtn_click(self, event):
        print('boo')

    def onNickFltr(self, event):
        s = event.GetString()
        self.olv.SetFilter(Filter.TextSearch(
            self.olv, columns=self.olv.columns[0:1], text=s))
        self.olv.RepopulateList()

    def onFltrCancel(self, event):
        event.EventObject.Clear()
        self.olv.SetFilter(None)
        self.olv.RepopulateList()

    def onNotesFltr(self, event):
        s = event.GetString()
        self.olv.SetFilter(Filter.TextSearch(
            self.olv, columns=self.olv.columns[4:1], text=s))
        self.olv.RepopulateList()
