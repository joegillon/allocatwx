import models.globals as gv
from models.project import Project
from models.employee import Employee

if __name__ == '__main__':
    from wx import App
    from views.main_window import MainWindow

    app = App()

    gv.prjRex = Project.get_all_active()
    gv.empRex = Employee.get_all()

    empNames = {emp['id']: emp['name'] for emp in gv.empRex}
    for prj in gv.prjRex:
        prj['PiName'] = empNames[prj['PI']] if prj['PI'] else ''
        prj['PmName'] = empNames[prj['PM']] if prj['PM'] else ''

    frm = MainWindow()
    frm.Show()

    app.MainLoop()
