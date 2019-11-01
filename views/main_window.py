import wx
from views.projects.prj_tab import PrjTab
from views.employees.emp_tab import EmpTab
from views.efforts.eff_tab import EffTab


class MainWindow(wx.Frame):
    def __init__(self, prjs, emps, asns):
        wx.Frame.__init__(self, None, title='allocat', size=(1000, 700))

        p = wx.Panel(self)
        nb = wx.Notebook(p)

        nb.AddPage(PrjTab(nb, prjs), 'Projects')
        nb.AddPage(EmpTab(nb), 'Employees')
        nb.AddPage(EffTab(nb), 'Scoreboard')

        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        p.SetSizer(sizer)
