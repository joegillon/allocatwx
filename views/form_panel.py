import wx
import globals as gbl
import lib.ui_lib as uil
from dal.dao import Dao


class FormPanel(wx.Panel):
    def __init__(self, parent, ownerRec):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(gbl.COLOR_SCHEME.pnlBg)
        layout = wx.BoxSizer(wx.VERTICAL)

        self.ownerName = None
        self.ownerRec = ownerRec
        self.formData = {}
        self.dal = None
        self.rex = None

        self.setProps()

        tbPanel = self.buildToolbarPanel()
        frmPanel = self.buildFormPanel()

        layout.Add(tbPanel, 0, wx.ALL | wx.EXPAND, 5)
        layout.Add(frmPanel, 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(layout)

        frmPanel.SetFocus()

    def setProps(self):
        raise NotImplementedError("Please Implement this method")

    def buildToolbarPanel(self):
        panel = wx.Panel(
            self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize
        )
        panel.SetBackgroundColour(wx.Colour(gbl.COLOR_SCHEME.tbBg))
        layout = wx.BoxSizer(wx.HORIZONTAL)

        dropBtn = uil.toolbar_button(panel, 'Drop ' + self.ownerName)
        dropBtn.Bind(wx.EVT_BUTTON, self.onDropClick)

        saveBtn = uil.toolbar_button(panel, 'Save ' + self.ownerName)
        saveBtn.Bind(wx.EVT_BUTTON, self.onSaveClick)

        layout.Add(dropBtn, 0, wx.ALL, 5)
        layout.Add(saveBtn, 0, wx.ALL, 5)

        panel.SetSizer(layout)

        return panel

    def buildFormPanel(self):
        panel = wx.Panel(
            self, wx.ID_ANY, wx.DefaultPosition, size=(-1, 375)
        )
        panel.SetBackgroundColour(wx.Colour(gbl.COLOR_SCHEME.frmBg))
        panel.SetForegroundColour('black')

        layout = self.getLayout(panel, self.ownerRec)

        panel.SetSizer(layout)
        return panel

    def getLayout(self, panel, ownerRec):
        raise NotImplementedError("Please Implement this method")

    def onDropClick(self, event):
        dlg = wx.MessageDialog(self, 'Drop ' + self.ownerName + '?',
                               'Just making sure',
                               wx.YES_NO | wx.ICON_QUESTION)
        reply = dlg.ShowModal()
        if reply == wx.ID_YES:
            if self.dropRec():
                self.Parent.Close()

    def onSaveClick(self, event):
        self.getFormData()

        if self.validate(self.ownerRec):
            if self.ownerRec is None:
                if self.addRec():
                    # self.Parent.dtlPanel.activateAddBtn()
                     pass
            else:
                self.updateRec()

    def getFormData(self):
        raise NotImplementedError("Please Implement this method")

    def validate(self, ownerRec):
        raise NotImplementedError("Please Implement this method")

    def addRec(self):
        try:
            rec_id = self.dal.add(Dao(), self.formData)
        except Exception as ex:
            wx.MessageBox('Error adding %s: %s' % (self.ownerName, str(ex)))
            return False
        self.ownerRec = self.formData.copy()
        self.ownerRec['id'] = rec_id
        self.supplementRec()
        self.ownerRec['active'] = 1
        self.updateMyRex()
        wx.MessageBox('%s added!' % self.ownerName)
        return True

    def updateRec(self):
        try:
            result = self.dal.update(Dao(), self.ownerRec, self.formData)
        except Exception as ex:
            wx.MessageBox('Error updating %s: %s' % (self.ownerName, str(ex)))
            return
        if result != 1:
            wx.MessageBox('Unanticipated error updating %s' % self.ownerName)
            return
        for fld, value in self.formData.items():
            self.ownerRec[fld] = value
        self.supplementRec()
        self.updateMyRex()
        wx.MessageBox('%s updated!' % self.ownerName)

    def supplementRec(self):
        raise NotImplementedError("Please Implement this method")

    def updateMyRex(self):
        self.rex[self.ownerRec['id']] = self.ownerRec
        self.GrandParent.loadList(self.rex.values())

    def dropRec(self):
        try:
            result = self.dal.delete(Dao(), [self.ownerRec['id']])
        except Exception as ex:
            wx.MessageBox('Error dropping %s: %s' % (self.ownerName, str(ex)))
            return False
        if result != 1:
            wx.MessageBox('Unanticipated error dropping %s' % self.ownerName)
            return False
        del self.rex[self.ownerRec['id']]
        self.GrandParent.loadList(self.rex.values())
        wx.MessageBox('%s dropped!' % self.ownerName)
        return True
