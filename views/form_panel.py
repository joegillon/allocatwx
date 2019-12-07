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
            result = self.dal.delete(Dao(), [self.ownerRec['id']])
            print(result)

    def onSaveClick(self, event):
        self.getFormData()

        if self.validate(self.ownerRec):
            if self.ownerRec is None:
                result = self.dal.add(Dao(), self.formData)
                print(result)
            else:
                result = self.dal.update(Dao(), self.ownerRec['id'], self.formData)
                print(result)
            self.Parent.dtlPanel.activateAddBtn()
            self.Parent.Close()

    def getFormData(self):
        raise NotImplementedError("Please Implement this method")

    def validate(self, ownerRec):
        raise NotImplementedError("Please Implement this method")