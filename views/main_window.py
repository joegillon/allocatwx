import wx
import models.globals as gv
from views.projects.prj_tab import PrjTab
from views.employees.emp_tab import EmpTab
from views.efforts.eff_tab import EffTab
import models.globals as gbl


class MainWindow(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title='allocat', size=(1000, 700))
        panel = wx.Panel(self)
        layout = wx.BoxSizer()

        panel.SetBackgroundColour(gbl.COLOR_SCHEME.pnlBg)
        notebook = wx.Notebook(panel)
        notebook.AddPage(PrjTab(notebook), 'Projects')
        notebook.AddPage(EmpTab(notebook), 'Employees')
        notebook.AddPage(EffTab(notebook), 'Scoreboard')
        layout.Add(notebook, 0, wx.EXPAND, 5)

        panel.SetSizer(layout)
