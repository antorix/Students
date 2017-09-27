#!/usr/bin/python
# -*- coding: utf-8 -*-

currentversion = "3.1.0"

import tkinter as tk
from tkinter import ttk
import webbrowser
import datetime
import urllib.request
import os
import sys
from os import name, path, remove, rename, makedirs
import tkinter.messagebox as mb
import _thread
from time import strftime, localtime
from tkinter import filedialog
import urllib.request
import zipfile
import time
import copy
import tkinter.scrolledtext as ScrolledText

def setFont(font=None):
    """Get nicest monotype fonts from the system"""
    fonts=[]
    if os.name=="nt":
        try:
            osFonts=os.listdir("C:/WINDOWS/fonts")
            if "LiberationMono-Regular.ttf" in osFonts: fonts.append("Liberation Mono")
            if "DejaVuSansMono_0.ttf" in osFonts: fonts.append("DejaVu Sans Mono")
            if "lucon.ttf" in osFonts: fonts.append("Lucida Console")
            if "cousine-regular.ttf" in osFonts: fonts.append("Cousine")
            if "firamono-regular.ttf" in osFonts: fonts.append("Fira Mono")
            if "PTM55F.ttf" in osFonts: fonts.append("PT Mono")
            if "ubuntumono-r.ttf" in osFonts: fonts.append("Ubuntu Mono")            
        except: print("no good font found on Windows")
    fonts.append("Courier New")
    return fonts[0]

def ifInt(char):
    """Check if value is integer"""    
    try: int(char) + 1
    except: return False
    else: return True

def getNumerical(number):
    """Generate raw number out of real one"""
    output=""
    for char in number:
        if ifInt(char)==True: output+=char
    try: return int(output)
    except: return 0

def checkDate(date):
    """Check correct date"""
    try:
        if  ifInt(date[0])==True and\
            ifInt(date[1])==True and\
            date[2]=="." and\
            ifInt(date[3])==True and\
            ifInt(date[4])==True and\
            date[5]=="." and\
            ifInt(date[6])==True and\
            ifInt(date[7])==True and\
            int(date[0]+date[1])<=31 and\
            int(date[3]+date[4])<=12 and\
            len(date)==8:        
                check=True
        else: check=False
    except: check=False
    return check
    
def getGender(name):
    """Returns gender м/ж depending on name string"""
    return name[name.index("{")+1]
    
def getStatus(name):
    """Returns status +/- depending on name string"""
    return name[name.index("{")+2]
    
def getRealName(name):
    """Returns real name cleaned from {}"""
    try:
        return name[ 0 : name.index("{") ]
    except:
        return name
        
def getStudyList():
    """Load study list from studies.ini"""
    output=[]
    try:
        with open("studies.ini", "r", encoding="utf-8") as file:
            output = [line.rstrip() for line in file]        
    except:
        print("can't load studies")
    return output
    
def getSettings():
    """Load data strings from data.ini"""    
    while 1:
        try:
            with open("data.ini", "r", encoding="utf-8") as file:
                datastring=[line.rstrip() for line in file]
            if len(datastring)<20:
                print("data file exists, but the format is invalid, creating a new one")
                raise
        except:
            with open("data.ini", "w", encoding="utf-8") as file:
                file.write(
                    "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n" + currentversion + "\n30\ns-89-u-4up.pdf\nв\n9\n0\n-\nhttps://www.jw.org/ru/публикации/свидетелей-иеговы-встреча-рабочая-тетрадь/\n1\n"
                )
        else:
            break
    return datastring
    
def clearReturns(input):
    """Delete all end of lines from string"""
    output=""
    for line in input:
        newline = line.rstrip('\r\n')
        output = output + newline
    return output

class Setup(tk.Frame):
    """Open settings window"""
    
    def __init__(self, root, fromNote):
        self.root=root
        self.fromNote=fromNote
        
        # Create card window
        self.window=tk.Toplevel()
        self.window.withdraw() 
        self.window.title("Настройки")
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        self.window.focus_force()
        self.window.bind_class("Entry", "<3>", self.root.contextMenu)
        self.window.bind_class("Text", "<3>", self.root.contextMenu)
        self.window.bind("<Return>", self.save)
        self.window.bind("<Escape>", lambda x: self.window.destroy())        
        self.window.tk.call('wm', 'iconphoto', self.window._w, self.root.img[13])
        
        # Styling
        self.style=ttk.Style()
        self.style.configure("small.TButton", font="{} 8")
        pad=5
        ipad=5
        
        # Fields frame
        frame1=tk.Frame(self.window)
        frame1.grid(column=0, row=0, padx=pad, sticky="nesw")
        frame1.columnconfigure(1, weight=1)        

        # Labels and fields
        self.entries=[]
        list=["Размер шрифта", "Цвета", "Резервные копии", "Файл бланков", "Ссылка на НХЖС", "Заметка"]
        for row, text in zip(range(len(list)), list):
            ttk.Label(frame1, text=text, justify="right").grid(column=0, row=row, padx=pad, pady=pad, sticky="en")                    
        for row in range(len(list)):
            if row==0:                                                          # размер шрифта
                self.myfont = tk.IntVar()                
                self.entries.append(ttk.Combobox(frame1, width=3, height=20, font=("", self.root.fontsize), state="readonly", textvariable=self.myfont))
                self.entries[row]["values"]=[5,6,7,8,9,10,11,12,13,14,15]
                self.entries[row].grid(column=1, row=row, pady=pad, sticky="wns")
            elif row==1:                                                        # цвет
                self.colors = tk.StringVar()
                self.entries.append(ttk.Checkbutton(frame1, text="", onvalue="1", offvalue="0", variable=self.colors))
                self.entries[row].grid(column=1, row=row, pady=pad, sticky="wns")
            elif row==2:                                                        # резервные копии
                self.entries.append(tk.Entry(frame1, font=("", self.root.fontsize), width=6, relief="flat"))
                self.entries[row].grid(column=1, row=row, pady=pad, sticky="wns")
            elif row==3 or row==4:                                              # ссылки
                self.entries.append(tk.Text(frame1, font=("", self.root.fontsize), relief="flat", width=40, height=3))
                self.entries[row].grid(column=1, row=row, pady=pad, sticky="wnse")    
            elif row==5:                                                        # заметка
                self.entries.append(ScrolledText.ScrolledText(frame1, font=("", self.root.fontsize), relief="flat", background="lightyellow", width=30, height=5))
                self.entries[row].grid(column=1, row=row, pady=pad, sticky="wnse")            
            
        self.entries[0].set(int(self.root.datastring[19]))
        self.colors.set(self.root.datastring[23])
        self.entries[2].insert(0, self.root.datastring[16])
        self.entries[3].insert(0.0, self.root.datastring[17])
        self.entries[4].insert(0.0, self.root.datastring[22])
        self.entries[5].insert(0.0, self.root.datastring[14])
        if self.fromNote==True:
            self.entries[5].focus_force()
        else:
            self.entries[0].focus_force()
        """
        14: Note
        15: Program version
        16: Number of backup copies
        17: PDF file path
        18: Gender filter
        19: Font size
        20: Sort type
        21: Active status filter
        22: Workbook URL
        23: Colorize
        """
        
        # Buttons        
        ttk.Button(frame1, text="Найти",    image=self.root.img[14], compound="left", style="small.TButton", command=self.browse).                         grid(column=2, row=3, pady=pad*2, sticky="ne")
        ttk.Button(frame1, text="Вставить", image=self.root.img[15], compound="left", style="small.TButton", command=lambda: self.insert(self.entries[4])).grid(column=2, row=4, pady=pad*2, sticky="ne")
        
        # Buttons frame to save/cancel
        frame2=tk.Frame(self.window)
        frame2.grid(column=0, row=1, sticky="es")
        ttk.Button(frame2, text="ОК", image=self.root.img[17], compound="left", command=self.save).grid(column=1, row=1, padx=pad, pady=pad, ipadx=ipad*2, ipady=ipad, sticky="we")
        ttk.Button(frame2, text="Отмена", command=self.window.destroy).grid(column=2, row=1, padx=pad, pady=pad, ipadx=ipad*2, ipady=ipad, sticky="we")
        self.window.protocol("WM_DELETE_WINDOW", self.window.destroy)
        
        # Run
        self.window.deiconify()
        self.window.wait_window()
        
    def browse(self, event=None):
        filename=filedialog.askopenfilename()
        if filename!="":
            self.entries[3].delete(0.0, "end")        
            self.entries[3].insert(0.0, filename)
        self.entries[3].focus_force()
        
    def insert(self, widget):
        """Insert clipboard into field"""
        widget.delete(0.0, "end")        
        widget.event_generate("<<Paste>>")
        widget.focus_force()
        
    def save(self, event=None):
        """Save settings"""
        if ifInt(self.entries[2].get().strip())==False or int(self.entries[2].get().strip())<3:
            mb.showwarning("Внимание", "Количество резервных копий должно быть целым числом и не меньше 3!")
            self.entries[2].focus_force()        
        else:                                                                   # everything is ok, save
            self.root.datastring[19]=str(self.myfont.get())
            self.root.datastring[23]=self.colors.get()
            self.root.datastring[16]=self.entries[2].get().strip()
            self.root.datastring[17]=clearReturns(self.entries[3].get(0.0, "end").strip())
            self.root.datastring[22]=clearReturns(self.entries[4].get(0.0, "end").strip())
            self.root.datastring[14]=clearReturns(self.entries[5].get(0.0, "end").strip())
            self.window.destroy()        
    def getFields(self):
        return self.entries    

class Card(tk.Frame):
    """Open student card (new or existing)"""
    
    def __init__(self, root, fields):        
        self.root=root
        self.fields=fields
        
        # Obtain technical information from {} and cut brackets to display properly
        if fields[0]!="":
            self.gender=getGender(fields[0])
            self.status=getStatus(fields[0])
            self.realName = getRealName(fields[0])
        else:
            self.gender=None
            self.status=None
            self.realName = ""
        
        # Create card window
        self.window=tk.Toplevel()
        self.window.withdraw() 
        self.window.title(getRealName(self.fields[0]))
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(1, weight=1)
        self.window.focus_force()
        self.window.bind_class("Entry", "<3>", self.root.contextMenu)
        self.window.bind_class("Text", "<3>", self.root.contextMenu)
        self.window.bind("<Return>", self.save)
        self.window.bind("<Escape>", self.cancel)
        self.window.tk.call('wm', 'iconphoto', self.window._w, self.root.img[7])
        
        # Styling
        self.style=ttk.Style()
        self.style.configure("small.TButton", font="{} 8")
        pad=ipad=5
        
        # Fields frame
        frame1=tk.Frame(self.window)
        frame1.grid(column=0, columnspan=2, row=0, padx=pad, sticky="nesw")
        frame1.columnconfigure(1, weight=1)
        frame1.rowconfigure(0, weight=1)
        
        # Labels and fields
        self.entries=[]
        for row, text in zip(range(7), ["Имя", "Выступление", "Помощь", "Урок", "Заметка", "Совет", "Пройденные\nуроки"]):
            ttk.Label(frame1, text=text, justify="right").grid(column=0, row=row, padx=pad, pady=pad, sticky="e")            
        for row in range(7):
            if row==0:                                                          # name
                self.entries.append(tk.Entry(frame1, font="{%s} %s" % ("", self.root.fontsize), relief="flat"))
                self.entries[row].grid(column=1, row=row, pady=pad, sticky="we")
                self.entries[row].insert(0, self.realName)                
            elif row==3:                                                        # study
                self.studies = tk.StringVar()                
                self.entries.append(ttk.Combobox(frame1, width=40, height=20, font=("", self.root.fontsize), state="readonly", textvariable=self.studies)) # publisher/date
                self.entries[row]["values"]=self.root.studyList       
                self.entries[row].grid(column=1, columnspan=2, row=row, pady=pad, sticky="we")                
                for s in self.root.studyList:
                    if "." in s and fields[row] == s[0:s.index(".")]:
                        self.entries[row].set(s)
                
            elif row<5:
                self.entries.append(tk.Entry(frame1, font="{%s} %s" % ("", self.root.fontsize), relief="flat"))
                self.entries[row].grid(column=1, columnspan=2, row=row, pady=pad, sticky="we")
                self.entries[row].insert(0, fields[row])
            else:
                self.entries.append(ScrolledText.ScrolledText(frame1, font="{%s} %s" % ("", self.root.fontsize), wrap="word", relief="flat", height=3, width=40))                
                self.entries[row].grid(column=1, columnspan=3, row=row, pady=pad, sticky="wesn")
                self.entries[row].insert(0.0, fields[row])
        self.entries[0].focus_force()
        
        # Gender radio selection
        self.entries.append(tk.StringVar())        
        if self.gender=="б":
            self.entries[7].set(1)
        elif self.gender!=None:
            self.entries[7].set(0)
        ttk.Radiobutton(frame1, variable=self.entries[7], text="Брат", value=1, command=self.setGender).grid(column=2, row=0, padx=pad, pady=pad, sticky="we")
        ttk.Radiobutton(frame1, variable=self.entries[7], text="Сестра", value=0, command=self.setGender).grid(column=3, row=0, padx=pad, pady=pad, sticky="we")        
        
        # Small buttons
        ttk.Button(frame1, text="Сегодня", image=self.root.img[9],  compound="left", style='small.TButton', command=lambda: self.today(self.entries[1])).grid(column=2, row=1, sticky="e")
        ttk.Button(frame1, text="Никогда", image=self.root.img[10], compound="left", style='small.TButton', command=lambda: self.never(self.entries[1])).grid(column=3, row=1, sticky="e")        
        ttk.Button(frame1, text="Сегодня", image=self.root.img[9],  compound="left", style='small.TButton', command=lambda: self.today(self.entries[2])).grid(column=2, row=2, sticky="e")
        ttk.Button(frame1, text="Никогда", image=self.root.img[10], compound="left", style='small.TButton', command=lambda: self.never(self.entries[2])).grid(column=3, row=2, sticky="e")
        ttk.Button(frame1, text="Пройден", image=self.root.img[11], compound="left", style='small.TButton', command=self.complete).grid(column=3, row=3, sticky="e")
        ttk.Button(frame1, text="Очистить",image=self.root.img[12], compound="left", style='small.TButton', command=self.clear).grid(column=3, row=4, sticky="e")
        
        # Status checkbox
        self.entries.append(tk.IntVar())
        if self.status=="+" or self.status==None:
            self.entries[8].set(1)
        else:
            self.entries[8].set(0)
        ttk.Checkbutton(self.window, text="Активен", variable=self.entries[8], onvalue=1, offvalue=0, command=self.setStatus).grid(column=0, row=1, padx=pad*2, pady=pad, sticky="w")        
   
        # Buttons frame to save/cancel
        frame2=tk.Frame(self.window)
        frame2.grid(column=0, row=1, pady=pad, sticky="es")
        ttk.Button(frame2, text="Отмена", command=self.cancel).pack(padx=pad, ipadx=ipad*2, ipady=ipad, side="right")
        ttk.Button(frame2, text="ОК", image=self.root.img[17], compound="left", command=self.save).pack(padx=pad, ipadx=ipad*2, ipady=ipad, side="right")
        self.window.protocol("WM_DELETE_WINDOW", self.cancel)
        
        # Run
        self.window.deiconify() 
        self.window.wait_window()
        
    def setGender(self):
        """Defines gender character according to radio buttons"""
        if int(self.entries[7].get())==1:
            self.gender="б"
        else:
            self.gender="с"
            
    def setStatus(self):
        """Defines active character according to radio buttons"""
        if int(self.entries[8].get())==1:
            self.status="+"
        else:
            self.status="-"
        
    def today(self, widget):
        """Date sets to today"""
        widget.delete(0,"end")
        widget.insert(0, time.strftime("%d.%m", time.localtime()) + "." + str(int(time.strftime("%Y", time.localtime()))-2000))
        
    def never(self, widget):
        """Date sets to 00.00.00"""
        widget.delete(0,"end")
        widget.insert(0, "00.00.00")
        
    def complete(self):
        """Complete study and save it to history"""
        study=self.entries[3].get()
        if self.entries[6].get(0.0, "end").strip()=="":
            self.entries[6].insert("end", study[ 0: study.index(".")])
        elif self.entries[3].get().strip()!="":
            self.entries[6].insert("end", ", %s" % study[ 0: study.index(".")])        
        self.entries[3].set("")
        
    def clear(self):
        """Clear note"""
        self.entries[4].delete(0, "end")        
        
    def save(self, event=None):
        """Save student fields"""
        if self.entries[0].get().strip()=="":                                   # check for errors
            mb.showwarning("Внимание", "Требуется имя!")
            self.entries[0].focus_force()
        elif self.gender==None:
            mb.showwarning("Внимание", "Требуется пол!")
            self.window.focus_force()
        elif checkDate(self.entries[1].get().strip())==False:
            mb.showwarning("Внимание", "Дата выступления должна быть в формате\nДД.ММ.ГГ (например 30.11.16)!")
            self.entries[1].focus_force()
        elif checkDate(self.entries[2].get().strip())==False:
            mb.showwarning("Внимание", "Дата помощи должна быть в формате\nДД.ММ.ГГ (например 30.11.16)!")
            self.entries[2].focus_force()
        else:                                                                   # everything is ok, save
            for row in range(7):
                if row==0:                                                      # process name
                    self.fields[0] = "%s{%s%s}" % (self.entries[0].get().strip(), self.gender, self.status) # add tech data to name
                elif row==3:                                                    # process study
                    study=self.entries[3].get()
                    if "." in study:
                        self.fields[3] = study[0:study.index(".")]
                    else:
                        self.fields[3]=""
                elif row<5:
                    self.fields[row]=self.entries[row].get().strip()            
                else:
                    self.fields[5]=clearReturns(self.entries[5].get(0.0, "end").strip())
                    self.fields[6]=clearReturns(self.entries[6].get(0.0, "end").strip())
            
            self.window.destroy()        
    
    def cancel(self, event=None):
        del self.fields
        #print(self.fields)
        self.window.destroy()
    
    def getFields(self):
        try:
            return self.fields
        except:
            pass

class Root(ttk.Frame):
    """Main interface"""
    
    def __init__(self):
        tk.Frame.__init__(self)
        self.master.withdraw()        
        
        # Load data from files
        self.datastring=getSettings()
        self.student=[]
        self.load()
        self.studyList=getStudyList()        
        #print(self.student)
        
        # Load images        
        self.img=[]
        self.img.append(tk.PhotoImage(file="arrow.gif"))                        # 0
        self.img.append(tk.PhotoImage(file="pdf.gif"))                          # 1
        self.img.append(tk.PhotoImage(file="mwb.gif"))                          # 2
        self.img.append(tk.PhotoImage(file=""))                                 # 3
        self.img.append(tk.PhotoImage(file="add_user.gif"))                     # 4
        self.img.append(tk.PhotoImage(file="icon.png"))                         # 5
        self.img.append(tk.PhotoImage(file=""))                                 # 6
        self.img.append(tk.PhotoImage(file="user32.gif"))                       # 7
        self.img.append(tk.PhotoImage(file=""))                                 # 8
        self.img.append(tk.PhotoImage(file="cal_add.gif"))                      # 9
        self.img.append(tk.PhotoImage(file="cal_del.gif"))                      # 10
        self.img.append(tk.PhotoImage(file="tick.gif"))                         # 11
        self.img.append(tk.PhotoImage(file="wipe.gif"))                         # 12
        self.img.append(tk.PhotoImage(file="settings.gif"))                     # 13
        self.img.append(tk.PhotoImage(file="folder.gif"))                       # 14
        self.img.append(tk.PhotoImage(file="paste.gif"))                        # 15
        self.img.append(tk.PhotoImage(file="save.gif"))                         # 16
        self.img.append(tk.PhotoImage(file="save.gif"))                         # 17
        
        # Window and styling
        self.geo=[]
        self.winSizeX=640
        self.winSizeY=480
        self.master.bind("<Configure>", self.getWinSize)
        try:            
            self.geo.append(int(self.datastring[0])) # w
            self.geo.append(int(self.datastring[1])) # h 
            self.geo.append(int(self.datastring[2])) # x
            self.geo.append(int(self.datastring[3])) # y
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
        self.master.minsize(100,220)        
        self.master.protocol("WM_DELETE_WINDOW", self.fullQuit)
        if name=="nt":
            self.master.iconbitmap("icon.ico")
        else:
            self.tk.call('wm', 'iconphoto', self.master._w, self.img[5])
        self.master.title("Students")        
        self.master.columnconfigure(0, weight=1)        
        self.master.rowconfigure(1, weight=1)
        self.padx=self.pady=5
        self.ipadxy=0
        self.fontsize=9
        self.style = ttk.Style()
        
        # Settings
        self.menubar = tk.Menu(self.master)
        self.menuFile = tk.Menu(self.menubar, tearoff=0)                       
        self.menubar.add_cascade(label="Файл", menu=self.menuFile)
        self.menuFile.add_command(label="Импорт", command=self.imp)
        self.menuFile.add_command(label="Очистка", command=self.wipe)
        self.menuFile.add_separator()
        self.menuFile.add_command(label="Выход", command=self.fullQuit)        
        self.menuSettings = tk.Menu(self.menubar, tearoff=0)
        #self.menubar.add_cascade(label="Настройки", command=self.settings)
        self.menuHelp = tk.Menu(self.menubar, tearoff=0)                       
        self.menubar.add_cascade(label="Помощь", menu=self.menuHelp)
        self.menuHelp.add_command(label="Справка", command=lambda: webbrowser.open("readme.txt"))
        self.menuHelp.add_command(label="Сайт", command=lambda: webbrowser.open("http://studentsprogram.blogspot.com"))
        self.menuHelp.add_separator()
        self.menuHelp.add_command(label="О программе", command=lambda: mb.showinfo("О программе", "Students (v.%s)\n\nРаспределение и назначение учебных заданий\n\nБесплатно, лицензия GPL" % currentversion))
        self.master.config(menu=self.menubar)
        
        # Gender radio button filter
        self.genderFrame=ttk.Frame(self.master)        
        self.genderFrame.grid(column=0, row=0, padx=self.padx, pady=self.pady)           
        self.gender = tk.StringVar()
        self.gender.set(self.datastring[18])
        ttk.Radiobutton(self.genderFrame, variable=self.gender, text="Все",    value="в", command=self.setGender).grid(column=0, row=0, padx=self.padx)
        ttk.Radiobutton(self.genderFrame, variable=self.gender, text="Братья", value="б", command=self.setGender).grid(column=1, row=0, padx=self.padx)
        ttk.Radiobutton(self.genderFrame, variable=self.gender, text="Сестры", value="с", command=self.setGender).grid(column=2, row=0, padx=self.padx)
        
        # Active checkbutton
        self.status = tk.StringVar()
        self.status.set(self.datastring[21])
        ttk.Checkbutton(self.master, text="Скрыть неактивных", variable=self.status, onvalue="+", offvalue="-", command=self.setStatus).grid(column=0, row=0, padx=self.padx, sticky="e")
        
        # Students list
        self.style.configure("main.Treeview", relief="ridge")
        self.headers=["Имя", "Выступление", "Помощь", "Урок", ""]
        self.list=ttk.Treeview(self.master, columns=self.headers, show="headings", style="main.Treeview")
        self.list.grid(column=0, row=1, padx=self.padx, pady=self.pady*0, sticky="wnse")
        self.list.focus()
        self.rightScrollbar = ttk.Scrollbar(self.list, orient="vertical", command=self.list.yview) 
        self.list.configure(yscrollcommand=self.rightScrollbar.set) 
        self.rightScrollbar.pack(side="right", fill="y")
        
        # Warning about inactive
        self.activewarn=ttk.Label(self.master, background="white", foreground="gray", font=("", 8))
        
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
        
        # Action frame (under list)
        self.actionFrame=tk.Frame(self.master)
        self.actionFrame.columnconfigure(1, weight=1)
        self.actionFrame.rowconfigure(0, weight=1)
        self.actionFrame.grid(column=0, row=2, padx=self.padx, pady=self.pady, sticky="nesw")
        
        # Buttons 
        self.buttonFrame=tk.Label(self.actionFrame)
        self.buttonFrame.grid(column=0, row=0, pady=self.pady, sticky="wsne")
        ttk.Button(self.buttonFrame, style='material.TButton', text="Создать",  image=self.img[4], compound="left", command=self.new).grid(column=0, row=0, padx=self.padx, pady=self.pady, sticky="we")
        ttk.Button(self.buttonFrame, style='material.TButton', text="Задания",  image=self.img[1], compound="left", command=self.pdf).grid(column=1, row=0, padx=self.padx, pady=self.pady, sticky="we")
        ttk.Button(self.buttonFrame, style='material.TButton', text="НХЖС",     image=self.img[2], compound="left", command=lambda: webbrowser.open(self.datastring[22])).grid(column=0, row=1, padx=self.padx, pady=self.pady, sticky="swe")
        ttk.Button(self.buttonFrame, style='material.TButton', text="Настройки",image=self.img[13], compound="left",command=self.settings).grid(column=1, row=1, padx=self.padx, pady=self.pady, sticky="swe")
        
        # Заметка
        self.statNote=ttk.LabelFrame(self.actionFrame, text="Заметка")
        self.statNote.grid(column=1, row=0, padx=self.padx, pady=self.pady, sticky="ns")
        self.notepad=ScrolledText.ScrolledText(self.statNote, wrap="word", relief="flat", cursor="hand2", background="lightyellow", height=6, width=50)
        self.notepad.pack(anchor="nw", padx=self.padx, pady=self.pady*2)
        self.notepad.bind("<1>", self.settings)#lambda x: self.settings(fromNote=True))
        
        # Статистика
        self.statFrame=ttk.LabelFrame(self.actionFrame, text="Статистика")
        self.statFrame.grid(column=2, row=0, padx=self.padx, pady=self.pady, sticky="nse")
        self.stats=ttk.Label(self.statFrame)
        self.stats.grid(padx=self.padx, pady=self.pady, sticky="wn")
        self.stats["text"]="Всего учащихся:\nБратьев:\nСестер:\nНикогда не выступали:\nНикогда не помогали:\nБез урока:\nНеактивны:" 
        self.stats2=ttk.Label(self.statFrame, style='stats.TLabel')
        self.stats2.grid(column=1, row=0, padx=self.padx, pady=self.pady, sticky="en")        
        
        # Footer
        self.statusBar=tk.Label(self.master, fg="gray40", font="(), 8")
        self.statusBar.grid(column=0, row=3, sticky="es")        
        ttk.Separator(self.master, orient='horizontal').grid (column=0, row=2, sticky='swe')
        ttk.Sizegrip(self.master).grid(column=0, row=3, sticky="se")       
        
        # Run
        self.deleteObsolete()
        self.sortList=tk.IntVar()           
        self.resizeList()
        self.font=setFont()
        self.sortList.set(int(self.datastring[20]))
        self.sort(self.headers[self.sortList.get()])        
        self.getWinSize()
        self.updateCheck()
        self.master.deiconify()
        self.master.wait_window()
        
    def draw(self):
        """Update list and all stats"""
        try: self.list.delete(*self.list.get_children())        
        except: return        
        
        if self.sortList.get()==0: # by name
            self.student=sorted(self.student, key=lambda s: s[0])
        elif self.sortList.get()==1: # by date1
            self.student=sorted(self.student, key=lambda s: s[7])
        elif self.sortList.get()==2: # by date2
            self.student=sorted(self.student, key=lambda s: s[8])
        elif self.sortList.get()==3: # by study
            self.student=sorted(self.student, key=lambda s: getNumerical(s[3]))
        elif self.sortList.get()==4: # by note
            self.student=sorted(self.student, key=lambda s: s[4])
        
        # Create virtual list to display with all filters
        self.displayList = copy.deepcopy(self.student)
        i=0    
        while i<len(self.displayList):            
            if self.gender.get()=="б" and getGender(self.displayList[i][0])=="с":
                del self.displayList[i]
                i=0
                continue
            elif self.gender.get()=="с" and getGender(self.displayList[i][0])=="б":
                del self.displayList[i]
                i=0
                continue
            elif self.status.get()=="+" and getStatus(self.displayList[i][0])!="+":
                del self.displayList[i]
                i=0
                continue
            i+=1        
        self.displayList2 = copy.deepcopy(self.displayList)
        
        # Cleanse name from {}
        for s in self.displayList:
            s[0] = getRealName(s[0])                    
        
        for col in self.headers: self.list.heading(col, text=col.title(), command=lambda c=col: self.sort(c))
        if self.datastring[23]=="1":
            for i in range(len(self.displayList)):
                if   getGender(self.displayList2[i][0])=="б" and getStatus(self.displayList2[i][0])=="+":
                    self.list.insert('', 'end', values=self.displayList[i], tags = ('brother+',))
                elif getGender(self.displayList2[i][0])=="б" and getStatus(self.displayList2[i][0])=="-":
                    self.list.insert('', 'end', values=self.displayList[i], tags = ('brother-',))
                elif getGender(self.displayList2[i][0])=="с" and getStatus(self.displayList2[i][0])=="+":
                    self.list.insert('', 'end', values=self.displayList[i], tags = ('sister+',))
                elif getGender(self.displayList2[i][0])=="с" and getStatus(self.displayList2[i][0])=="-":
                    self.list.insert('', 'end', values=self.displayList[i], tags = ('sister-',))            
                self.list.tag_configure('brother+', foreground='navy')
                self.list.tag_configure('brother-', foreground='cornflowerblue')
                self.list.tag_configure('sister+',  foreground='purple')
                self.list.tag_configure('sister-',  foreground='plum')
        else:
            for d in self.displayList:
                self.list.insert('', 'end', values=d)
        self.style.configure("Treeview", font=("", self.fontsize))
        
        # Count statistics
        noStudy = noDate1 = noDate2 = brothers = sisters = self.noactive = 0        
        for student in self.student:
            if getGender(student[0])=="б": brothers+=1
            if getGender(student[0])=="с": sisters+=1
            if getStatus(student[0])=="-": self.noactive+=1
            if student[1]=="00.00.00": noDate1+=1
            if student[2]=="00.00.00": noDate2+=1
            if student[3]=="": noStudy+=1
        self.stats2["text"]="%d\n%d\n%d\n%d\n%d\n%d\n%d" % (len(self.student), brothers, sisters, noDate1, noDate2, noStudy, self.noactive)
        
        # Show note        
        self.notepad["state"]="normal"
        self.notepad.delete(0.0, "end")
        self.notepad.insert(0.0, self.datastring[14])
        self.notepad["state"]="disabled"
        
        # Show change time
        try:
            self.statusBar["text"] = "Последнее изменение: %s     " % datetime.datetime.fromtimestamp(os.path.getmtime("students.txt")) # last core save            
        except: pass
        
        # Mark inactive
        if self.status.get()=="+" and self.noactive>0:
            self.activewarn.grid(column=0, row=1, sticky="es", pady=2, padx=25)
            self.activewarn["text"]="Скрыто: %d" % (self.noactive)
        else:
            self.activewarn.grid_forget()
        
        # Adjust fonts
        self.notepad["font"]=("", self.fontsize)
        self.stats["font"]=("", self.fontsize)
        self.stats2["font"]=("", self.fontsize)
        
    def resizeList(self):
        """Resize columns"""
        self.list.column(0, width=130)
        self.list.column(1, width=70)
        self.list.column(2, width=70)
        self.list.column(3, width=20)
        self.list.column(4, width=100)
        
    def getWinSize(self, event=None, save=None):
        """Manage window geometry saving"""        
        ws=self.master.winfo_width()
        hs=self.master.winfo_height()
        x=self.master.winfo_x()
        y=self.master.winfo_y()
        if save==True and (ws!=self.geo[0] or hs!=self.geo[1] or x!=self.geo[2] or y!=self.geo[3]):
            
            self.datastring[0]=str(ws)
            self.datastring[1]=str(hs)
            self.datastring[2]=str(x)
            self.datastring[3]=str(y)
            self.saveSettings()
            
    def fullQuit(self, event=None):
        """Quit process"""
        self.getWinSize(save=True)
        self.master.destroy()
        self.master.quit()
    
    def sort(self, col):
        """sort tree contents when a column header is clicked on"""
        if col!="":
            for n in range(len(self.headers)): self.list.heading(n, image="")
        for n in range(len(self.headers)-1):
            if col==self.headers[n]:
                self.sortList.set(n)
                self.list.heading(n, image=self.img[0])
                self.datastring[20]=str(n)                
        #self.draw()        
        self.saveSettings()
        
    def select(self, event=None):
        """Select student from list"""
        selected=self.list.item(self.list.focus())["values"]
        self.master.clipboard_clear()        
        self.master.clipboard_append(str(selected[0]))
        self.tip(str(selected[0]) + " в буфере обмена ", 1000)        

    def open(self, event=None):
        """Open student card"""        
        selected=self.list.item(self.list.focus())["values"]
        if selected=="": return
        self.select()
        for editedstudent in range(len(self.student)):            
            if str(getRealName(self.student[editedstudent][0]))==getRealName(str(selected[0])):
                fields=Card(self, self.student[editedstudent]).getFields()
                if fields!=None:
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
                break
    
    def new(self, event=None):
        """Create new student"""        
        fields=Card(self, fields=["", "00.00.00", "00.00.00", "", "", "", ""]).getFields()
        if fields!=None:        
            # Add new student to list                        
            self.student.append([fields[0], fields[1], fields[2], fields[3], fields[4], fields[5], fields[6],
                                [  # create new date list (invisible) in sortable format
                                    fields[1][6], fields[1][7], fields[1][3], fields[1][4], fields[1][0], fields[1][1]
                                ],
                                [
                                    fields[2][6], fields[2][7], fields[2][3], fields[2][4], fields[2][0], fields[2][1]
                                ]
                            ])
            for i in range(len(self.student)): # create additional integer field to sort by counsel point
                if(self.student[i][3]) != "":
                    try: self.student[i].append(int(self.student[i][3]))
                    except: self.student[i].append(0)
                else:
                    self.student[i].append(0)
            self.save()            
            self.gender.set("в")
            self.status.set(0)            
            self.draw()            
        
    def delete(self, event=None):
        """Delete student"""
        selected=self.list.item(self.list.focus())["values"]
        if selected=="": return
        if (mb.askyesno("Удаление", "Удалить учащегося %s?" % str(selected[0])))==True:
            for editedstudent in range(len(self.student)):
                if getRealName(str(self.student[editedstudent][0]))==getRealName(str(selected[0])):
                    del self.student[editedstudent]
                    self.save()
                    if len(self.student) == 0: # deleting students file
                        remove("students.txt")
                        print("removing file")
                        self.student = []
                    self.draw()
                    break
        
    def pdf(self, event=None):
        if path.isfile(self.datastring[17]):
            webbrowser.open(self.datastring[17])
        else:
            mb.showerror("Ошибка", "Файл %s не найден! Введите имя существующего файла\nв настройках." % self.datastring[17])
    
    def settings(self, fromNote=False, event=None):
        """Open settings window"""
        fields=Setup(self, fromNote).getFields()
        if fields!=[]:      
            self.saveSettings()
            self.settings=getSettings()
            #self.draw()
            self.font=setFont()
            
    def setGender(self):
        """Save gender to settings and redraw"""
        self.datastring[18]=self.gender.get()
        self.saveSettings()
        self.draw()
        
    def setStatus(self):
        """Save status to settings and redraw"""
        self.datastring[21]=self.status.get()
        self.saveSettings()
        self.draw()
        
    def saveSettings(self):
        try:
            with open("data.ini", "w", encoding="utf-8") as datafile:
                for i in range(len(self.datastring)): datafile.write(self.datastring[i] + "\n")        
        except:
            print("settings saving failed")
        
        # Get font size from file
        try:
            self.fontsize=int(self.datastring[19])
        except:
            mb.showwarning("Внимание", "Проверьте размер шрифта в настройках!")
        
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
            #try:        
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
            self.student=student
            self.checkBrackets()
            result=True
            #except:
            #    mb.showerror("Ошибка", "Ошибка загрузки базы данных!")                
        return result
        
    def checkBrackets(self):
        """Check if there is technical data in brackets, add if none"""
        for student in self.student:
            if "{" not in student[0]:
                student[0]=student[0]+"{б+}"

    def save(self):
        """Save and backing up student list"""                
        limit=int(self.datastring[16])
        #self.student=sorted(self.student, key=lambda student: student[0])
        
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
        
    def wipe(self):
        if mb.askyesno("Очистка", "Вы уверены, что хотите удалить всех учащихся? Это действие можно будет отменить только путем импорта резервной копии (если есть)!")==True:            
            self.student=[]
            self.save()
            self.draw()
        
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
            except: print("can't check new version")
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
        files.append("easygui_mod.py")
        files.append("win.ini")
        for file in files:
            if os.path.exists(file): os.remove(file)
            
    def tip(self, text="test", time=2000):
        """Show self-destructing notification"""           
        label=tk.Label(self.master, fg="seagreen", font="(), 8")
        label.grid(column=0, row=3, sticky="ws")
        label["text"]=text
        label.after(time, lambda: label.grid_remove())
        
    def contextMenu(self, e=None):
        """Context menu on fields"""
        menu = tk.Menu(self.master, tearoff=0)
        menu.add_command(label="Вырезать", command=lambda: e.widget.event_generate("<<Cut>>"))
        menu.add_command(label="Копировать", command=lambda: e.widget.event_generate("<<Copy>>"))
        menu.add_command(label="Вставить", command=lambda: e.widget.event_generate("<<Paste>>"))
        menu.add_command(label="Удалить", command=lambda: e.widget.event_generate("<<Clear>>"))
        menu.add_separator()
        menu.add_command(label="Выделить все", command=lambda: e.widget.event_generate("<<SelectAll>>"))
        menu.tk.call("tk_popup", menu, e.x_root, e.y_root)
        
# Launch interface
app=Root()
app.mainloop()