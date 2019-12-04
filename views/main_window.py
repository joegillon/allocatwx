import wx
import globals as gbl
from views.tab_panel import TabPanel
from views.projects.tab_def import PrjTabDef
from views.employees.tab_def import EmpTabDef
from views.efforts.eff_tab import EffTab


class MainWindow(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title='allocat', size=(1000, 700))
        panel = wx.Panel(self)
        layout = wx.BoxSizer()

        panel.SetBackgroundColour(gbl.COLOR_SCHEME.pnlBg)
        notebook = wx.Notebook(panel)

        notebook.AddPage(TabPanel(notebook, PrjTabDef()), 'Projects')
        notebook.AddPage(TabPanel(notebook, EmpTabDef()), 'Employees')
        notebook.AddPage(EffTab(notebook), 'Scoreboard')
        layout.Add(notebook, 0, wx.EXPAND, 5)

        panel.SetSizer(layout)
