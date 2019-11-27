import wx
import wx.grid
import models.globals as gbl
from utils.ui_utils import getToolbarLabel
from models.month import Month
from datetime import date
import utils.buttons as btn_lib


class PercentEffort(object):
    def __init__(self, prj, percent):
        self.prj = prj
        self.percent = percent


class EffCell(object):
    def __init__(self, month):
        self.month = month
        self.total = 0
        self.efforts = []


class EffRow(object):
    def __init__(self, employee):
        self.employee = employee
        self.cells = []


class EffTab(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(gbl.COLOR_SCHEME.pnlBg)
        layout = wx.BoxSizer(wx.VERTICAL)

        self.grid = None
        self.rows = []

        tbPanel = self.buildToolbarPanel()
        layout.Add(tbPanel, 0, wx.EXPAND | wx.ALL, 5)

        self.lstPanel = self.buildGridPanel()
        layout.Add(self.lstPanel, 0, wx.EXPAND | wx.ALL, 5)

        self.SetSizerAndFit(layout)

        self.onRunClick(None)

    def buildToolbarPanel(self):
        panel = wx.Panel(
            self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize
        )
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.tbBg)
        layout = wx.BoxSizer(wx.HORIZONTAL)

        lblStart = getToolbarLabel(panel, 'Start:')
        lblStart.SetForegroundColour(wx.Colour(gbl.COLOR_SCHEME.tbFg))
        layout.Add(lblStart, 0, wx.ALL, 5)

        start = date.today()
        self.txtStart = Month.getMonthCtrl(panel, Month.d2month(start))
        layout.Add(self.txtStart, 0, wx.ALL, 5)

        lblThru = getToolbarLabel(panel, 'Thru:')
        lblThru.SetForegroundColour(wx.Colour(gbl.COLOR_SCHEME.tbFg))
        layout.Add(lblThru, 0, wx.ALL, 5)

        self.txtThru = Month.getMonthCtrl(panel, Month.datePlus(start, 11))
        layout.Add(self.txtThru, 0, wx.ALL, 5)

        btnRun = btn_lib.toolbar_button(panel, 'Run Query')
        btnRun.Bind(wx.EVT_BUTTON, self.onRunClick)
        layout.Add(btnRun, 0, wx.ALL, 5)

        panel.SetSizerAndFit(layout)

        return panel

    def buildGridPanel(self):
        panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.lstBg)

        return panel

    def onRunClick(self, event):
        if self.grid:
            self.grid.Destroy()
        self.rows = []

        start = self.txtStart.GetValue()
        thru = self.txtThru.GetValue()
        months = Month.getMonths(start, thru)
        self.buildDataSet(start, thru, months)

        self.grid = wx.grid.Grid(self.lstPanel, wx.ID_ANY)
        self.grid.CreateGrid(len(gbl.empRex), len(months) + 2)

        self.setGridAlignment()
        self.grid.SetRowLabelSize(0)
        self.grid.HideCol(0)
        self.grid.SetColSize(1, gbl.EMP_NAME_WIDTH)

        self.grid.SetDefaultCellBackgroundColour(gbl.COLOR_SCHEME.grdCellBg)
        self.grid.SetLabelBackgroundColour(gbl.COLOR_SCHEME.grdLblBg)

        self.grid.SetColLabelValue(0, 'EmpID')
        self.grid.SetColLabelValue(1, 'Employee')
        self.grid.SetColLabelValue(2, 'FTE')

        self.grid.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.onLeftClick)

        colnum = 3
        for month in months:
            self.grid.SetColLabelValue(colnum, month)
            colnum += 1

        for rownum in range(0, len(self.rows)):
            employee = gbl.empRex[self.rows[rownum].employee]
            self.grid.SetCellValue(rownum, 0, str(employee['id']))
            self.grid.SetCellValue(rownum, 1, employee['name'])
            self.grid.SetCellValue(rownum, 2, str(employee['fte']))
            for colnum in range(3, len(months) + 2):
                value = self.rows[rownum].cells[colnum - 3].total
                self.grid.SetCellValue(rownum, colnum, str(value))
                if value < employee['fte']:
                    self.grid.SetCellTextColour(rownum, colnum, 'red')

        layout = wx.BoxSizer(wx.HORIZONTAL)
        layout.Add(self.grid, 0, wx.ALL | wx.EXPAND, 5)

        # These 2 lines are required to get scroll bars on subsequent grids
        self.lstPanel.SetSizer(layout)
        self.Layout()

    def setGridAlignment(self):
        nrows = self.grid.GetNumberRows()
        ncols = self.grid.GetNumberCols()
        for i in range(nrows):
            for j in range(2, ncols):
                self.grid.SetCellAlignment(i, j, wx.ALIGN_RIGHT, wx.ALIGN_CENTER)

    def buildDataSet(self, start, thru, months):
        from models.assignment import Assignment

        asns = Assignment.get_for_timeframe(start, thru)
        self.emp_asns = {emp['id']: [] for emp in gbl.empRex.values()}

        for asn in asns:
            self.emp_asns[asn['employee_id']].append(asn)

        for emp in gbl.empRex:
            row = EffRow(emp)
            for month in months:
                cell = EffCell(month)
                for emp_asn in self.emp_asns[emp]:
                    uglyMo = Month.uglify(month)
                    if uglyMo < emp_asn['first_month'] or uglyMo > emp_asn['last_month']:
                        continue
                    cell.total += emp_asn['effort']
                    cell.efforts.append(
                        PercentEffort(emp_asn['project'], emp_asn['effort']))
                row.cells.append(cell)
            self.rows.append(row)

        self.breakdowns = self.build_breakdowns()

    def onLeftClick(self, event):
        from views.efforts.emp_brkdwn_dlg import EmployeeBreakdownDlg
        from views.efforts.month_brkdwn_dlg import MonthBreakdownDialog

        if event.Col == 2:
            return
        if event.Col == 1:
            empId = int(self.grid.GetCellValue(event.Row, 0))
            if not self.emp_asns[empId]:
                wx.MessageBox('No assignments!', 'Oops!',  wx.OK | wx.ICON_INFORMATION)
            dlg = EmployeeBreakdownDlg(self, wx.ID_ANY, self.emp_asns[empId])
            dlg.ShowModal()
        else:
            empId = self.grid.GetCellValue(event.Row, 0)
            empName = self.grid.GetCellValue(event.Row, 1)
            month = self.grid.GetColLabelValue(event.Col)
            key = empId + ':' + month
            dlg = MonthBreakdownDialog(self, wx.ID_ANY, empName, month, self.breakdowns[key])
            dlg.ShowModal()

    def build_breakdowns(self):
        d = {}
        for row in self.rows:
            for cell in row.cells:
                k = '%s:%s' % (row.employee, cell.month)
                d[k] = [{'project': pe.prj, 'percent': pe.percent} for pe in cell.efforts]
        return d


def getFteHrs(fte):
    return int(40 * fte / 100)
