from tkinter import*
from pandas import DataFrame, read_csv
import pandas as pd 
import plotly.offline as pl
import plotly.graph_objs as go

def Visualize(filename):
    
    def get_values(*args):
        values = [(i, var.get()) for i, var in labels.items()]
        selectedLabels = []
        for i,var in values:
            if(var ==1):
                selectedLabels.append(i)
        graph(selectedLabels)
    
    window = Tk()
    window.title("Visualize Software")

    data = pd.read_csv(filename.get())
    
    j=1   
    labels={}
    for i in data.keys(): 
        var = IntVar()
        Checkbutton(window, text=i,variable = var).grid(column =0, row = j)
        j += 1
        labels[i] = var
    
    Button(window, text='Graph',command = get_values).grid(row=j, sticky=W, pady=4)
    Button(window, text='Quit', command= window.destroy).grid(row=j, column =1, sticky=W, pady=4)


    def graph(labels): 
        pl.plot([go.Scatter(x=data[labels[0]], y=data[labels[1]], mode="markers", marker=dict(size=4))])
        return

    
    
    window.mainloop()

 

