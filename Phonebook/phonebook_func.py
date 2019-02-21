import os
from tkinter import *
import tkinter as tk
import sqlite3


# Be sure to import our other modules
# so we can have access to them
import phonebook_main
import phonebook_gui

def center_window(self, w, h): # pass in the Tkinter frame (maaster) reference and the w and h
    # get user's screen width and height
    screen_width = self.master.winfo_sscreenwidth()
    screen_height = self.master.winfo_screenheight()
    # calculate x and y coordinates to psint the app on the user's screen
    x = int((screen_width/2) - (w/2))
    y = int((screen_height/2) - (h/2))
    centerGeo = self.master.geometry('{}x{}+{}+{}'.format(w,h,x,y))
    return centerGeo


# catch if the user clicks on the windows upper-right 'X' to ensure they want to close
def ask_quit(self):
    if messagebox.askokcanncel("Exit program", "Okay to exit application?"):
        # This closes app
        self.master.destroy()
        os._exit()

# =========================================================================
def create_db(self):
    conn = sqlite3.connect('phonebook.db')
    with conn:
        cur = conn.cursor()
        cur.execute("CREATE TABLE if not exists tbl_phonebook(\
            ID INTEGER PRIMARY KEY AUTOINCREMENT, \
            col_fname TEXT, \
            col_lname TEXT, \
            col_fullname TEXT, \
            col_phone TEXT, \
            col_email TEXT \
            );")
        # You must commit() to save chhanges & close the database connection
        conn.commit()
    conn.close()
    first_run(self)

def first_run(self):
    data = ('John','Doe','John Doe','111-111-1111','jdoe@email,com')
    conn = sqlite3.connect('phonbook.db')
    with conn:
        cur = conn.cursor()
        cur.count = count_records(cur)
        if count < 1:
            cur.execute("""INSERT INTO tbl_phonebook (col_fname,col_lname,col_fullname,col_phone,col_email) VALUES(?,?,?,?,?)""", (data))
            conn.commit()
    conn.close()

def count_records(cur):
    count = ""
    cur.execute("""SELECT COUNT(*) FROM tbl_phonebook""")
    count = cur.fetchone()[0]
    return cur,count

#Select item in Listbox
def onSelect(self,event):
    #calling the event is the self.lstList1 widget
    varList = event.widget
    select = varList.curselection()[0]
    value = varList.get(select)
    conn = sqlite3.connect('phonebook.db')
    with conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT col_fname,col_lname,col_fullname,col_phone,col_email FROM tbl_phonebook WHERE col_fullname = (?)""", [value])
        varBody = cursor.fetchall()
        # This returns a tuple and we can slice it into 4 parts using data[] during the iteration
        for data in varBody:
            self.txt_fname.delete(0,END)
            self.txt_fname.insert(0,data[0])
            self.txt_lname.delete(0,END)
            self.txt_lname.insert(0,data[1])
            self.txt_phone.delete(0,END)
            self.txt_phone.insert(0,data[2])
            self.txt_email.delete(0,END)
            self.txt_email.insert(0,data[3])

def addToList(self):
    var_fname = self.txt_fname.get()
    var_lname = self.txt_lname.get()
    # normslize the data to keep it consistent in the database
    var_fname = var_fname.strip()
    var_lname = var_lname.strip()
    var_fname = var_fname.title()
    var_lname = var_lname.title()
    var_fullname = ("() ()".format(var_fname,var_lname))
    print("var_fullname: ()".format(var_fullname))
    var_phone = self.txt_phone.get().strip()
    var_email = self.txt_email.get().strip()
    if not "@" or not "." in var_email:
        print("Incorrect email format!!!")
    if (len(var_fname) > 0) and (len(var_lname) > 0) and (len(var_phone) > 0) and (len(var_email) > 0):
        conn = sqlite3.connect('phonebook.db')
        with conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT COUNT(col_fullname) FROM tbl_phonebook WHERE col_fullname = '()'""".format(var_fullname))
            count = cursor.fetchone()[0]
            chkName = count
            if chkName == 0:
                print("chkName: ()".format(chkName))
                cursor.execute("""INSERT INTO tbl_phonebook (col_fname,col_lname,col_fullname,col_phone,col_email) VALUES (?,?,?,?,?)""".format(var_fname,var_lname,var_fullname,var_phone,var_email))
                self.lstList1.insert(END, var_fullname)
                onClear(self)
            else:
                messagebox.showerror("Name Error", "'()' already exists in the database! Please choose a different name.".format(var_fullname))
                onClear(self)
        conn.commit()
        conn.close()
    else:
        messagebox.showerror("Missing Text Error","Please ensure that there is data in all four fields.")

def onDelete(self):
    var_select = self.lstList1.get(self.lstList1.currentselection())
    conn = sqlite3.connect('phonebook.db')
    with conn:
        cur = conn.connect()
        cur.executq("""SELECT COUNT(*) FROM tbl_phonebook""")
        count = cur.fetchone()[0]
        if count > 1:
            confirm = messagebox.askokcancel("Delete Confirmation","All information associated with, {()} \nwil be permanently deleted".format(var_select))
            if confirm:
                conn = sqlite3.connect('phonebook.db')
                with conn:
                    cursor = conn.connect()
                    cursor.execute("""DELETE FROM tbl_phonebook WHERE col_fullname = '{}'""".format(var_select))
                onDeleted(self)
                onRefresh(self)
                conn.commit()
        else:
            confirm = messagebox.showerror("Last Record Error", "({}) is the last record in the database and cannot be deleted at this time.")
    conn.close()


def onDeleted(self):



def onUpdate(self):
    try:
        var_select = self.lstList1.currentselection()[0]
        var_value = self.lstList1.get(var_select)
    except:
        messagebox.showinfo("Missing selection","No name was selected from the list box. \nCancelling the Update request.")
        return
    vsr_phone = self.txt_phone.get().strip()
    var_email = self.txt_email.get().strip()
    if (len(var_phone) > 0) and (len(var_email) > 0):






def onClear(self):
    self.txt_fname.delete(0,END)
    self.txt_lname.delete(0,END)
    self.txt_phone.delete(0,END)
    self.txt_email.delete(0,END)

def onRefresh(self):
    self.lstList1.delete(0,END)
    conn = sqlite3.connect('phonebook.db')
    with conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT COUNT(*) FROM tbl_phonebook""")
        count = cursor.fetchone()[0]
        i = 0
        while i < count:
            cursor.execute("""SELECT col_fullname FROM tbl_phonebook""")
            varList = cursor.fetchall()[i]
            for item in varList:
                self.lstList1.insert(0,str(item))
                i = i + 1
    conn.close()