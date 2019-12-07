import wx
import globals as gbl
from views.projects.tab_panel import PrjTabPanel
from views.employees.tab_panel import EmpTabPanel
from views.efforts.eff_tab import EffTab


class MainWindow(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title='allocat', size=(1000, 700))
        panel = wx.Panel(self)
        layout = wx.BoxSizer()

        panel.SetBackgroundColour(gbl.COLOR_SCHEME.pnlBg)
        notebook = wx.Notebook(panel)

        notebook.AddPage(PrjTabPanel(notebook), 'Projects')
        notebook.AddPage(EmpTabPanel(notebook), 'Employees')
        notebook.AddPage(EffTab(notebook), 'Scoreboard')
        layout.Add(notebook, 0, wx.EXPAND, 5)

        panel.SetSizer(layout)
