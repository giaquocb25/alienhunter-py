# import wx

# class MyFrame(wx.Frame):
#     def __init__(self, parent, title):
#         super(MyFrame, self).__init__(parent, title =title, size = (600,400))


#         self.panel = MyPanel(self)


# class MyPanel(wx.Panel):
#     def __init__(self, parent):
#         super(MyPanel, self).__init__(parent)


#         hbox = wx.BoxSizer(wx.HORIZONTAL)

#         self.listbox = wx.ListBox(self)
#         hbox.Add(self.listbox, wx.ID_ANY, wx.EXPAND | wx.ALL, 20)

#         btnPanel = wx.Panel(self)
#         vbox = wx.BoxSizer(wx.VERTICAL)
#         newBtn = wx.Button(btnPanel, wx.ID_ANY, 'Thêm', size=(90, 30))
#         renBtn = wx.Button(btnPanel, wx.ID_ANY, 'Sửa', size=(90, 30))
#         delBtn = wx.Button(btnPanel, wx.ID_ANY, 'Xóa', size=(90, 30))
#         clrBtn = wx.Button(btnPanel, wx.ID_ANY, 'Xóa Hết', size=(90, 30))

#         self.Bind(wx.EVT_BUTTON, self.NewItem, id=newBtn.GetId())
#         self.Bind(wx.EVT_BUTTON, self.OnRename, id=renBtn.GetId())
#         self.Bind(wx.EVT_BUTTON, self.OnDelete, id=delBtn.GetId())
#         self.Bind(wx.EVT_BUTTON, self.OnClear, id=clrBtn.GetId())
#         self.Bind(wx.EVT_LISTBOX_DCLICK, self.OnRename)

#         vbox.Add((-1, 20))
#         vbox.Add(newBtn)
#         vbox.Add(renBtn, 0, wx.TOP, 5)
#         vbox.Add(delBtn, 0, wx.TOP, 5)
#         vbox.Add(clrBtn, 0, wx.TOP, 5)

#         btnPanel.SetSizer(vbox)
#         hbox.Add(btnPanel, 0.6, wx.EXPAND | wx.RIGHT, 20)
#         self.SetSizer(hbox)


#         self.Centre()

#     def NewItem(self, event):

#         text = wx.GetTextFromUser('Nhập Giá Trị Mới', 'Bảng Nhập Giá Trị')
#         if text != '':
#             self.listbox.Append(text)

#     def OnRename(self, event):

#         sel = self.listbox.GetSelection()
#         text = self.listbox.GetString(sel)
#         renamed = wx.GetTextFromUser('Sửa Giá Trí', 'Bảng Sửa Giá Trị', text)

#         if renamed != '':
#             self.listbox.Delete(sel)
#             item_id = self.listbox.Insert(renamed, sel)
#             self.listbox.SetSelection(item_id)

    
#     def OnDelete(self, event):

#         sel = self.listbox.GetSelection()
#         if sel != -1:
#             self.listbox.Delete(sel)
#         else:
#             wx.MessageBox('Bạn chưa chọn giá trị', 'Warning',
#                                      wx.OK | wx.ICON_WARNING)

#     def OnClear(self, event):
#         self.listbox.Clear()

# class MyApp(wx.App):
#     def OnInit(self):
#         self.frame = MyFrame(parent=None, title="Demo 2")
#         self.frame.Show()
#         return True



# app = MyApp()
# app.MainLoop()