def build_globals():
    import globals as gbl
    import lib.ui_lib as uil
    from dal.dao import Dao
    import dal.prj_dal as prj_dal
    import dal.emp_dal as emp_dal

    dao = Dao(stateful=True)
    gbl.prjRex = prj_dal.get_all_active(dao)
    gbl.empRex = emp_dal.get_all(dao)
    dao.close()

    # Add PI and PM names to prjRex
    # Build prj name and nickname comparison dicts
    empNames = {emp['id']: emp['name'] for emp in gbl.empRex.values()}
    for prj in gbl.prjRex.values():
        prj['PiName'] = empNames[prj['PI']] if prj['PI'] else ''
        prj['PmName'] = empNames[prj['PM']] if prj['PM'] else ''
        gbl.prjNames[uil.set2compare(prj['name'])] = prj['id']
        gbl.prjNicknames[uil.set2compare(prj['nickname'])] = prj['id']
        w = dc.GetTextExtent(prj['name'])[0]
        if dc.GetTextExtent(prj['name'])[0] > gbl.widestPrjName:
            gbl.widestPrjName = w
        w = dc.GetTextExtent(prj['nickname'])[0]
        if w > gbl.widestNickname:
            gbl.widestNickname = w

    gbl.empNames = {uil.set2compare(e['name']): e['id']
                    for e in gbl.empRex.values()}
    gbl.widestEmpName = uil.getWidestTextExtent(font, empNames.values())


if __name__ == '__main__':
    import wx
    from views.main_window import MainWindow

    app = wx.App()

    # Set the font for the widest text calculations
    font = wx.Font(9,
                   wx.FONTFAMILY_DEFAULT,
                   wx.FONTSTYLE_NORMAL,
                   wx.FONTWEIGHT_NORMAL)
    dc = wx.ScreenDC()
    dc.SetFont(font)

    build_globals()

    frm = MainWindow()
    frm.Show()

    app.MainLoop()
