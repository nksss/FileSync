from tkinter import *
import os
import shutil

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.routeEntry1 = Entry(self)
        self.routeEntry1.grid(row=1,column=1,padx=10,pady=10)  #测试

        self.routeEntry2 = Entry(self)
        self.routeEntry2.grid(row=1,column=3,padx=10,pady=10)

        self.routeList1 = Listbox(self, listvariable=None)
        self.routeList1.bind('<Double-Button-1>', self.freshListBox1)
        self.routeList1.grid(row=2,column=1,padx=10,pady=10)

        self.routeList2 = Listbox(self, listvariable=None)
        self.routeList2.bind('<Double-Button-1>', self.freshListBox2)
        self.routeList2.grid(row=2,column=3,padx=10,pady=10)

        self.routeConfirm1 = Button(self, text='Quit', command=self.printRoute1)
        self.routeConfirm1.grid(row=1,column=2,padx=10,pady=10)

        self.routeConfirm2 = Button(self, text='Quit', command=self.printRoute2)
        self.routeConfirm2.grid(row=1,column=4,padx=10,pady=10)

        # self.buttonPanel = PanedWindow()
        
        # self.buttonPanel.add(self.syncButton)

        self.panel = PanedWindow(self)
        self.panel.grid(row=2,column=2,padx=10,pady=10)

        syncButton = Button(self.panel, text='Sync', command=self.syncFolder)
        syncButton.pack()
        # syncButton.grid(row=1,column=1)
        leftSyncButton = Button(self.panel, text='<<', command=self.right2left)
        leftSyncButton.pack()
        # leftSyncButton.grid(row=2,column=1)
        rightSyncButton = Button(self.panel, text='>>', command=self.left2right)
        rightSyncButton.pack()
        # rightSyncButton.grid(row=3,column=1)
        self.panel.add(syncButton)
        self.panel.add(leftSyncButton)
        self.panel.add(rightSyncButton)

    def printRoute1(self):
        files = os.listdir(self.routeEntry1.get())
        index = 0
        for file in files:
            if os.path.isfile(os.path.join(self.routeEntry1.get(), file)):
                self.routeList1.insert(index, file + ' ' + str(os.path.getsize(os.path.join(self.routeEntry1.get(), file))))
            else:
                self.routeList1.insert(index, file)
            index+=1

    def printRoute2(self):
        files = os.listdir(self.routeEntry2.get())
        index = 0
        for file in files:
            self.routeList2.insert(index, file)
            index+=1

    def freshListBox1(self, event):
        route = self.routeList1.get(self.routeList1.curselection())
        self.routeList1.delete(0, END)
        tmp = self.routeEntry1.get()
        path = os.path.join(tmp, route)
        self.routeEntry1.delete(0, END)
        self.routeEntry1.insert(0, path)
        files = os.listdir(path)
        index = 0
        for file in files:
            if os.path.isfile(os.path.join(path, file)):
                self.routeList1.insert(index, file + ' ' + str(os.path.getsize(os.path.join(path, file))))
            else:
                self.routeList1.insert(index, file)
            index+=1

    def freshListBox2(self, event):
        route = self.routeList2.get(self.routeList2.curselection())
        self.routeList2.delete(0, END)
        tmp = self.routeEntry2.get()
        path = os.path.join(tmp, route)
        self.routeEntry2.delete(0, END)
        self.routeEntry2.insert(0, path)
        files = os.listdir(path)
        index = 0
        for file in files:
            if os.path.isfile(os.path.join(path, file)):
                self.routeList2.insert(index, file + ' ' + str(os.path.getsize(os.path.join(path, file))))
            else:
                self.routeList2.insert(index, file)
            index+=1

    def syncFolder(self):
        leftList = self.routeList1.get(0, END)
        rightList = self.routeList2.get(0, END)
        self.routeList1.delete(0, END)
        self.routeList2.delete(0, END)
        tmpList = set([])
        for left in leftList:
            tmpList.add(left)

        for right in rightList:
            tmpList.add(right)
        index = 0
        for tmp in tmpList:
            for left in leftList:
                if left == tmp:
                    self.routeList1.insert(index, left)
                    break
                else:
                    self.routeList1.insert(index, '')
            index+=1
        index = 0
        for tmp in tmpList:
            for right in rightList:
                if right == tmp:
                    self.routeList2.insert(index, right)
                    break
                else:
                    self.routeList2.insert(index, '')
            index+=1

        self.routeList1.bind('<MouseWheel>', self.mw1)
        self.routeList2.bind('<MouseWheel>', self.mw2)

    def mw1(self, e):
        long = e.delta//120
        if long == -1:
            self.routeList2.yview_scroll(-1*long,'units')
        else:
            self.routeList2.yview_scroll(-1,'units')

    def mw2(self, e):
        long = e.delta//120
        if long == -1:
            self.routeList1.yview_scroll(-1*long,'units')
        else:
            self.routeList1.yview_scroll(-1,'units')

    def left2right(self):
        src = str(os.path.join(self.routeEntry1.get(), self.routeList1.get(self.routeList1.curselection()))).split(' ')
        dst = str(os.path.join(self.routeEntry2.get(), self.routeList1.get(self.routeList1.curselection()))).split(' ')
        shutil.copyfile(src[0], dst[0])

    def right2left(self):
        src = str(os.path.join(self.routeEntry2.get(), self.routeList2.get(self.routeList2.curselection()))).split(' ')
        dst = str(os.path.join(self.routeEntry1.get(), self.routeList2.get(self.routeList2.curselection()))).split(' ')
        shutil.copyfile(src[0], dst[0])
        
            
app = Application()

app.master.title('sync')
app.master.geometry('800x500')

app.mainloop()