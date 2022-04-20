#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
version beta0.2 for barcode reading with python tkinter
'''

from tkinter import Scale, Tk, Frame, Label, Button, Text, TOP, END, LEFT, RIGHT
from tkinter.ttk import Notebook,Entry
from tkinter import ttk
import pandas as pd
import numpy as np
from os import getcwd
from os import listdir
from os.path import isfile, join
import re

##############
## global varialbes
tot_items = 0
desg_compras = pd.DataFrame(
	{
	"cantidad" : [],
	"producto" : [],
	"precio" : [],
	"codigo" : []
	},
	index = [])

### load prices from csv file
def carga_precios():
	init_path = "../testing"
	# onlyfiles = [f for f in listdir(init_path) if isfile(join(init_path, f))]
	onlyfiles = [f for f in listdir(init_path) if re.match(".*prices.csv", f)]
	onlyfiles.sort(reverse=True)
	last_file = onlyfiles[0]

	df = pd.read_csv(join(init_path, last_file), sep="|", header=0)
	return(df)

precios = carga_precios()
print(precios)

def getValue(value):
    print(value)

def getValue2(value):
    print(scale2.get())

def getValue3(value):
    print(value)


### main/root window
window=Tk()
window.title("Leector código barras - Farna")
window.geometry("600x800")

# input barcode
tinfo = Text(window, width=40, height=2)
tinfo.pack(side=TOP) # side=TOP


frame1=Frame(window)
frame1.pack(fill="both")

tablayout=Notebook(frame1)

'''
#tab1
tab1=Frame(tablayout)
tab1.pack(fill="both")
'''

# precio total
l = Label(window, text = "Precio Total:")
l.config(font =("Courier", 14))
l.pack()

Total = Text(window, height = 2, width = 12)
Total.pack() #fil="both")
Total.insert(END, " - $$$ -")


#adding table into tab
def addData(btn):
    row=btn.grid_info()['row']
    column=btn.grid_info()['column']
    #print("Column : "+str(column)+" Row : "+str(row))
    #widget0=tab2.grid_slaves(row=row,column=0)[0]
    #widget1=tab2.grid_slaves(row=row,column=1)[0]
    #widget2=tab2.grid_slaves(row=row,column=2)[0]
    widget3=tab2.grid_slaves(row=row,column=3)[0]
    #print("Value at Column 1 : "+widget0.cget("text") +" Column 2 : "+widget1.cget("text") + " Column 3 : "+widget2.cget("text")+" Column 4 : "+widget3.cget("text"))

    #updating value of label
    widget3.config(text=str(int(widget3.cget("text"))+1))
    global desg_compras
    desg_compras.iloc[int(row)-1,0] = int(widget3.cget("text"))
    Total.delete("1.0", END)
    Total.insert(END, "{:.2f}".format((desg_compras["cantidad"] * desg_compras["precio"]).sum()))
    print(desg_compras)

def decData(btn):
    row=btn.grid_info()['row']
    column=btn.grid_info()['column']
    #print("Column : "+str(column)+" Row : "+str(row))
    #widget0=tab2.grid_slaves(row=row,column=0)[0]
    #widget1=tab2.grid_slaves(row=row,column=1)[0]
    #widget2=tab2.grid_slaves(row=row,column=2)[0]
    widget3=tab2.grid_slaves(row=row,column=3)[0]
    #print("Value at Column 1 : "+widget0.cget("text") +" Column 2 : "+widget1.cget("text") + " Column 3 : "+widget2.cget("text")+" Column 4 : "+widget3.cget("text"))

    #updating value of label
    widget3.config(text= "0" if int(widget3.cget("text")) == 0 else str(int(widget3.cget("text"))-1))
    global desg_compras
    desg_compras.iloc[int(row)-1,0] = int(widget3.cget("text"))
    Total.delete("1.0", END)
    Total.insert(END, "{:.2f}".format((desg_compras["cantidad"] * desg_compras["precio"]).sum()))
    print(desg_compras)

def updProd(btn):
	result=tinfo.get(1.0, END)
	temp = result.split("\n")[0]
	row=btn.grid_info()['row']
	column=btn.grid_info()['column']

	widget4=tab2.grid_slaves(row=row,column=4)[0]
	widget4.config(text= str(widget4.cget("text") if temp == "" else "-".join(re.split("-", temp)[:-1])))

	widget5=tab2.grid_slaves(row=row,column=5)[0]
	widget5.config(text= str(widget5.cget("text") if temp == "" else "-".join(re.split("-", temp)[:-1])))

	widget6=tab2.grid_slaves(row=row,column=6)[0]
	widget6.config(text= str(widget6.cget("text") if temp == "" else re.split("-", temp)[-1]))

	global desg_compras
	desg_compras.iloc[int(row)-1,1] = widget4.cget("text")
	desg_compras.iloc[int(row)-1,2] = float(widget6.cget("text"))
	print(desg_compras)

	tinfo.delete("1.0", END)
	Total.delete("1.0", END)
	Total.insert(END, "{:.2f}".format((desg_compras["cantidad"] * desg_compras["precio"]).sum()))
	print ("prueba: " + temp)


tab2=Frame(tablayout)
tab2.pack(fill="both")

tablayout.add(tab2,text="TAB 2")

tablayout.pack(fill="both")

def limpia(): # self
	tinfo.delete("1.0", END)
	Total.delete("1.0", END)
	global tot_items
	global desg_compras
	total_items = desg_compras.shape[0]
	for ii in range(tot_items+1):
		l = list(tab2.grid_slaves(row=ii))
		for w in l:
			w.grid_forget()

	desg_compras = pd.DataFrame(
	{
		"cantidad" : [],
		"producto" : [],
		"precio" : [],
		"codigo" : []
	},	index = [])

	print("limpia grid: + " + str(l))
	print("total_items: "+ str(tot_items))

def notaDigital(): # self
	result=tinfo.get(1.0, END) #+"-1c")
	temp = [i for i in result.split("\n") if i != ""]
	prods1 = pd.DataFrame (temp, columns = ['id_product'])
	output = pd.merge(prods1, precios, how="left", on="id_product")[["id_product", "producto_x", "comprados", "min_precio", "max_precio"]].sort_values("comprados", ascending=False)
	output["comprados"] = 1

	global desg_compras
	desg_compras["producto"] = output["producto_x"]
	desg_compras["cantidad"] = output["comprados"]
	desg_compras["precio"] = output["max_precio"]
	desg_compras["codigo"] = output["id_product"]
	print(desg_compras)

	total_rows = desg_compras.shape[0]     
	global tot_items 
	tot_items = total_rows
	total_columns = 7 #output.shape[1]+3               # adding 3 buttons colum
	print(total_rows, total_columns)

	for row in range(total_rows+1):                    # adding heading row
	    for column in range(total_columns):
	        if row==0:
	            if column==0:
	                label = Label(tab2, text="Add", bg="black", fg="white", padx=3, pady=3)
	                label.config(font=('Arial', 12))
	                label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
	                tab2.grid_columnconfigure(column, weight=1)
	            elif column == 1:
	                label = Label(tab2, text="Decrease", bg="black", fg="white", padx=3, pady=3)
	                label.config(font=('Arial', 12))
	                label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
	                tab2.grid_columnconfigure(column, weight=1)
	            elif column == 2:
	                label = Label(tab2, text="Update", bg="black", fg="white", padx=3, pady=3)
	                label.config(font=('Arial', 12))
	                label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
	                tab2.grid_columnconfigure(column, weight=1)
	            elif column == 3:
	                label = Label(tab2, text="Cantidad", bg="black", fg="white", padx=3, pady=3)
	                label.config(font=('Arial', 12))
	                label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
	                tab2.grid_columnconfigure(column, weight=1)
	            elif column == 4:
	                label = Label(tab2, text="Producto", bg="black", fg="white", padx=3, pady=3)
	                label.config(font=('Arial', 12))
	                label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
	                tab2.grid_columnconfigure(column, weight=1)
	            elif column == 6:
	                label = Label(tab2, text="Precio", bg="black", fg="white", padx=3, pady=3)
	                label.config(font=('Arial', 12))
	                label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
	                tab2.grid_columnconfigure(column, weight=1)
	            elif column == 5:
	            	label = Label(tab2, text="codigo", bg="black", fg="white", padx=3, pady=3)
	            	label.config(font=('Arial', 12))
	            	label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
	            	tab2.grid_columnconfigure(column, weight=1)

	        else:
	            if column==1:
	                button=Button(tab2,text="Decrease",bg="red",fg="white",padx=3,pady=3)
	                button.grid(row=row,column=column,sticky="nsew",padx=1,pady=1)
	                button['command']=lambda btn=button:decData(btn)
	                tab2.grid_columnconfigure(column,weight=1)
	                
	            elif column==0:
	                button=Button(tab2,text="Add",bg="green",fg="white",padx=3,pady=3)
	                button.grid(row=row,column=column,sticky="nsew",padx=1,pady=1)
	                button['command']=lambda btn=button:addData(btn)
	                tab2.grid_columnconfigure(column,weight=1)

	            elif column==2:
	                button=Button(tab2,text="Update",bg="blue",fg="white",padx=3,pady=3)
	                button.grid(row=row,column=column,sticky="nsew",padx=1,pady=1)
	                button['command']=lambda btn=button:updProd(btn)
	                tab2.grid_columnconfigure(column,weight=1)

	            elif column == 3:
	                label=Label(tab2,text=str(desg_compras.iat[row-1,0]),bg="white",fg="black",padx=3,pady=3)
	                label.grid(row=row,column=column,sticky="nsew",padx=1,pady=1)
	                tab2.grid_columnconfigure(column,weight=1)  

	            elif column == 4:
	                label=Label(tab2,text=str(desg_compras.iat[row-1,1]),bg="white",fg="black",padx=3,pady=3)
	                label.grid(row=row,column=column,sticky="nsew",padx=1,pady=1)
	                tab2.grid_columnconfigure(column,weight=1)  
	            
	            elif column == 6:
	                label=Label(tab2,text=str(desg_compras.iat[row-1,2]),bg="white",fg="black",padx=3,pady=3)
	                label.grid(row=row,column=column,sticky="nsew",padx=1,pady=1)
	                tab2.grid_columnconfigure(column,weight=1)  

	            elif column == 5:
	            	label=Label(tab2,text=str(desg_compras.iat[row-1,3]),bg="white",fg="black",padx=3,pady=3)
	            	label.grid(row=row,column=column,sticky="nsew",padx=1,pady=1)
	            	tab2.grid_columnconfigure(column,weight=1)  
	
	Total.delete("1.0", END)
	sub_total = sum([ output.at[i, "comprados"] * output.at[i, "max_precio"] for i in range(output.shape[0]) if output.at[i,"max_precio"] > 0])
	Total.insert(END, sub_total)

	# tinfo.insert("1.0", output)
	tinfo.delete("1.0", END)

def recalcular():
	sub_total = 999
	global desg_compras
	temp = desg_compras['precio']*desg_compras['cantidad']
	sub_total = temp.sum()
	Total.delete("1.0", END)
	# temp = [i for i in result.split("\n") if i != ""]
	# temp01 = tab1.grid_slaves(row=1,column=1)[0]
	# print("Value1 : " + temp01.cget("text"))
	# sub_total = sum([ output.at[i, "comprados"] * output.at[i, "max_precio"] for i in range(output.shape[0]) if output.at[i,"max_precio"] > 0])
	Total.insert(END, "{:.2f}".format(sub_total))
	#tinfo.insert("1.0", output)
	#tinfo.delete("1.0", END)	


bLimpia = ttk.Button(window, text='Limpiar', command=limpia)
bLimpia.pack()

bNota = ttk.Button(window, text='Nota', command=notaDigital)
bNota.pack()

bRecalcular = ttk.Button(window, text='Recalcular', command=recalcular)
bRecalcular.pack()

bsalir = ttk.Button(window, text='Salir', command=window.destroy)
bsalir.pack()

window.mainloop()