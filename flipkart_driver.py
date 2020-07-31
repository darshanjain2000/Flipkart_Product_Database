import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import sqlite3
import time
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
from PIL import ImageTk, Image
from http.client import IncompleteRead

    

def Table(tablename):
    
    
    conn = sqlite3.connect('FLIPKART')
    curs = conn.cursor()
    try:
        curs.execute("create table "+tablename+" (ProductId int(3), Product_Name char(100), Price char(20), Rating real(5), Review_Title char(1000), Review_Text char(9999999))")
    except:
        l1.configure(text="Table Already Exists")
    
    conn.commit()
    conn.close()
    
def Drop(tablename):

    conn = sqlite3.connect('FLIPKART')
    curs = conn.cursor()
    try:
        curs.execute("drop table "+tablename)
    except:
        l1.configure(text="Table not found/deleted")
    
    conn.commit()
    conn.close()

    
    
def table_init():
    
    global count
    global tablename
    global prodname
    global tot_rec
    
    table = str(prev_search.get())
    tablename = table.replace(' ','')
    
    
    
    prodname = str(product_name.get()) 
    
    conn = sqlite3.connect('FLIPKART')
    curs = conn.cursor()
    try:
        curs.execute("select * from "+tablename+" where Product_Name = \""+prodname+"\"")
        rec = curs.fetchall()
        tot_rec = len(rec)
    except:
        messagebox.showerror("SQL ERROR", "Table Name Error")
    conn.commit()
    conn.close()
    
    if(tot_rec > 0):
        count = 1
    firstRec()
    
    l2.configure(text=str(count)+"/"+str(tot_rec))
    

def firstRec():
    global count
    global tablename
    global prodname
    global tot_rec
    
    if(count==0):
        messagebox.showerror("SQL ERROR", "No Records...")
        return
    
    conn = sqlite3.connect('FLIPKART')
    curs = conn.cursor()
    ins_rec = curs.execute("select * from "+tablename+" where Product_Name = \""+prodname+"\"") 
    first = curs.fetchone()
    name.set(first[1])
    price.set(first[2])
    rating.set(first[3])
    title.set(first[4])
    text.set(first[5])
    conn.close()
    count = 1
    l2.configure(text=str(count)+"/"+str(tot_rec))
    
def preRec():
    global count
    global tablename
    global prodname
    global tot_rec
    
    if(count==0):
        messagebox.showerror("SQL ERROR", "No Records...")
        return        
    conn = sqlite3.connect('FLIPKART')
    curs = conn.cursor()
    ins_rec = curs.execute("select * from "+tablename+" where Product_Name = \""+prodname+"\"")
    if(count==1):
        first = curs.fetchone()
    else:
        for i in range(1,count):
            first = curs.fetchone()
        count -= 1
    name.set(first[1])
    price.set(first[2])
    rating.set(first[3])
    title.set(first[4])
    text.set(first[5])
    conn.close()
    l2.configure(text=str(count)+"/"+str(tot_rec))
    
def nextRec():
    global count
    global tablename
    global prodname
    global tot_rec
    
    if(count==0):
        messagebox.showerror("SQL ERROR", "No Records...")
        return
    conn = sqlite3.connect('FLIPKART')
    curs = conn.cursor()
    ins_rec = curs.execute("select * from "+tablename+" where Product_Name = \""+prodname+"\"")
    if(tot_rec == 1):
        first = curs.fetchone()
    else:
        for i in range(1,count+1):
            first = curs.fetchone()
    if(count<tot_rec):
        first = curs.fetchone()
    else:
        count -= 1
    name.set(first[1])
    price.set(first[2])
    rating.set(first[3])
    title.set(first[4])
    text.set(first[5])
    conn.close()
    count += 1
    l2.configure(text=str(count)+"/"+str(tot_rec))
    
def lastRec():
    global count
    global tablename
    global prodname
    global tot_rec
    
    if(count==0):
        messagebox.showerror("SQL ERROR", "No Records...")
        return
    conn = sqlite3.connect('FLIPKART')
    curs = conn.cursor()
    ins_rec = curs.execute("select * from "+tablename+" where Product_Name = \""+prodname+"\"")
    if(tot_rec == 1):
        first = curs.fetchone()
    else:
        count = 0
        for i in range(1,tot_rec+1):
            first = curs.fetchone()
            count += 1
    name.set(first[1])
    price.set(first[2])
    rating.set(first[3])
    title.set(first[4])
    text.set(first[5])    
    conn.close()
    l2.configure(text=str(count)+"/"+str(tot_rec))
    
def addRec():
    global count
    global tablename
    global tot_rec
    
    conn = sqlite3.connect('FLIPKART')
    curs = conn.cursor()
    try:
        ins_rec=curs.execute('insert into '+tablename+' values (?, ?, ?, ?, ?)', (name.get(), price.get(), rating.get(), title.get(), text.get(),))
        conn.commit()
        conn.close()
        tot_rec += 1
        count = tot_rec
        l2.configure(text=str(count)+"/"+str(tot_rec))
        
    except:
        messagebox.showerror("SQL ERROR", "Value Error")
    
def delRec():
    global count
    global tablename
    global tot_rec
    
    if(count==0):
        messagebox.showerror("DELETE ERROR", "No Records...")
        return
    conn = sqlite3.connect('FLIPKART')
    curs = conn.cursor()
    try:
        ins_rec=curs.execute('delete from '+tablename+' where Review_Title=?',(title.get(),))
        conn.commit()
        conn.close()
        count = 1
        tot_rec -= 1
        firstRec()
    
    except:
        messagebox.showerror("SQL ERROR", "Value Not Found")
    
def updateRec():
    global tablename
    conn = sqlite3.connect('FLIPKART')
    curs = conn.cursor()
    try:
        ins_rec=curs.execute('update '+tablename+' set Product_Name=?,Price=?,Rating=?,Review_Title=?,Review_Text=? where Review_Title=?',(name.get(), price.get(), rating.get(), title.get(), text.get(),title.get(),))
        conn.commit()
        conn.close()
        count = 1
        firstRec()
    except:
        messagebox.showerror("SQL ERROR", "Value Not Found")

def searchRec():
    global tablename
    conn = sqlite3.connect('FLIPKART')
    curs = conn.cursor()
    try:
        ins_rec=curs.execute('select * from '+tablename+' where Review_Title like ?',(title.get(),))
        first = curs.fetchone()
        name.set(first[1])
        price.set(first[2])
        rating.set(first[3])
        title.set(first[4])
        text.set(first[5])
        conn.close()
    except:
        messagebox.showerror("SQL ERROR", "Value Not Found")



    
def Fetch_Data():
    
    service = 'https://www.flipkart.com/search?'
    search = str(flipkart_search.get())

    parms = dict()
    parms['q'] = search
    url = service + urllib.parse.urlencode(parms)
    
    tablename = search.replace(' ','') 

    try:
        
        l1.configure(text="Please Wait...")
        
        listurl = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(listurl, 'html.parser')

        prodname = soup.findAll("div",{"class":"_3wU53n"})
        prodprice = soup.findAll("div",{"class":"_2rQ-NK"})
        prodrating = soup.findAll("span",{"class":"_2_KrJI"})
        flipkart = 'https://www.flipkart.com'
        prodlinks = soup.findAll("a",{"class":"_31qSD5"})
        prodcount = len(prodname)
        prodId = []
        
        
        
        Table(tablename)



        for i in range(0,prodcount):

            pid = i+1;
            pname = prodname[i].text
            pprice = prodprice[i].text
            prating = float(prodrating[i].text)
            
            plink = flipkart + prodlinks[i]['href']
            
            productpage = urllib.request.urlopen(plink).read()
            soup1 = BeautifulSoup(productpage, 'html.parser')
            
            reviewTitle = soup1.findAll("p",{"class":"_2xg6Ul"})
            reviewText = soup1.findAll("div",{"class":"qwjRop"})
            reviewscount = len(reviewTitle)
            
            
            for j in range(0,reviewscount):
                
                rtitle = reviewTitle[j].text.strip().encode('ascii', 'ignore').decode('ascii')
                rtext = reviewText[j].text.replace('READ MORE','').strip().encode('ascii', 'ignore').decode('ascii')
                
                conn = sqlite3.connect('FLIPKART')
                curs = conn.cursor()
                curs.execute("insert into "+tablename+" values(?,?,?,?,?,?)",(pid,pname,pprice,prating,rtitle,rtext))
                conn.commit()
                conn.close()
                
    
        l1.configure(text = search+" added successfully")
        
    except IncompleteRead:
        
        l1.configure(text = "IncompleteRead Error, Please try adding again")
        Drop(tablename)
        
    except:
        l1.configure(text="Error")
        Drop(tablename)
        
    
def plot():
    

    try:
        tabname = str(searchplot.get()).replace(' ','')
        conn = sqlite3.connect('FLIPKART')
        df = pd.read_sql_query("select * from "+tabname, conn)
        conn.commit()
        conn.close()
        fig_dims = (10,10)
        fig, ax = plt.subplots(figsize=fig_dims)
        graph_plot = sns.barplot(y="Product_Name", x="Rating",  data=df, ax=ax)
        graph_plot.figure.savefig('./temp_plot.png')
    
        graph_display = tk.Toplevel(win)
        load = Image.open("temp_plot.png")
        render = ImageTk.PhotoImage(load)
        img = tk.Label(graph_display, image=render)
        img.image = render
        img.place(x=0, y=0)
        img.pack(side = "bottom", fill = "both", expand = "yes")
    
    except:
        messagebox.showerror("SQL ERROR", "Table Not Found")
    

    
# GUI
    

win = tk.Tk()
win.title("Review Analysis System")
win.geometry("700x600")

tab_parent = ttk.Notebook(win)

tab1 = ttk.Frame(tab_parent)
tab2 = ttk.Frame(tab_parent)
tab3 = ttk.Frame(tab_parent)

tab_parent.add(tab1, text="Add Products")
tab_parent.add(tab2, text="Modify Products")
tab_parent.add(tab3, text="Search Analysis")





# TAB 1

l1a = Label(tab1,text = "Flipkart Scraper",font=("cambria",15,"bold"), width=50, anchor="c")
l1a.grid(row=1,column=1,columnspan=4)

searchlabel = Label(tab1,text="Search: ",font=("cambria",15,"bold"),bg="blue",fg="white", width=8, anchor="w")
searchlabel.grid(row=2,column=1)
flipkart_search = StringVar()
searchentry = Entry(tab1,textvariable = flipkart_search,width = 45,font=("cambria",15,"bold"),bg="orange")
searchentry.grid(row=2,column=2,columnspan=3)


b1 = Button(tab1, width="8", text="Enter", command=Fetch_Data, font=("cambria",15,"bold"))
b1.grid(row=3, column=2,padx=10,pady=10)


l1 = Label(tab1,font=("cambria",15,"bold"), width=50, anchor="c")
l1.grid(row=5,column=1,columnspan=4)


# TAB 2

l1b = Label(tab2,text = "Read/Update Product Reviews",font=("cambria",15,"bold"), width=50, anchor="c")
l1b.grid(row=1,column=1,columnspan=4)

tablelabel = Label(tab2,text="Search:",font=("cambria",15,"bold"),bg="blue",fg="white", width=8, anchor="w")
tablelabel.grid(row=2,column=1)
prev_search = StringVar()
tableentry = Entry(tab2,textvariable = prev_search,width = 45,font=("cambria",15,"bold"),bg="orange")
tableentry.grid(row=2,column=2,columnspan=3)

prodlabel = Label(tab2,text="Product:",font=("cambria",15,"bold"),bg="blue",fg="white", width=8, anchor="w")
prodlabel.grid(row=3,column=1)
product_name = StringVar()
prodentry = Entry(tab2,textvariable = product_name,width = 45,font=("cambria",15,"bold"),bg="orange")
prodentry.grid(row=3,column=2,columnspan=3)

b1 = Button(tab2, width="8", text="Modify", command=table_init,font=("cambria",15,"bold"))
b1.grid(row=4, column=3,padx=10,pady=10)


namelabel = Label(tab2,text="Name: ",font=("cambria",15,"bold"),bg="blue",fg="white", width=8, anchor="w")
namelabel.grid(row=6,column=1)
name = StringVar()
nameentry = Entry(tab2,textvariable = name,width = 45,font=("cambria",15,"bold"),bg="orange")
nameentry.grid(row=6,column=2,columnspan=3)

pricelabel = Label(tab2,text="Price: ",font=("cambria",15,"bold"),bg="blue",fg="white", width=8, anchor="w")
pricelabel.grid(row=7,column=1)
price = StringVar()
priceentry = Entry(tab2,textvariable = price,width = 45,font=("cambria",15,"bold"),bg="orange")
priceentry.grid(row=7,column=2,columnspan=3)

ratinglabel = Label(tab2,text="Rating: ",font=("cambria",15,"bold"),bg="blue",fg="white", width=8, anchor="w")
ratinglabel.grid(row=8,column=1)
rating = StringVar()
ratingentry = Entry(tab2,textvariable = rating,width = 45,font=("cambria",15,"bold"),bg="orange")
ratingentry.grid(row=8,column=2,columnspan=3)

titlelabel = Label(tab2,text="Title: ",font=("cambria",15,"bold"),bg="blue",fg="white", width=8, anchor="w")
titlelabel.grid(row=9,column=1)
title = StringVar()
titleentry = Entry(tab2,textvariable = title,width = 45,font=("cambria",15,"bold"),bg="orange")
titleentry.grid(row=9,column=2,columnspan=3)

textlabel = Label(tab2,text="Review: ",font=("cambria",15,"bold"),bg="blue",fg="white", width=8, anchor="w")
textlabel.grid(row=10,column=1)
text = StringVar()
textentry = Entry(tab2,textvariable = text,width = 45,font=("cambria",15,"bold"),bg="orange")
textentry.grid(row=10,column=2,columnspan=3)

l2 = Label(tab2,font=("cambria",15,"bold"),bg="white", width=8, anchor="c")
l2.grid(row=11,column=1,columnspan=4)

b2 = Button(tab2, width="8", text="|<", command=firstRec,font=("cambria",15,"bold"))
b2.grid(row=12, column=1,padx=10,pady=10)
b3 = Button(tab2, width="8", text="<", command=preRec,font=("cambria",15,"bold"))
b3.grid(row=12, column=2)
b4 = Button(tab2, width="8", text=">", command=nextRec,font=("cambria",15,"bold"))
b4.grid(row=12, column=3)
b5 = Button(tab2, width="8", text=">|", command=lastRec,font=("cambria",15,"bold"))
b5.grid(row=12, column=4)

b6 = Button(tab2,width="10",text="ADD", command=addRec,font=("cambria",15,"bold"))
b6.grid(row=13,column=1,padx=10,pady=10)
b7 = Button(tab2,width="10",text="DELETE", command=delRec,font=("cambria",15,"bold"))
b7.grid(row=13,column=2)
b8 = Button(tab2,width="10",text="UPDATE", command=updateRec,font=("cambria",15,"bold"))
b8.grid(row=13,column=3)
b9 = Button(tab2,width="15",text="SEARCH TITLE", command=searchRec,font=("cambria",15,"bold"))
b9.grid(row=13,column=4)



# TAB 3

l1c = Label(tab3,text = "Search Analysis",font=("cambria",15,"bold"), width=50, anchor="c")
l1c.grid(row=1,column=1,columnspan=4)

searchlabel = Label(tab3,text="Searched:",font=("cambria",18,"bold"),bg="blue",fg="white", width=8, anchor="w")
searchlabel.grid(row=2,column=1)
searchplot = StringVar()
searchentry = Entry(tab3,textvariable = searchplot,width = 45,font=("cambria",15,"bold"),bg="orange")
searchentry.grid(row=2,column=2,columnspan=3)

b10 = Button(tab3, width="8", text="Analyze", command=plot,font=("cambria",15,"bold"))
b10.grid(row=3, column=2,padx=10,pady=10)






tab_parent.pack(expand=1, fill='both')
win.mainloop()
