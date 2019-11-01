import wx
import wx.grid


class DetailPanel(wx.Panel):
    def __init__(self, parent, data):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(wx.Colour(79, 114, 142))

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

        grdPanel = wx.Panel(
            self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize
        )
        grdPanel.SetBackgroundColour(wx.Colour(116, 65, 43))
        self.grid = wx.grid.Grid(grdPanel, wx.ID_ANY)
        self.grid.CreateGrid(len(data), 7)
        self.grid.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.on_cell_click)
        self.load(data)
        self.grid.HideCol(0)
        self.grid.HideCol(1)
        grdSizer = wx.BoxSizer(wx.HORIZONTAL)
        grdSizer.Add(self.grid, 0, wx.ALL, 5)
        grdPanel.SetSizer(grdSizer)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(tbPanel, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(grdPanel, 0, wx.ALL, 5)
        self.SetSizer(sizer)

        self.grid.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.on_cell_click)

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
