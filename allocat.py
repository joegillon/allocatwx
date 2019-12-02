if __name__ == '__main__':
    from wx import App
    from views.main_window import MainWindow
    import models.globals as gbl
    from models.dao import Dao
    from models.project import Project
    from models.employee import Employee
    from utils.strutils import set2compare

    app = App()

    dao = Dao(stateful=True)
    gbl.prjRex = Project.get_all_active(dao)
    gbl.empRex = Employee.get_all(dao)
    dao.close()

    # These dicts are for checking for unique values. We can't trust
    # the DB to handle this since it is easily fooled by trivial changes
    # like extra spaces.
    gbl.prjNames = {set2compare(p['name']):p['id']
                    for p in gbl.prjRex.values()}
    gbl.prjNicknames = {set2compare(p['nickname']): p['id']
                        for p in gbl.prjRex.values()}

    empNames = {emp['id']: emp['name'] for emp in gbl.empRex.values()}
    for prj in gbl.prjRex.values():
        prj['PiName'] = empNames[prj['PI']] if prj['PI'] else ''
        prj['PmName'] = empNames[prj['PM']] if prj['PM'] else ''

    gbl.empNames = {set2compare(e['name']): e['id']
                    for e in gbl.empRex.values()}

    frm = MainWindow()
    frm.Show()

    app.MainLoop()
