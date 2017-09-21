#!/usr/bin/python
# -*- coding: utf-8 -*-

currentversion = "3.0.3"

import tkinter as tk
from tkinter import ttk
import webbrowser
import datetime
import urllib.request
from easygui_mod import multenterbox
import os
import sys
from os import name, path, remove, rename, makedirs
import tkinter.messagebox as mb
import _thread
from time import strftime, localtime
from tkinter import filedialog
import urllib.request
import zipfile

class Root(ttk.Frame):    
    def __init__(self):
        tk.Frame.__init__(self)
        self.master.withdraw()        
        
        # Initializing data
        self.student=[]
        if not path.exists("data.ini"): # if absent, create blank
            with open("data.ini", "w", encoding="utf-8") as file:
                file.write("\n\n\n\n\n\n\n\n\n\n\n\n\n\n \n" + currentversion + "\n30\ns-89-u-4up\nда\n9\n0\n-\nhttps://www.jw.org/ru/публикации/свидетелей-иеговы-встреча-рабочая-тетрадь/\nда\n")        
        try:
            with open("data.ini", "r", encoding="utf-8") as file:
                self.datastring = [line.rstrip() for line in file]
                self.datafile_len = len(self.datastring)
        except:
            with open("data.ini", "r") as file:
                self.datastring = [line.rstrip() for line in file]
                self.datafile_len = len(self.datastring)
        
        # Rewriting data file with the current program version        
        with open("data.ini", "w", encoding="utf-8") as datafile:
            self.datastring[15] = currentversion
            for i in range(self.datafile_len): datafile.write(self.datastring[i] + "\n")
        
        # Load images        
        self.img=[]
        self.img.append(tk.PhotoImage(file="arrow.gif"))                        # 0
        self.img.append(tk.PhotoImage(file="pdf.gif"))                          # 1
        self.img.append(tk.PhotoImage(file="mwb.gif"))                          # 2
        self.img.append(tk.PhotoImage(file="settings.gif"))                     # 3
        self.img.append(tk.PhotoImage(file="add_user.gif"))                     # 4
        self.img.append(tk.PhotoImage(file="icon.png"))                         # 5
        
        # Window set up
        self.geo=[]
        self.winSizeX=640
        self.winSizeY=480
        self.master.bind("<Configure>", self.getWinSize)
        try:
            with open("win.ini") as f: file=f.readlines()
            self.geo.append(int(file[0])) # w
            self.geo.append(int(file[1])) # h 
            self.geo.append(int(file[2])) # x
            self.geo.append(int(file[3])) # y
        except:
            ws = self.master.winfo_screenwidth()
            hs = self.master.winfo_screenheight()
            self.geo.append(self.winSizeX)
            self.geo.append(self.winSizeY)
            self.geo.append(int((ws/2) - (self.geo[0]/2)))
            self.geo.append(int((hs/2) - (self.geo[1]/2)))
            if self.master.winfo_screenwidth()<self.winSizeX or self.master.winfo_screenheight()<self.winSizeY:
                self.master.wm_state('zoomed')
        self.master.geometry('%dx%d+%d+%d' % (self.geo[0], self.geo[1]+20, self.geo[2], self.geo[3]))                
        self.master.minsize(100,200)        
        self.master.protocol("WM_DELETE_WINDOW", self.fullQuit)
        if name=="nt":
            self.master.iconbitmap("icon.ico")
        else:
            self.tk.call('wm', 'iconphoto', self.master._w, self.img[5])        
        self.master.title("Students")        
        self.master.columnconfigure(0, weight=1)        
        self.master.rowconfigure(0, weight=1)
        self.master.rowconfigure(1, weight=0)
        self.master.rowconfigure(2, weight=0)
        self.padx=self.pady=5        
        
        # Settings
        self.menubar = tk.Menu(self.master)
        self.menuFile = tk.Menu(self.menubar, tearoff=0)                       
        self.menubar.add_cascade(label="Файл", menu=self.menuFile)
        self.menuFile.add_command(label="Импорт", command=self.imp) 
        #self.menuFile.add_command(label="Экспорт", command=self.exp)
        self.menuFile.add_command(label="Очистка", command=self.wipe)
        self.menuFile.add_separator()
        self.menuFile.add_command(label="Выход", command=self.fullQuit)        
        self.menuSettings = tk.Menu(self.menubar, tearoff=0)                       
        #self.menubar.add_cascade(label="Настройки", command=self.settings)        
        self.menuHelp = tk.Menu(self.menubar, tearoff=0)                       
        self.menubar.add_cascade(label="Помощь", menu=self.menuHelp)
        self.menuHelp.add_command(label="Справка", command=self.readme)
        self.menuHelp.add_command(label="Сайт", command=self.site)        
        self.master.config(menu=self.menubar)
        
        # Main frame        
        self.mainframe=tk.Frame(self.master) 
        self.mainframe.grid(column=0, row=0, sticky="wnse")        
        self.headers=["Имя", "Выступление", "Помощь", "Урок", ""]
        
        # Students list
        self.style = ttk.Style()
        self.list=ttk.Treeview(self.mainframe, columns=self.headers, show="headings")        
        self.list.pack(fill="both", expand=True)
        self.rightScrollbar = ttk.Scrollbar(self.list, orient="vertical", command=self.list.yview) 
        self.list.configure(yscrollcommand=self.rightScrollbar.set) 
        self.rightScrollbar.pack(side="right", fill="y")
        
        # List actions
        self.list.bind("<<TreeviewSelect>>", self.select)
        self.list.bind("<Return>", self.open) 
        self.list.bind("<Double-1>", self.open)
        self.list.bind("<3>", lambda event: self.listmenu.post(event.x_root, event.y_root)) 
        self.list.bind("<Delete>", self.delete)
        self.list.bind("<BackSpace>", self.delete)
        
        # List context menu
        self.listbar = tk.Menu(self.list)                                       
        self.listmenu = tk.Menu(self.listbar, tearoff=0)
        self.listmenu.add_command(label="Открыть", command=self.open)
        self.listmenu.add_command(label="Удалить", command=self.delete)        
        
        # Bottom action frame
        self.actionFrame=tk.Frame(self.master)
        self.actionFrame.columnconfigure(2, weight=1)
        self.actionFrame.rowconfigure(2, weight=1)
        self.actionFrame.grid(column=0, row=1, padx=self.padx, pady=self.pady, sticky="nesw")
        self.ipadxy=3
        
        # Buttons
        self.style.configure("new.TButton", justify="center")        
        ttk.Button(self.actionFrame, style='new.TButton', text="Новый", image=self.img[4], compound="left", command=self.new).grid(column=0, row=0, padx=self.padx, ipadx=self.ipadxy, ipady=self.ipadxy, sticky="we")
        ttk.Button(self.actionFrame, style='new.TButton', text="PDF", image=self.img[1], command=self.pdf, compound="left").grid(column=1, row=0, padx=self.padx, ipadx=self.ipadxy, ipady=self.ipadxy, sticky="we")
        ttk.Button(self.actionFrame, style='new.TButton', text="НХЖС", image=self.img[2], compound="left", command=self.mwb).grid(column=0, row=1, padx=self.padx, ipadx=self.ipadxy, ipady=self.ipadxy, sticky="we")
        ttk.Button(self.actionFrame, style='new.TButton', text="Настройки", image=self.img[3], compound="left", command=self.settings).grid(column=1, row=1, padx=self.padx, ipadx=self.ipadxy, ipady=self.ipadxy, sticky="we")
        
        # Note
        self.statNote=ttk.LabelFrame(self.actionFrame, text="Заметка")
        self.statNote.grid(column=2, row=0, rowspan=2, padx=self.padx, pady=self.pady, sticky="ns")
        self.note=tk.Message(self.statNote, width=180)
        self.note.pack(anchor="nw", padx=self.padx, pady=self.pady)
        
        # Stats
        self.statFrame=ttk.LabelFrame(self.actionFrame, text="Статистика")
        self.statFrame.grid(column=3, row=0, rowspan=2, padx=self.padx, pady=self.pady, sticky="nse")
        self.stats=ttk.Label(self.statFrame)
        self.stats.grid(column=0, row=0, padx=self.padx, pady=self.pady, sticky="wn")
        self.stats["text"]="Всего учащихся:\nНикогда не выступали:   \nНикогда не помогали:\nБез урока:" 
        self.stats2=ttk.Label(self.statFrame, style='stats.TLabel')
        self.stats2.grid(column=1, row=0, padx=self.padx, pady=self.pady, sticky="en")        
        
        # Footer
        #self.statusFrame=tk.Frame(self.master)
        #self.statusFrame.grid(column=0, row=2, padx=self.padx, pady=self.pady, sticky="nesw")
        self.statusBar=tk.Label(self.master, fg="gray40", font="(), 8")
        self.statusBar.grid(column=0, row=2, sticky="es")        
        ttk.Separator(self.master, orient='horizontal').grid (column=0, row=1, sticky='swe')
        ttk.Sizegrip(self.master).grid(column=0, row=2, sticky="se")       
        
        # Run
        self.deleteObsolete()
        self.load()
        self.sortList=tk.IntVar()           
        self.resizeList()
        self.draw()
        self.setFont(9)
        self.sortList.set(int(self.datastring[20]))
        self.sort(self.headers[self.sortList.get()])        
        self.getWinSize()
        self.updateCheck()        
        self.master.deiconify()
        
    def draw(self):
        """Update list and all stats"""        

        if self.sortList.get()==0: # by name
            self.student = sorted(self.student, key=lambda s: s[0])
        elif self.sortList.get()==1: # by date1
            self.student = sorted(self.student, key=lambda s: s[7])
        elif self.sortList.get()==2: # by date2
            self.student = sorted(self.student, key=lambda s: s[8])
        elif self.sortList.get()==3: # by study
            self.student = sorted(self.student, key=lambda s: self.getNumerical(s[3]))
        elif self.sortList.get()==4: # by note
            self.student = sorted(self.student, key=lambda s: s[4])    
        
        #self.student[0][0]= "☻☺" + self.student[0][0]
        self.list.delete(*self.list.get_children())        
        self.values=tuple(self.student)
        for col in self.headers: self.list.heading(col, text=col.title(), command=lambda c=col: self.sort(c))
        for item in self.values: self.list.insert('', 'end', values=item)
            
        # Count statistics
        noStudy=0
        noDate1=0
        noDate2=0
        for student in self.student:
            if student[1]=="00.00.00": noDate1+=1
            if student[2]=="00.00.00": noDate2+=1
            if student[3]=="": noStudy+=1
        self.stats2["text"]="%s\n%s\n%s\n%s" % (len(self.student),noDate1,noDate2,noStudy)
        
        # Show note
        self.note["text"]=self.datastring[14]
        
        # Show change time
        try:
            self.statusBar["text"] = "Последнее изменение: %s     " % datetime.datetime.fromtimestamp(os.path.getmtime("students.txt")) # last core save            
        except: pass
        
    def resizeList(self):
        """Resize columns"""
        self.list.column(0, width=130)
        self.list.column(1, width=80)
        self.list.column(2, width=80)
        self.list.column(3, width=20)
        self.list.column(4, width=80)
        
    def getWinSize(self, event=None, save=None):
        """Manage window geometry saving"""
        
        ws=self.master.winfo_width()
        hs=self.master.winfo_height()
        x=self.master.winfo_x()
        y=self.master.winfo_y()
        if save==True and (ws!=self.geo[0] or hs!=self.geo[1] or x!=self.geo[2] or y!=self.geo[3]):
            with open("win.ini", "w") as f: f.write("%d\n%d\n%d\n%d" % (ws, hs, x, y))        
            self.geo[0]=ws
            self.geo[1]=hs
            self.geo[2]=x
            self.geo[3]=y
            
    def fullQuit(self, event=None):
        """Quit process"""
        self.getWinSize(save=True)
        self.master.destroy()
        self.master.quit()
        
    def sort(self, col):
        """sort tree contents when a column header is clicked on"""
        if col!="":
            for n in range(4): self.list.heading(n, image="")
        for n in range(4):
            if col==self.headers[n]:
                self.sortList.set(n)
                self.list.heading(n, image=self.img[0])
                self.datastring[20]=str(n)                
        self.draw()        
        self.saveSettings()
        
    def select(self, event=None):
        """Select student from list"""
        selected=self.list.item(self.list.focus())["values"]
        self.master.clipboard_clear()
        self.master.clipboard_append(str(selected[0]))
        self.tip(str(selected[0]) + " в буфере обмена", 1000)
        for i in range(len(self.student)):
            if self.student[i][0]==str(selected[0]):
                #print(i)
                pass
                
    def open(self, event=None):
        """Open student card"""
        selected=self.list.item(self.list.focus())["values"]
        for editedstudent in range(len(self.student)):
            try:
                if str(self.student[editedstudent][0])==str(selected[0]):
                    fields = []
                    fieldNames = ["Имя (обязательно)","Последнее выступление","Последняя помощь","Урок","Примечание","Совет","Все пройденные уроки"]
                    fields = multenterbox("Отредактируйте данные:", str(selected[0]) + " – Обновление данных учащегося", fieldNames, [self.student[editedstudent][0], self.student[editedstudent][1], self.student[editedstudent][2], self.student[editedstudent][3], self.student[editedstudent][4], self.student[editedstudent][5], self.student[editedstudent][6]], neutralButton=True)
                    if fields == None: return
                    
                    # Check name and date
                    editstudent=False
                    while editstudent==False:
                        if fields[0].strip() == "":
                            fields = multenterbox("Необходимо ввести имя!", str(selected[0]) + " – Обновление данных учащегося", fieldNames, fields, neutralButton=True)                        
                            if fields==None: break
                        else:
                            editstudent = True
                    
                        if self.checkDate(fields[1])==False or self.checkDate(fields[2])==False:
                            editstudent = False
                            fields = multenterbox("Проверьте даты!", str(selected[0]) + " – Обновление данных учащегося", fieldNames, fields, neutralButton=True)     
                            if fields==None: break
                        else:                        
                            editstudent = True
                        
                    if editstudent == True:
                        for i in range(7):
                            self.student[editedstudent][i] = fields[i]
                        self.student[editedstudent][7] = [
                            fields[1][6], fields[1][7], fields[1][3], fields[1][4], fields[1][0], fields[1][1]
                            ]                                                
                        self.student[editedstudent][8] = [
                            fields[2][6], fields[2][7], fields[2][3], fields[2][4], fields[2][0], fields[2][1]
                            ]                        
                        for i in range(len(self.student)):
                                if(self.student[i][3]) != "":
                                    try: self.student[i].append(int(self.student[i][3]))
                                    except: self.student[i].append(0)
                                else:
                                    self.student[i].append(0)                                
                        self.save()
                        self.draw()
                        return
            except: return
                            
    def new(self, event=None):
        """Create new student"""        
        fieldNames = ["Имя (обязательно)","Последнее выступление","Последняя помощь","Номер урока","Примечание","Совет","Все пройденные уроки"]
        fields = []
        fields = multenterbox("Введите данные:", "Новый учащийся", fieldNames, ["", "00.00.00", "00.00.00", "", "", "", ""], neutralButton=True)        
        if fields==None: return
        
        if len(fields[1])=="" or len(fields[1])=="0" or self.checkDate(fields[1])==False:
            fields[1] = "00.00.00"

        if len(fields[2])=="" or len(fields[1])=="0" or self.checkDate(fields[2])==False:
            fields[2] = "00.00.00"

        # Check name and date
        newstudent=False
        while newstudent==False:
            if fields[0].strip() == "":
                fields = multenterbox("Необходимо ввести имя!", "Новый учащийся", fieldNames, fields, neutralButton=True)
                if fields==None: break
            else:
                newstudent=True
                
            if self.checkDate(fields[1])==False or self.checkDate(fields[2])==False:
                fields = multenterbox("Проверьте даты!", "Новый учащийся", fieldNames, fields, neutralButton=True)     
                if fields==None: break
            else:
                newstudent=True

        if newstudent == True:
        
            # Adding new student to list                        
            self.student.append([fields[0], fields[1], fields[2], fields[3], fields[4], fields[5], fields[6],
                                [  # creating a new date list (invisible) in sortable format
                                    fields[1][6], fields[1][7], fields[1][3], fields[1][4], fields[1][0], fields[1][1]
                                ],
                                [
                                    fields[2][6], fields[2][7], fields[2][3], fields[2][4], fields[2][0], fields[2][1]
                                ]
                            ])
            for i in range(len(self.student)): # creating additional integer field to sort by counsel point
                if(self.student[i][3]) != "":
                    try: self.student[i].append(int(self.student[i][3]))
                    except: self.student[i].append(0)
                else:
                    self.student[i].append(0)
            self.student=sorted(self.student, key=lambda student: student[0])           
            self.save()
            self.draw()
        
    def delete(self, event=None):
        """Delete student"""
        selected=self.list.item(self.list.focus())["values"]
        if (mb.askyesno("Удаление", "Удалить учащегося %s?" % str(selected[0])))==True:
            for editedstudent in range(len(self.student)):
                if str(self.student[editedstudent][0])==str(selected[0]):
                    del self.student[editedstudent]
                    self.save()
                    if len(self.student) == 0: # deleting students file
                        remove("students.txt")
                        print("removing file")
                        self.student = []
                    self.draw()
                    break
                    
    def ifInt(self, char):
        """Check if value is integer"""    
        try: int(char) + 1
        except: return False
        else: return True
    
    def checkDate(self, date, event=None):
        """Check correct date"""
        try:
            if  self.ifInt(date[0])==True and\
                self.ifInt(date[1])==True and\
                date[2]=="." and\
                self.ifInt(date[3])==True and\
                self.ifInt(date[4])==True and\
                date[5]=="." and\
                self.ifInt(date[6])==True and\
                self.ifInt(date[7])==True and\
                int(date[0]+date[1])<=31 and\
                int(date[3]+date[4])<=12 and\
                len(date)==8:        
                    check=True
            else: check=False
        except: check=False
        return check
        
    def getNumerical(self, number, event=None):
        """Generate raw number out of real one"""
        output=""
        for char in number:
            if self.ifInt(char)==True: output+=char
        try: return int(output)
        except: return 0
                    
    def mwb(self, event=None):
        webbrowser.open(self.datastring[22])
        
    def pdf(self, event=None):
        if path.isfile(self.datastring[17] + ".pdf"):
            webbrowser.open(self.datastring[17] + ".pdf")
        else:
            mb.showerror("Ошибка", "Файл %s.pdf не найден! Введите имя существующего файла\nв настройках. Файл должен находиться в одной папке с программой." % self.datastring[17])
    
    def settings(self, event=None):        
        """Edit settings
        Data file (data.ini) structure:
        Lines 0-6:  Schedule names
        Lines 7-13: Schedule names for second class (if set)
        14: Note
        15: Program version
        16: Number of backup copies
        17: PDF file path
        18: Show note
        19: Font size
        20: Sort type
        21: Second class (deprecated)
        22: Website
        23: Check updates
        """        
        #while 1:
        fieldNames =\
           ["Кол-во резервных копий (от 2 до 999)", # 16
            "PDF-файл", # 17
            #"Показывать заметку на главной", # 18
            "Размер шрифта", # 19
            #"Число учащихся на главной", # 20
            "Адрес рабочей тетради", # 22
            #"Проверять обновления при выходе", # 23
            "Заметка"] # 14
        fields = []
        fields = multenterbox("Отредактируйте данные:", "Настройки", fieldNames, 
          [self.datastring[16],
           self.datastring[17],
           #self.datastring[18],
           self.datastring[19],
           #self.datastring[20],
           self.datastring[22],
           #self.datastring[23],
           self.datastring[14]])
        if fields == None: return
        
        # datastring[20] - sort type
        
        #datastring[14] = fields[6].strip()
        self.datastring[16] = fields[0].strip()
        self.datastring[17] = fields[1].strip()
        #self.datastring[18] = fields[2].strip()
        self.datastring[19] = fields[2].strip()
        #self.datastring[20] = fields[4].strip()
        self.datastring[22] = fields[3].strip()
        #self.datastring[23] = fields[6].strip()
        self.datastring[14] = fields[4].strip()
        
        if self.datastring[16] == "0" or self.datastring[16] == "1": self.datastring[16] = "2" # backup copies number cannot be < 2
        
        self.saveSettings()
        self.draw()
        self.setFont()
        
    def saveSettings(self):
        with open("data.ini", "w", encoding="utf-8") as datafile:
            for i in range(self.datafile_len): datafile.write(self.datastring[i] + "\n")
        
        
    def setFont(self, font=None):
        """Set font size"""
        try:
            if font==None: font=int(self.datastring[19])
            self.style.configure("Treeview", font="(Arial), %s" % font)
        except:
            mb.showwarning("Внимание", "Проверьте размер шрифта в настройках!")
            #self.style.configure("Treeview", font="(), 9")
        self.draw()
        
    def load(self, filename=None):
        """If students.txt is present, reading from it, else returning void list"""
        student = allstudents = []
        result=False
        if filename==None:
            filename="students.txt"
        if path.exists(filename) == 0:
            print("no file")
        else:    
            try:        
                with open(filename, "r", encoding="utf-8") as f:
                    allstudents = [line.rstrip() for line in f]
                    student.append([allstudents[0], allstudents[1], allstudents[2], allstudents[3], allstudents[4], allstudents[5], allstudents[6],
                                            [ # creating a new date list (invisible) in sortable format
                                                    allstudents[1][6], allstudents[1][7], allstudents[1][3], allstudents[1][4], allstudents[1][0], allstudents[1][1]
                                            ],
                                            [
                                                    allstudents[2][6], allstudents[2][7], allstudents[2][3], allstudents[2][4], allstudents[2][0], allstudents[2][1]
                                            ]
                                    ])
                    b = 7
                    for a in range(int(len(allstudents)/7)-1):
                        student.append([allstudents[b], allstudents[b+1], allstudents[b+2], allstudents[b+3], allstudents[b+4], allstudents[b+5], allstudents[b+6],
                                                                    [ # creating a new date list (invisible) in sortable format
                                                                            allstudents[b+1][6], allstudents[b+1][7], allstudents[b+1][3], allstudents[b+1][4], allstudents[b+1][0], allstudents[b+1][1]
                                                                    ], 
                                                                    [
                                                                            allstudents[b+2][6], allstudents[b+2][7], allstudents[b+2][3], allstudents[b+2][4], allstudents[b+2][0], allstudents[b+2][1]
                                                                    ]
                                                            ])
                        b += 7        
                    for i in range(len(student)): # creating additional temporary integer field for sorting by counsel
                            if(student[i][3]) != "":
                                try: student[i].append(int(student[i][3]))
                                except: pass
                            else:
                                student[i].append(0)
                print("base loaded")
                self.student=student
                result=True
            except:
                mb.showerror("Ошибка", "Ошибка загрузки базы данных!")                
        return result

    def save(self):
        """Save and backing up student list"""                
        limit=int(self.datastring[16])
        
        # First back up
        if not path.exists("./backup"):
            makedirs("./backup")        
        for i in range(1, 99): # counting existing backup files
            file_i = "./backup/students_" + ("%03d" % i) + ".txt"
            if path.isfile(file_i):
                backupnumber = limit
                continue
            else:
                backupnumber = i-1
                break        
        if i < limit+1: # limit not reached, regular backup
            newbkfile = open(file_i, "w", encoding="utf-8")
            for a in range(len(self.student)):
                for i in range(7):
                    newbkfile.write(str(self.student[a][i]) + "\n")
            newbkfile.close()            
        else: # limit reached, first renaming up to the limit
            remove("./backup/students_001.txt")
            for i in range(1, backupnumber):
                if i <= limit:
                    file_i = "./backup/students_" + ("%03d" %  i)    + ".txt"
                    file_i1= "./backup/students_" + ("%03d" % (i+1)) + ".txt"
                    rename(file_i1, file_i)
        
            with open(file_i1, "w", encoding="utf-8") as newbkfile:
                for a in range(len(self.student)):
                    for i in range(7):
                        newbkfile.write(str(self.student[a][i]) + "\n")
    
            for i in range(limit, 999): # deleting all files after limit, if any
                file_i= "./backup/students_" + ("%03d" % i) + ".txt"
                if path.isfile(file_i):
                    remove(file_i)
    
        # Now save
        if len(self.student)!=0:
            with open("students.txt", "w", encoding="utf-8") as newfile:
                for a in range(len(self.student)):
                    for i in range(7):
                        newfile.write(str(self.student[a][i]) + "\n")                    
        else:
            try: remove("students.txt")
            except: pass
                    
    def imp(self):
        filename=filedialog.askopenfilename(filetypes=[("База данных Students", ".txt")], defaultextension='.txt')        
        if self.load(filename)==True:
            self.save()
            self.draw()
        
    def exp(self):
        pass
        
    def wipe(self):
        if mb.askyesno("Очистка", "Вы уверены, что хотите удалить всех учащихся? Это действие можно будет отменить только путем импорта резервной копии (если есть)!")==True:            
            self.student=[]
            self.save()
            self.draw()
    
    def readme(self):
        webbrowser.open("readme.txt")
        
    def site(self):
        webbrowser.open("http://studentsprogram.blogspot.com")
        
    def updateCheck(self):
        """Check new version"""
        def run(threadName, delay):           
            try:    
                file = urllib.request.urlopen("https://raw.githubusercontent.com/antorix/Students/master/version.txt")
                version = str(file.read())
                thisversion = [int(currentversion[0]), int(currentversion[2]), int(currentversion[4])]
                newversion = [int(version[2]), int(version[4]), int(version[6])]
                if newversion > thisversion:
                    print("new version found, trying to download update")
                    self.updateInstall()
            except: print("can't check new version")
        try: _thread.start_new_thread(run,("Thread-Load", 1,))
        except: print("can't run thread")
        
    def updateInstall(self):
        """Install update"""
        def run(threadName, delay):            
            try: urllib.request.urlretrieve("http://github.com/antorix/Students/raw/master/update.zip", "update.zip")
            except: print("download failed")
            else:
                print("download complete")                    
                try:
                    zip=zipfile.ZipFile("update.zip", "r")
                    zip.extractall("")
                    zip.close()
                    os.remove("update.zip")
                except: print("unpacking failed")
                else:
                    print("unpacking complete")
                    mb.showinfo("Обновление", "Успешно установлено обновление! Изменения вступят в силу после перезапуска программы.")                                        
        try: _thread.start_new_thread(run,("Thread-Load", 1,))
        except: print("can't run thread")
        
    def deleteObsolete(self):
        """Delete obsolete files from older versions"""
        files=[]
        files.append("help.png")
        files.append("add_user.png")
        files.append("mwb.png")
        files.append("pdf.png")
        files.append("profile.png")
        files.append("settings.png")
        files.append("modules.py")
        for file in files:
            if os.path.exists(file): os.remove(file)
            
    def tip(self, text="test", time=2000):
        """Show self-destructing notification"""           
        label=tk.Label(self.master, fg="seagreen", font="(), 8")
        label.grid(column=0, row=2, sticky="ws")
        label["text"]=text
        label.after(time, lambda: label.grid_remove())
        
# Launch interface
app=Root()
app.mainloop()
