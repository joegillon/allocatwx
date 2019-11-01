from models.project import Project

if __name__ == '__main__':
    from wx import App
    from views.main_window import MainWindow

    app = App()

    frm = MainWindow(Project.get_all(), [], [])
    frm.Show()
    app.MainLoop()
