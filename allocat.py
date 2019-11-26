import models.globals as gbl
from models.project import Project
from models.employee import Employee

if __name__ == '__main__':
    from wx import App
    from views.main_window import MainWindow

    app = App()

    gbl.prjRex = Project.get_all_active()
    gbl.empRex = Employee.get_all()

    empNames = {emp['id']: emp['name'] for emp in gbl.empRex.values()}
    for prj in gbl.prjRex.values():
        prj['PiName'] = empNames[prj['PI']] if prj['PI'] else ''
        prj['PmName'] = empNames[prj['PM']] if prj['PM'] else ''

    frm = MainWindow()
    frm.Show()

    app.MainLoop()
