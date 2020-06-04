from tkinter import *
from tkinter import PhotoImage
from tkinter import ttk
import tkinter as tk
import pandas as pd
from PIL import Image, ImageTk
import sqlite3
import math
from tkinter import messagebox
from datetime import date
import os
import xlsxwriter
from xlsxwriter.workbook import Workbook

window2=Tk()
f1=Frame(window2,bg="black")
f2=Frame(window2,bg="black")
f3=Frame(window2,bg="black")
f4=Frame(window2,bg="black")

def swap(frame):
	frame.tkraise()
for frame in(f1,f2,f3,f4):
	frame.place(x=0,y=0,width=1000,height=700)
window2.geometry('1000x700+100+100')
window2.resizable(FALSE,FALSE)
f1.tkraise()
label3=Label(f1,text="Corona-Status",font=("arial",20,"bold"),bg="slategrey",fg="black",relief=SUNKEN)
label3.pack(side=TOP,fill=X)


#=============GiffAnimationPart==========================================
class AnimatedGIF(Label, object):
    def __init__(self, master, path, forever=True):
        self._master = master
        self._loc = 0
        self._forever = forever

        self._is_running = False

        im = Image.open(path)
        self._frames = []
        i = 0
        try:
            while True:
                photoframe = ImageTk.PhotoImage(im.copy().convert('RGBA'))
                self._frames.append(photoframe)

                i += 1
                im.seek(i)
        except EOFError: pass
        
        self._last_index = len(self._frames) - 1

        try:
            self._delay = im.info['duration']
        except:
            self._delay = 100

        self._callback_id = None

        super(AnimatedGIF, self).__init__(master, image=self._frames[0])

    def start_animation(self, frame=None):
        if self._is_running: return

        if frame is not None:
            self._loc = 0
            self.configure(image=self._frames[frame])

        self._master.after(self._delay, self._animate_GIF)
        self._is_running = True

    def stop_animation(self):
        if not self._is_running: return

        if self._callback_id is not None:
            self.after_cancel(self._callback_id)
            self._callback_id = None

        self._is_running = False

    def _animate_GIF(self):
        self._loc += 1
        self.configure(image=self._frames[self._loc])

        if self._loc == self._last_index:
            if self._forever:
                self._loc = 0
                self._callback_id = self._master.after(self._delay, self._animate_GIF)
            else:
                self._callback_id = None
                self._is_running = False
        else:
            self._callback_id = self._master.after(self._delay, self._animate_GIF)

    def pack(self, start_animation=True, **kwargs):
        if start_animation:
            self.start_animation()

        super(AnimatedGIF, self).pack(**kwargs)

    def grid(self, start_animation=True, **kwargs):
        if start_animation:
            self.start_animation()

        super(AnimatedGIF, self).grid(**kwargs)
        
    def place(self, start_animation=True, **kwargs):
        if start_animation:
            self.start_animation()

        super(AnimatedGIF, self).place(**kwargs)
        
    def pack_forget(self, **kwargs):
        self.stop_animation()

        super(AnimatedGIF, self).pack_forget(**kwargs)

    def grid_forget(self, **kwargs):
        self.stop_animation()

        super(AnimatedGIF, self).grid_forget(**kwargs)
        
    def place_forget(self, **kwargs):
        self.stop_animation()

        super(AnimatedGIF, self).place_forget(**kwargs)

if __name__ == "__main__":
    l = AnimatedGIF(f1, "3.gif")
    l.pack()

#====================SavingDataInDatabase=================================
def createdb():
    conn = sqlite3.connect('corona.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS corona_status (id INTEGER unique primary key autoincrement, Age INTEGER, Gender TEXT, Postal_Code INTEGER , Dry_Cough TEXT,Fever TEXT, Fatigue TEXT, Nasal_Congestion TEXT, Sore_Throat TEXT, Diarrhoea TEXT,Breath TEXT,Temperature INTEGER, Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL)")
    conn.commit()
    conn.close()
createdb()

def save_record():
    conn=sqlite3.connect("corona.db")
    c=conn.cursor()
    uage=age_entry.get()
    upost=postal_entry.get()
    uppost=upost.upper()
    utemp=temp_entry.get()
    if uppost == "":
        messagebox.showerror("Error","Please Enter your Postal Code")
    else:
        c.execute("INSERT INTO corona_status (Age,Gender,Postal_Code,Dry_Cough,Fever,Fatigue,Nasal_Congestion,Sore_Throat,Diarrhoea,Breath,Temperature) VALUES(?,?,?,?,?,?,?,?,?,?,?) ",(uage,gender.get(),uppost,dry.get(),fever.get(),fatigue.get(),nasal.get(),sore.get(),diarrhoea.get(),breath.get(),utemp))
    conn.commit()
    conn.close()
    age_entry.delete(0,END)
    postal_entry.delete(0,END)
    temp_entry.delete(0,END)
    messagebox.showinfo("Saved","Data has been saved successfully.")
    
#====================ExportingToExcel========================================================

def export():
    if not os.path.exists('./Excel_import'):
        os.makedirs('./Excel_import')
    conn=sqlite3.connect("corona.db")
    c=conn.cursor()
    c.execute("SELECT * FROM corona_status")
    data = c.fetchall()
    time=str(date.today())
    df=pd.DataFrame(data, columns=['Sl. No.', 'Age', 'Gender', 'Postal Code', 'Dry Cough','Fever','Fatigue','Nasal Congestion','Sore Throat','Diarrhoea','Shortness of Breath','Temperature','Date'])
    datatoexcel = pd.ExcelWriter("./Excel_import/Corona Record"+time+".xlsx", engine='xlsxwriter')
    df.to_excel(datatoexcel, index= False, sheet_name = "Sheet1")
    worksheet = datatoexcel.sheets['Sheet1']
    worksheet.set_column('A:A', 5)
    worksheet.set_column('B:B', 8)
    worksheet.set_column('C:C', 15)
    worksheet.set_column('D:D', 15)
    worksheet.set_column('E:E', 20)
    worksheet.set_column('F:F', 20)
    worksheet.set_column('G:G', 20)
    worksheet.set_column('H:H', 20)
    worksheet.set_column('I:I', 20)
    worksheet.set_column('J:J', 20)
    worksheet.set_column('K:K', 20)
    worksheet.set_column('L:L', 20)
    worksheet.set_column('M:M', 20)
    datatoexcel.save()
    messagebox.showinfo("Success","Excel File Generated Successfully.")
#====================ListView===========================================
class Product:
    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result
    
    db_name = 'corona.db'
    def __init__(self, window2):
        self.Detail_Frame=Frame(f3,bd=4,relief=RIDGE,bg="white")
        self.Detail_Frame.pack(fill=X,expand=1)
        self.scroll_x=Scrollbar(self.Detail_Frame,orient=HORIZONTAL)
        self.scroll_y=Scrollbar(self.Detail_Frame,orient=VERTICAL)
        self.tree = ttk.Treeview(self.Detail_Frame,columns=('1','2','3','4','5','6','7','8','9','10','11','12','13'),xscrollcommand=self.scroll_x.set,yscrollcommand=self.scroll_y.set)
        self.scroll_x.pack(side=BOTTOM,fill=X)
        self.scroll_y.pack(side=RIGHT,fill=Y)
        self.scroll_x.config(command=self.tree.xview)
        self.scroll_y.config(command=self.tree.yview)
        self.tree.place(x=0,y=0)
        self.tree.heading('#1', text = 'Sl. No.')
        self.tree.heading('#2', text = 'Age')
        self.tree.heading('#3', text = 'Gender')
        self.tree.heading('#4', text = 'Postal Code')
        self.tree.heading('#5', text = 'Dry Cough')
        self.tree.heading('#6', text = 'Fever')
        self.tree.heading('#7', text = 'Fatigue')
        self.tree.heading('#8', text = 'Nasal Congestion')
        self.tree.heading('#9', text = 'Sore Throat')
        self.tree.heading('#10', text = 'Diarrhoea')
        self.tree.heading('#11', text = 'Shortness of Breath')
        self.tree.heading('#12', text = 'Temperature')
        self.tree.heading('#13', text = 'Date')
        self.tree['show']='headings'
        self.tree.column("1",width=1)
        self.tree.column("2",width=1)
        self.tree.column("3",width=8)
        self.tree.column("4",width=15)
        self.tree.column("5",width=15)
        self.tree.column("6",width=10)
        self.tree.column("7",width=10)
        self.tree.column("8",width=30)
        self.tree.column("9",width=15)
        self.tree.column("10",width=10)
        self.tree.column("11",width=30)
        self.tree.column("12",width=15)
        self.tree.column("13",width=30)
        self.tree.pack(fill=X,expand=1)
        
        self.get_products()
    def get_products(self):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        query = 'SELECT * FROM corona_status'
        db_rows = self.run_query(query)
        for row in db_rows:
            self.tree.insert('', tk.END, values = row)
        


#===========ItemsInFrame2F2=============================================
label=Label(f2,text="Add Record",font=("arial",17,"bold"),bg="slategrey",fg="black",relief=SUNKEN)
label.pack(side=TOP,fill=X)

label=Label(f2,text='Age',font=("arial",15,'bold'),bg='slategrey',fg='white')
label.place(x=90,y=50)
label=Label(f2,text='Gender',font=("arial",15,'bold'),bg='slategrey',fg='white')
label.place(x=90,y=100)
label=Label(f2,text='Postal Code',font=("arial",15,'bold'),bg='slategrey',fg='white')
label.place(x=90,y=150)
label=Label(f2,text="               Symptoms              ",font=("arial",15,"bold"),bg="blue",fg="white",relief=SUNKEN)
label.place(x=90,y=200)
label=Label(f2,text='Dry Cough',font=("arial",15,'bold'),bg='slategrey',fg='white')
label.place(x=90,y=250)
label=Label(f2,text='Fever',font=("arial",15,'bold'),bg='slategrey',fg='white')
label.place(x=90,y=300)
label=Label(f2,text='Fatigue',font=("arial",15,'bold'),bg='slategrey',fg='white')
label.place(x=90,y=350)
label=Label(f2,text='Nasal Congestion',font=("arial",15,'bold'),bg='slategrey',fg='white')
label.place(x=90,y=400)
label=Label(f2,text='Sore Throat',font=("arial",15,'bold'),bg='slategrey',fg='white')
label.place(x=90,y=450)
label=Label(f2,text='Diarrhoea',font=("arial",15,'bold'),bg='slategrey',fg='white')
label.place(x=90,y=500)
label=Label(f2,text='Shortness of Breath',font=("arial",15,'bold'),bg='slategrey',fg='white')
label.place(x=90,y=550)
label=Label(f2,text='Temperature',font=("arial",15,'bold'),bg='slategrey',fg='white')
label.place(x=90,y=600)

age_entry=IntVar()
age_entry=ttk.Entry(f2,textvariable=age_entry)
age_entry.place(x=150,y=50,width=160)
age_entry.focus()
gender=StringVar()
gender=ttk.Combobox(f2,textvariable=gender,width=15,font=("arial",10),state='readonly')
gender['values']=("Female","Male","Other")
gender.place(x=190,y=100,width=160)
postal_entry=IntVar()
postal_entry=ttk.Entry(f2,textvariable=postal_entry)
postal_entry.place(x=230,y=150,width=160)
postal_entry.focus()
dry=StringVar()
dry=ttk.Combobox(f2,textvariable=dry,width=15,font=("arial",10),state='readonly')
dry['values']=("YES","NO")
dry.place(x=220,y=250,width=160)
fever=StringVar()
fever=ttk.Combobox(f2,textvariable=fever,width=15,font=("arial",10),state='readonly')
fever['values']=("YES","NO")
fever.place(x=170,y=300,width=160)
fatigue=StringVar()
fatigue=ttk.Combobox(f2,textvariable=fatigue,width=15,font=("arial",10),state='readonly')
fatigue['values']=("YES","NO")
fatigue.place(x=180,y=350,width=160)
nasal=StringVar()
nasal=ttk.Combobox(f2,textvariable=nasal,width=15,font=("arial",10),state='readonly')
nasal['values']=("YES","NO")
nasal.place(x=280,y=400,width=160)
sore=StringVar()
sore=ttk.Combobox(f2,textvariable=sore,width=15,font=("arial",10),state='readonly')
sore['values']=("YES","NO")
sore.place(x=220,y=450,width=160)
diarrhoea=StringVar()
diarrhoea=ttk.Combobox(f2,textvariable=diarrhoea,width=15,font=("arial",10),state='readonly')
diarrhoea['values']=("YES","NO")
diarrhoea.place(x=200,y=500,width=160)
breath=StringVar()
breath=ttk.Combobox(f2,textvariable=breath,width=15,font=("arial",10),state='readonly')
breath['values']=("YES","NO")
breath.place(x=300,y=550,width=160)
temp_entry=IntVar()
temp_entry=ttk.Entry(f2,textvariable=temp_entry)
temp_entry.place(x=250,y=600,width=160)
temp_entry.focus()

btn1=Button(f2,text="Save Record",bg='green',command=save_record)
btn1.place(x=30, y=650,width=450,height=30)
#============ButtonsInFrame1=============================================

btn1=Button(f1,text="Add Record",bg='slategrey',command=lambda:swap(f2))
btn1.place(x=820, y=60,width=150,height=30)

btn2=Button(f1,text="View",bg='slategrey',command=lambda:swap(f3))
btn2.place(x=820, y=150,width=150,height=30)

btn2=Button(f1,text="Export Excel",bg='slategrey',command=export)
btn2.place(x=820, y=240,width=150,height=30)

btn2=Button(f1,text="Developer",bg='slategrey',command=lambda:swap(f4))
btn2.place(x=820, y=330,width=150,height=30)

def destroy():
    window2.destroy()
btn2=Button(f1,text="Exit",bg='slategrey',command=destroy)
btn2.place(x=820, y=410,width=150,height=30)
#=============ItemsInFrame3================================================


label3=Label(f4,text="Developers Page",font=("arial",20,"bold"),bg="slategrey",fg="black",relief=SUNKEN)
label3.pack(side=TOP,fill=X)
label3=Label(f4,text="Project by Priti Shaw",font=("arial",12,"bold"),bg="slategrey",fg="black",relief=SUNKEN)
label3.pack(side=BOTTOM,fill=X)
label3=Label(f4,text="                    Help us uncover and predict the corona spread in your area.                    ",font=("arial",12,"bold"),bg="blue",fg="black",relief=SUNKEN)
label3.place(x=200,y=130)
label3=Label(f4,text="Regardeless if you are healthy or not, please take the survey.",font=("arial",12,"bold"),bg="blue",fg="black",relief=SUNKEN)
label3.place(x=260,y=160)
label3=Label(f4,text="For any Information Please Email at:      ",font=("arial",12,"bold"),bg="slategrey",fg="black",relief=SUNKEN)
label3.place(x=10,y=280)
label3=Label(f4,text="pd3459@srmist.edu.in",font=("arial",12,"bold"),bg="slategrey",fg="black",relief=SUNKEN)
label3.place(x=10,y=310)
label3=Label(f4,text="                      Thank You!                     ",font=("arial",12,"bold"),bg="blue",fg="black",relief=SUNKEN)
label3.place(x=380,y=500)



#============BackButtons===================================================
backf2=Button(f2,text="Back	",bg='red',fg='white',command=lambda:swap(f1))
backf2.place(x=3, y=40,width=60,height=30)
backf3=Button(f3,text="Back	",bg='red',fg='white',command=lambda:swap(f1))
backf3.place(x=3, y=40,width=60,height=30)
backf3=Button(f4,text="Back	",bg='red',fg='white',command=lambda:swap(f1))
backf3.place(x=3, y=40,width=60,height=30)

if __name__ == '__main__':
    application = Product(window2)
    window2.mainloop()
