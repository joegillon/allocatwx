import wx
from ObjectListView import ObjectListView, ColumnDefn, Filter
from utils.strutils import getWidestTextDimension, monthPrettify


class DetailPanel(wx.Panel):
    def __init__(self, parent, data):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(wx.Colour(79, 114, 142))

        self.olv = None

        tbPanel = self.buildToolbarPanel()
        lstPanel = self.buildListPanel(data)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(tbPanel, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(lstPanel, 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizerAndFit(sizer)

    def buildToolbarPanel(self):
        tbPanel = wx.Panel(
            self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize
        )
        tbPanel.SetBackgroundColour(wx.Colour(190, 130, 96))
        addBtn = wx.Button(tbPanel, wx.ID_ANY, label='Add Assignment')
        # addBtn.Bind()

        dropBtn = wx.Button(tbPanel, wx.ID_ANY, label='Drop Assignment')
        # dropBtn.Bind()

        saveBtn = wx.Button(tbPanel, wx.ID_ANY, label='Save Assignment')
        # saveBtn.Bind()

        tbSizer = wx.BoxSizer(wx.HORIZONTAL)
        tbSizer.Add(addBtn, 0, wx.ALL, 5)
        tbSizer.Add(dropBtn, 0, wx.ALL, 5)
        tbSizer.Add(saveBtn, 0, wx.ALL, 5)
        tbPanel.SetSizer(tbSizer)

        return tbPanel

    def buildListPanel(self, data):
        listPanel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize)
        listPanel.SetBackgroundColour(wx.Colour(37, 63, 91))

        olv = ObjectListView(listPanel, wx.ID_ANY,
                             size=wx.Size(-1, 550),
                             style=wx.LC_REPORT | wx.SUNKEN_BORDER)

        font = olv.GetFont()
        empWidth = getWidestTextDimension(
            [x['employee'] for x in data],
            font.GetFaceName(), font.GetPointSize()
        )

        olv.SetColumns([
            ColumnDefn('Employee', 'left', 200, 'employee'),
            ColumnDefn('First Month', 'left', 105, 'first_month', stringConverter=monthPrettify),
            ColumnDefn('Last Month', 'left', 100, 'last_month', stringConverter=monthPrettify),
            ColumnDefn('Effort', 'left', 100, 'effort'),
        ])

        # olv.Bind(wx.EVT_LEFT_DOWN, self.left_click)
        # olv.Bind(wx.EVT_RIGHT_DOWN, self.right_click)
        # olv.Bind(wx.EVT_LIST_ITEM_SELECTED, self.selected)

        olv.SetObjects(data)
        self.olv = olv

        lstSizer = wx.BoxSizer(wx.HORIZONTAL)
        lstSizer.Add(olv, 1, wx.ALL | wx.EXPAND, 5)

        listPanel.SetSizer(lstSizer)

        return listPanel

    def load(self, data):
        self.grid.ClearGrid()
        for rownum in range(len(data)):
            self.grid.SetCellValue(rownum, 0, str(data[rownum]['id']))
            self.grid.SetCellValue(rownum, 1, str(data[rownum]['employee_id']))
            self.grid.SetCellValue(rownum, 2, data[rownum]['employee'])
            self.grid.SetCellValue(rownum, 3, data[rownum]['first_month'])
            self.grid.SetCellValue(rownum, 4, data[rownum]['last_month'])
            self.grid.SetCellValue(rownum, 5, str(data[rownum]['effort']))

    def on_cell_click(self, event):
        row = event.GetRow()
        asnid = self.grid.GetCellValue(row, 0)
        print(asnid)

        # dlg = PrjDetailFrame(self, -1, 'Project Details')
        # dlg.ShowModal()
