import os
import sys
import time

# Try to import the Python Image Library.  If it doesn't exist, only .gif images are supported.
try:
    from PIL import Image as PILImage
    from PIL import ImageTk as PILImageTk
except:
    pass

from tkinter import *
from tkinter import ttk
import tkinter.filedialog as tk_FileDialog
from io import StringIO

def getWinFonts():
    """Try to get a nice font on Windows as default, return first font or Courier if none found"""
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
    return fonts

def getFont():
    try:
        with open("data.ini", "r", encoding="utf-8") as file:
            datastring = [line.rstrip() for line in file]
        font=int(datastring[19])
    except: font=9
    return font

myFont=getWinFonts()[0]
PROPORTIONAL_FONT_FAMILY = (myFont)
MONOSPACE_FONT_FAMILY = (myFont)
PROPORTIONAL_FONT_SIZE = 9
MONOSPACE_FONT_SIZE = 9  
TEXT_ENTRY_FONT_SIZE = 9 

STANDARD_SELECTION_EVENTS = ["Return", "Button-1", "space"]

#-------------------------------------------------------------------
# multenterbox
#-------------------------------------------------------------------

def multenterbox(msg="Fill in values for the fields."
                 , title=" "
                 , fields=()
                 , values=()
                 , neutralButton=False):
    return __multfillablebox(msg, title, fields, values, None, neutralButton=neutralButton)


def bindArrows(widget):

    widget.bind("<Down>", tabRight)
    widget.bind("<Up>", tabLeft)

    widget.bind("<Right>", tabRight)
    widget.bind("<Left>", tabLeft)


def tabRight(event):
    boxRoot.event_generate("<Tab>")


def tabLeft(event):
    boxRoot.event_generate("<Shift-Tab>")

#-----------------------------------------------------------------------
# __multfillablebox
#-----------------------------------------------------------------------
def __multfillablebox(msg="Fill in values for the fields."
                      , title=" "
                      , fields=()
                      , values=()
                      , mask=None
                      , neutralButton=False):
    global boxRoot, __multenterboxText, __multenterboxDefaultText, cancelButton, entryWidget, okButton

    choices = ["Ввод (Enter)", "Отмена (Escape)"]
    if len(fields) == 0:
        return None

    fields = list(fields[:])  # convert possible tuples to a list
    values = list(values[:])  # convert possible tuples to a list

    #TODO RL: The following seems incorrect when values>fields.  Replace below with zip?
    if len(values) == len(fields):
        pass
    elif len(values) > len(fields):
        fields = fields[0:len(values)]
    else:
        while len(values) < len(fields):
            values.append("")

    boxRoot = Tk()

    w_size = 470
    h_size = 200
    ws_size = boxRoot.winfo_screenwidth()
    hs_size = boxRoot.winfo_screenheight()
    x_size = (ws_size/2) - (w_size/2)
    y_size = (hs_size/2) - (h_size/2)
    #rootWindowPosition = "+%d+%d" % (x_size/1.25, y_size/2)
    rootWindowPosition = "+30+30"
    
  
    boxRoot.geometry(rootWindowPosition)
    boxRoot.minsize(w_size, h_size)
    boxRoot.protocol('WM_DELETE_WINDOW', __multenterboxCancel)
    boxRoot.title(title)
    boxRoot.iconname('Dialog')
    boxRoot.bind("<Escape>", __multenterboxCancel)
    if os.name=="nt": boxRoot.iconbitmap('icon.ico')


    # -------------------- put subframes in the boxRoot --------------------
    messageFrame = ttk.Frame(master=boxRoot)
    messageFrame.pack(side=TOP, fill=BOTH)
    

    #-------------------- the msg widget ----------------------------
    messageWidget = Message(messageFrame, width="5.5i", text=msg)
    messageWidget.configure(font=(PROPORTIONAL_FONT_FAMILY, PROPORTIONAL_FONT_SIZE))
    
    messageWidget.pack(side=TOP, expand=1, fill=BOTH, padx='3m', pady='3m')

    global entryWidgets
    entryWidgets = list()

    lastWidgetIndex = len(fields) - 1

    for widgetIndex in range(len(fields)):
        argFieldName = fields[widgetIndex]
        argFieldValue = values[widgetIndex]
        entryFrame = ttk.Frame(master=boxRoot)
        entryFrame.pack(side=TOP, fill=BOTH)

        labelWidget = ttk.Label(entryFrame, text=argFieldName)
        labelWidget.pack(side=LEFT, padx="1m", pady="1m")
        style = ttk.Style()
        style.configure('my.TButton', font=('', 8))
        if "выступление" in argFieldName:
            def mainToday():
                entryWidgets[1].delete(0,END)
                entryWidgets[1].insert(0, time.strftime("%d.%m", time.localtime()) + "." + str(int(time.strftime("%Y", time.localtime()))-2000))
            def mainNever():
                entryWidgets[1].delete(0,END)
                entryWidgets[1].insert(0, "00.00.00")
            never1 = ttk.Button(entryFrame, text="Никогда", style='my.TButton', command=mainNever)
            never1.pack(side=RIGHT, anchor="e", padx="1m")
            today1 = ttk.Button(entryFrame, text="Сегодня", style='my.TButton', command=mainToday)
            today1.pack(side=RIGHT, anchor="e", padx="1m")
            entryWidget = ttk.Entry(entryFrame, width=9)
        elif "помощь" in argFieldName:
            def helpToday():
                entryWidgets[2].delete(0,END)
                entryWidgets[2].insert(0, time.strftime("%d.%m", time.localtime()) + "." + str(int(time.strftime("%Y", time.localtime()))-2000))
            def helpNever():
                entryWidgets[2].delete(0,END)
                entryWidgets[2].insert(0, "00.00.00")
            never2 = ttk.Button(entryFrame, text="Никогда", style='my.TButton', command=helpNever)
            never2.pack(side=RIGHT, padx="1m")
            today2 = ttk.Button(entryFrame, text="Сегодня", style='my.TButton', command=helpToday)
            today2.pack(side=RIGHT, padx="1m")
            entryWidget = ttk.Entry(entryFrame, width=9)
        elif "Имя" in argFieldName:
            def toClip():
                content=entryWidgets[0].get()
                boxRoot.clipboard_clear()
                boxRoot.clipboard_append(content)
            clip = ttk.Button(entryFrame, text="В буфер", style='my.TButton', command=toClip)
            #clip.pack(side=RIGHT, padx="1m")
            entryWidget = ttk.Entry(entryFrame, width=50)
        else: entryWidget = ttk.Entry(entryFrame, width=50)
        
        entryWidgets.append(entryWidget)
        entryWidget.configure(font=(PROPORTIONAL_FONT_FAMILY, TEXT_ENTRY_FONT_SIZE))
        entryWidget.pack(side=RIGHT, padx="1m")
        
        def standardMenu(e):
            conMenu.entryconfigure("Вырезать", command=lambda: e.widget.event_generate("<<Cut>>"))
            conMenu.entryconfigure("Копировать", command=lambda: e.widget.event_generate("<<Copy>>"))
            conMenu.entryconfigure("Вставить", command=lambda: e.widget.event_generate("<<Paste>>"))
            conMenu.entryconfigure("Удалить", command=lambda: e.widget.event_generate("<<Clear>>"))
            conMenu.entryconfigure("Выделить все", command=lambda: e.widget.event_generate("<<SelectAll>>"))              
            conMenu.tk.call("tk_popup", conMenu, e.x_root, e.y_root)
        entryWidget.bind("<Button-3>", standardMenu)

        #bindArrows(entryWidget)

        entryWidget.bind("<Return>", __multenterboxGetText)
        entryWidget.bind("<Escape>", __multenterboxCancel)        

        # for the last entryWidget, if this is a multpasswordbox,
        # show the contents as just asterisks
        if widgetIndex == lastWidgetIndex:
            if mask:
                entryWidgets[widgetIndex].configure(show=mask)

        # put text into the entryWidget
        entryWidgets[widgetIndex].insert(0, argFieldValue)
        widgetIndex += 1
        
    #Message(text="123").pack(side=BOTTOM)

    # ------------------ ok button -------------------------------
    buttonsFrame = Frame(master=boxRoot)
    buttonsFrame.pack(side=BOTTOM, fill=BOTH)
    #buttonsFrame.grid(column=0, row=10)

    okButton = ttk.Button(buttonsFrame, takefocus=1, text="OK (Enter)")
    bindArrows(okButton)
    okButton.pack(expand=1, side=LEFT, padx='3m', pady='3m', ipadx='2m', ipady='1m')

    # for the commandButton, bind activation events to the activation event handler
    commandButton = okButton
    handler = __multenterboxGetText
    for selectionEvent in STANDARD_SELECTION_EVENTS:
        commandButton.bind("<%s>" % selectionEvent, handler)
        
    # ------------------ delete button -------------------------------
    if neutralButton==True:
        deleteButton = ttk.Button(buttonsFrame, takefocus=1, text="Удалить")
        bindArrows(deleteButton)
        #deleteButton.pack(expand=1, side=LEFT, padx='3m', pady='3m', ipadx='2m', ipady='1m')

        # for the commandButton, bind activation events to the activation event handler
        commandButton = deleteButton
        handler = __multenterboxDelete
        for selectionEvent in STANDARD_SELECTION_EVENTS:
            commandButton.bind("<%s>" % selectionEvent, handler)


    # ------------------ cancel button -------------------------------
    cancelButton = ttk.Button(buttonsFrame, takefocus=1, text="Отмена (Escape)")
    bindArrows(cancelButton)
    cancelButton.pack(expand=1, side=LEFT, padx='3m', pady='3m', ipadx='2m', ipady='1m')

    # for the commandButton, bind activation events to the activation event handler
    commandButton = cancelButton
    handler = __multenterboxCancel
    for selectionEvent in STANDARD_SELECTION_EVENTS:
        commandButton.bind("<%s>" % selectionEvent, handler)

    # Context menu

    conMenu = Menu(entryFrame, tearoff=0)
    conMenu.add_command(label="Вырезать")
    conMenu.add_command(label="Копировать")
    conMenu.add_command(label="Вставить")
    conMenu.add_command(label="Удалить")
    conMenu.add_separator()
    conMenu.add_command(label="Выделить все")   


    # ------------------- time for action! -----------------
    entryWidgets[0].focus_force()  # put the focus on the entryWidget
    boxRoot.mainloop()  # run it!

    # -------- after the run has completed ----------------------------------
    boxRoot.destroy()  # button_click didn't destroy boxRoot, so we do it now
    return __multenterboxText

#-----------------------------------------------------------------------
# __multenterboxGetText
#-----------------------------------------------------------------------
def __multenterboxGetText(event):
    global __multenterboxText

    __multenterboxText = list()
    for entryWidget in entryWidgets:
        __multenterboxText.append(entryWidget.get())
    boxRoot.quit()


def __multenterboxCancel(event=None):
    global __multenterboxText
    __multenterboxText = None
    boxRoot.quit()
    
def __multenterboxDelete(event):
    global __multenterboxText
    __multenterboxText = "delete"
    boxRoot.quit()

def KeyboardListener(event):
    global choiceboxChoices, choiceboxWidget
    key = event.keysym
    if len(key) <= 1:
        if key in string.printable:
            # Find the key in the list.
            # before we clear the list, remember the selected member
            try:
                start_n = int(choiceboxWidget.curselection()[0])
            except IndexError:
                start_n = -1

            ## clear the selection.
            choiceboxWidget.selection_clear(0, 'end')

            ## start from previous selection +1
            for n in range(start_n + 1, len(choiceboxChoices)):
                item = choiceboxChoices[n]
                if item[0].lower() == key.lower():
                    choiceboxWidget.selection_set(first=n)
                    choiceboxWidget.see(n)
                    return
            else:
                # has not found it so loop from top
                for n, item in enumerate(choiceboxChoices):
                    if item[0].lower() == key.lower():
                        choiceboxWidget.selection_set(first=n)
                        choiceboxWidget.see(n)
                        return

                # nothing matched -- we'll look for the next logical choice
                for n, item in enumerate(choiceboxChoices):
                    if item[0].lower() > key.lower():
                        if n > 0:
                            choiceboxWidget.selection_set(first=(n - 1))
                        else:
                            choiceboxWidget.selection_set(first=0)
                        choiceboxWidget.see(n)
                        return

                # still no match (nothing was greater than the key)
                # we set the selection to the first item in the list
                lastIndex = len(choiceboxChoices) - 1
                choiceboxWidget.selection_set(first=lastIndex)
                choiceboxWidget.see(lastIndex)
                return
