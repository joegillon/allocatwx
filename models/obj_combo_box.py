import wx


class ObjComboBox(wx.ComboBox):
    def __init__(self, parent, choices, display_fld, style=None):
        wx.ComboBox.__init__(self, parent, wx.ID_ANY, style=style)

        isDict = isinstance(choices[0], dict)
        for choice in choices:
            show = choice[display_fld] if isDict else getattr(choice, display_fld)
            self.Append(show, choice)

    def getSelectionId(self):
        if self.CurrentSelection == -1:
            return None
        return self.GetClientData(self.GetSelection())['id']
