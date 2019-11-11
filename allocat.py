import models.globals as gv
from models.project import Project
from models.employee import Employee

if __name__ == '__main__':
    from wx import App
    from views.main_window import MainWindow

    app = App()

    gv.prjRex = Project.get_all()
    gv.empRex = Employee.get_all()

    frm = MainWindow()
    frm.Show()

    app.MainLoop()
