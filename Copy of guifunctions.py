

import tkinter as tk
import threading
from functions import *
import time




def createlistbox(root,row,col):
       
        listbox = Listbox(root, font=("Helvetica", 9))
        listbox.grid(row=row, column=col, padx='10', pady='10',sticky=W+E+N+S)        
        return listbox    

def addinfo(lb, info):
    lb.insert('1.0',"\n")
    lb.insert('1.0',info)

def createtextarea(window,row,col,title,width):
        
        frame = LabelFrame(window, text="INFO", font=('Helvetica', 8, 'bold'), bg='cornsilk3')
        frame.grid(row=row, column=col, columnspan=6,pady='10')
        
        textarea = Text(frame, font=("Helvetica", 10), width='50', height='50')
        textarea.grid(row=0, column=0, padx='5', pady='5')
        textarea.config(bg='white')

        return textarea
       
def addtotextarea(textarea,info):

    lock = threading.Lock()

    def addinfo(textarea, info):
        textarea.insert('1.0',"\n")
        textarea.insert('1.0',info)

    
    lock.acquire()
    try:
        addinfo(textarea,info)


    finally:
        lock.release()

def createlabel(window,text,row,col,fs=8):
    infolabel = Label(window, text=text, justify=LEFT,font=("Helvetica", fs),bg='white')
    infolabel.grid(row=row,   column = col, padx='5',pady='2', sticky=W+E )
    return infolabel



def create_table_2(window,text1,text2,row):
    col1 = createlabel(window,text1,row,0)
    col2 = createlabel(window,text2,row,1)
    out = {'col1':col1, 'col2':col2 }
    return out


def create_table_4(window,text1,text2,text3,text4,row):
    col1 = createlabel(window,text1,row,0)
    col2 = createlabel(window,text2,row,1)
    col3 = createlabel(window,text3,row,2)
    col4 = createlabel(window,text4,row,3)
    out = {'col1':col1, 'col2':col2 , "col3":col3,'col4':col4}
    return out



def createorderframe(window,title,roww,col):
        lframe = LabelFrame(window, text=title, font=('Helvetica', 8, 'bold'), bg='cornsilk3')
        lframe.grid(row=roww, column=col, pady='10',padx='50',sticky=W+E+N+S)


        objframe =Frame(lframe, relief=SUNKEN )
        objframe.grid(row=0, column=1, pady='10',padx='10',sticky=W+E+N+S)
        listbox = createlistbox(lframe,0,2)

        exchangeinfo=create_table_2(objframe,'EXCHANGE',"---",0)
        
        symbol=create_table_2(objframe,'SYMBOL','---',1)
        balance = create_table_2(objframe,'BALANCE','0.0000',2)
        

        sellbutton =Button(objframe,text="SELL")
        sellbutton.grid(row=3,   column = 0, ipadx='5',  ipady='5', padx='10',pady='10', sticky=W+E)

        sellentry = Entry(objframe, width=10,font=('Helvetica', 14, 'bold'))
        sellentry.grid(row=3,column=1, ipadx='5',  ipady='5', padx='10',pady='10', sticky=W+E)
        sellentry.insert(0, "0.00")

        buybutton =Button(objframe,text="BUY")
        buybutton.grid(row=4,   column = 0, ipadx='5',  ipady='5', padx='10',pady='10', sticky=W+E)

        buyentry = Entry(objframe, width=10, font=('Helvetica', 14, 'bold'))
        buyentry.grid(row=4,column=1, ipadx='5',  ipady='5', padx='10',pady='10', sticky=W+E)        
        buyentry.insert(0, "0.00")

        withdrawbutton =Button(objframe,text="WD DOGE")
        withdrawbutton.grid(row=5,   column = 0, ipadx='5',  ipady='5', padx='10',pady='10', sticky=W+E)

        info ={'listbox':listbox, 'exchange':exchangeinfo,   'symbol':symbol, 'balance':balance, 'sellbutton':sellbutton, 'buybutton':buybutton, 'withdrawbutton':withdrawbutton, 'buyentry':buyentry, 'sellentry':sellentry}
        return info


