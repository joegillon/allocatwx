if __name__ == '__main__':
    from wx import App
    from views.main_window import MainWindow
    import globals as gbl
    import lib.ui_lib as uil
    from dal.dao import Dao
    import dal.prj_dal as prj_dal
    import dal.emp_dal as emp_dal

    app = App()

    dao = Dao(stateful=True)
    gbl.prjRex = prj_dal.get_all_active(dao)
    gbl.empRex = emp_dal.get_all(dao)
    dao.close()

    # Add PI and PM names to prjRex
    empNames = {emp['id']: emp['name'] for emp in gbl.empRex.values()}
    for prj in gbl.prjRex.values():
        prj['PiName'] = empNames[prj['PI']] if prj['PI'] else ''
        prj['PmName'] = empNames[prj['PM']] if prj['PM'] else ''

    # These dicts are for checking for unique values. We can't trust
    # the DB to handle this since it is easily fooled by trivial changes
    # like extra spaces.
    gbl.prjNames = {uil.set2compare(p['name']):p['id']
                    for p in gbl.prjRex.values()}
    gbl.prjNicknames = {uil.set2compare(p['nickname']): p['id']
                        for p in gbl.prjRex.values()}

    gbl.empNames = {uil.set2compare(e['name']): e['id']
                    for e in gbl.empRex.values()}

    frm = MainWindow()
    frm.Show()

    app.MainLoop()
