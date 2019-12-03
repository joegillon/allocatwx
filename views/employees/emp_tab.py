import wx
import ObjectListView as olv
import globals as gbl
import lib.ui_lib as uil
from dal.dao import Dao
import dal.emp_dal as emp_dal
from views.employees.detail_dlg import EmpDetailDlg


class EmpTab(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(gbl.COLOR_SCHEME.pnlBg)
        layout = wx.BoxSizer(wx.VERTICAL)

        # Need properties for the filters
        self.theList = None
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
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.tbBg)
        layout = wx.BoxSizer(wx.HORIZONTAL)

        addBtn = uil.toolbar_button(panel, 'Add Employee')
        addBtn.Bind(wx.EVT_BUTTON, self.onAddBtnClick)
        layout.Add(addBtn, 0, wx.ALL, 5)

        dropBtn = uil.toolbar_button(panel, 'Drop Employees')
        dropBtn.Bind(wx.EVT_BUTTON, self.onDropBtnClick)
        layout.Add(dropBtn, 0, wx.ALL, 5)

        lblNameFltr = uil.getToolbarLabel(panel, 'Name:')
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

        lblInvestigators = uil.getToolbarLabel(panel, 'Investigators:')
        layout.Add(lblInvestigators, 0, wx.ALL, 5)

        chkInvestigators = wx.CheckBox(panel, wx.ID_ANY)
        chkInvestigators.Bind(wx.EVT_CHECKBOX, self.onInvestigatorToggle)
        layout.Add(chkInvestigators, 0, wx.ALL, 5)

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
        gbl.EMP_NAME_WIDTH = \
            uil.getWidestTextExtent(font, [x['name'] for x in data.values()])

        self.theList.SetColumns([
            olv.ColumnDefn('Name', 'left', gbl.EMP_NAME_WIDTH, 'name'),
            olv.ColumnDefn('Grade', 'right', 105, 'grade'),
            olv.ColumnDefn('Step', 'right', 100, 'step'),
            olv.ColumnDefn('FTE', 'right', 100, 'fte'),
            olv.ColumnDefn('Notes', 'left', 0, 'notes'),
            olv.ColumnDefn('Investigator', 'right', 120, 'investigator',
                           stringConverter=uil.toYN)
        ])

        self.theList.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.onDblClick)
        self.theList.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.onRightClick)

        self.theList.SetBackgroundColour(gbl.COLOR_SCHEME.lstHdr)

        self.theList.SetObjects(list(data.values()))

        layout.Add(self.theList, 1, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(layout)

        return panel

    def onDblClick(self, event):
        emp = event.EventObject.GetSelectedObject()
        asns = emp_dal.getAsns(Dao(), emp['id'])

        dlg = EmpDetailDlg(self, wx.ID_ANY, 'Employee Details', emp['id'], asns)
        dlg.ShowModal()

    def onRightClick(self, event):
        emp = event.EventObject.GetSelectedObject()
        wx.MessageBox(emp['notes'], 'Notes', wx.OK | wx.ICON_INFORMATION)

    def onAddBtnClick(self, event):
        dlg = EmpDetailDlg(self, wx.ID_ANY, 'New Employee', None, None)
        dlg.ShowModal()

    def onDropBtnClick(self, event):
        ids = [x['id'] for x in self.theList.GetSelectedObjects()]
        if not ids:
            wx.MessageBox('No employees selected!', 'Oops!',
                          wx.OK | wx.ICON_ERROR)
            return
        dlg = wx.MessageDialog(self, 'Drop selected employees?', 'Just making sure',
                               wx.YES_NO | wx.ICON_QUESTION)
        reply = dlg.ShowModal()
        if reply == wx.ID_YES:
            result = emp_dal.delete(Dao(), ids)
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
            col = self.theList.columns[4:5]
        self.theList.SetFilter(olv.Filter.TextSearch(
            self.theList, columns=col, text=self.srchValue))
        self.theList.RepopulateList()
        event.Skip()

    def onFltrCancel(self, event):
        event.EventObject.Clear()
        self.theList.SetFilter(None)
        self.theList.RepopulateList()
        self.srchValue = ''

    def onInvestigatorToggle(self, event):
        if event.Selection == 0:
            self.theList.SetFilter(None)
        else:
            self.theList.SetFilter(olv.Filter.TextSearch(
                self.theList, columns=self.theList.columns[5:], text='Y'))
        self.theList.RepopulateList()
