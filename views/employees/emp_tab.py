import wx
from ObjectListView import ObjectListView, ColumnDefn, Filter
from views.employees.detail_dlg import EmpDetailDlg
from models.employee import Employee
import models.globals as gbl
from utils.strutils import getWidestTextExtent, monthPrettify


class EmpTab(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(gbl.PANEL_BG_COLOR)
        layout = wx.BoxSizer(wx.VERTICAL)

        # Need properties for the filters
        self.olv = None
        self.srchValue = ''

        tbPanel = self.buildToolbarPanel()
        lstPanel = self.buildListPanel(gbl.empRex)

        layout.Add(tbPanel, 0, wx.EXPAND | wx.ALL, 5)
        layout.Add(lstPanel, 0, wx.EXPAND | wx.ALL, 5)

        self.SetSizerAndFit(layout)

    def buildToolbarPanel(self):
        panel = wx.Panel(
            self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize
        )
        panel.SetBackgroundColour(gbl.TOOLBAR_BG_COLOR)
        layout = wx.BoxSizer(wx.HORIZONTAL)

        font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                       wx.FONTWEIGHT_BOLD)

        addBtn = wx.Button(panel, wx.ID_ANY, label='Add Employee',
                           pos=wx.DefaultPosition,
                           size=wx.DefaultSize,
                           style=0)
        addBtn.Bind(wx.EVT_BUTTON, self.onAddBtnClick)

        dropBtn = wx.Button(panel, wx.ID_ANY, label='Drop Employees')
        dropBtn.Bind(wx.EVT_BUTTON, self.onDropBtnClick)

        lblNameFltr = wx.StaticText(panel, wx.ID_ANY, 'Name:')
        lblNameFltr.SetFont(font)
        lblNameFltr.SetForegroundColour('white')
        nameFltr = wx.SearchCtrl(panel, wx.ID_ANY, '', style=wx.TE_PROCESS_ENTER, name='nameFltr')
        nameFltr.ShowCancelButton(True)
        nameFltr.Bind(wx.EVT_CHAR, self.onFltr)
        nameFltr.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, self.onFltrCancel)

        lblNotesFltr = wx.StaticText(panel, wx.ID_ANY, 'Notes')
        lblNotesFltr.SetFont(font)
        lblNotesFltr.SetForegroundColour('white')
        notesFltr = wx.SearchCtrl(panel, wx.ID_ANY, style=wx.TE_PROCESS_ENTER, name='notesFltr')
        notesFltr.ShowCancelButton(True)
        notesFltr.Bind(wx.EVT_CHAR, self.onFltr)
        notesFltr.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, self.onFltrCancel)

        layout.Add(addBtn, 0, wx.ALL, 5)
        layout.Add(dropBtn, 0, wx.ALL, 5)
        layout.Add(lblNameFltr, 0, wx.ALL, 5)
        layout.Add(nameFltr, 0, wx.ALL, 5)
        layout.Add(lblNotesFltr, 0, wx.ALL, 5)
        layout.Add(notesFltr, 0, wx.ALL, 5)

        hlpBtn = gbl.getHelpBtn(panel)
        hlpBtn.Bind(wx.EVT_BUTTON, gbl.showListHelp)
        layout.Add(hlpBtn, 0, wx.ALL, 5)

        panel.SetSizerAndFit(layout)

        return panel

    def buildListPanel(self, data):
        panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize)
        panel.SetBackgroundColour(gbl.LIST_BG_COLOR)
        layout = wx.BoxSizer(wx.HORIZONTAL)

        self.olv = ObjectListView(panel, wx.ID_ANY,
                                  size=wx.Size(-1, 550),
                                  style=wx.LC_REPORT | wx.SUNKEN_BORDER)

        font = self.olv.GetFont()
        nameWidth = getWidestTextExtent(font, [x['name'] for x in data])

        self.olv.SetColumns([
            ColumnDefn('Name', 'left', nameWidth, 'name'),
            ColumnDefn('Grade', 'right', 105, 'grade'),
            ColumnDefn('Step', 'right', 100, 'step'),
            ColumnDefn('FTE', 'right', 100, 'fte'),
            ColumnDefn('Notes', 'left', 0, 'notes'),
            ColumnDefn('Investigator', 'left', 0, 'investigator')
        ])

        self.olv.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.onDblClick)
        self.olv.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.onRightClick)

        self.olv.SetObjects(data)

        layout.Add(self.olv, 1, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(layout)

        return panel

    def onDblClick(self, event):
        emp = event.EventObject.GetSelectedObject()
        asns = Employee.getAsns(emp['id'])

        dlg = EmpDetailDlg(self, wx.ID_ANY, 'Employee Details', emp, asns)
        dlg.ShowModal()

    def onRightClick(self, event):
        emp = event.EventObject.GetSelectedObject()
        wx.MessageBox(emp['notes'], 'Notes', wx.OK | wx.ICON_INFORMATION)

    def onAddBtnClick(self, event):
        dlg = EmpDetailDlg(self, wx.ID_ANY, 'New Employee', None, None)
        dlg.ShowModal()

    def onDropBtnClick(self, event):
        ids = [x['id'] for x in self.olv.GetSelectedObjects()]
        if not ids:
            wx.MessageBox('No employees selected!', 'Oops!',
                          wx.OK | wx.ICON_ERROR)
            return
        dlg = wx.MessageDialog(self, 'Drop selected employees?', 'Just making sure',
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
