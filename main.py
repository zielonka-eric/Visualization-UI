from tkinter import *
from tkinter import ttk, filedialog
import pandas as pd
import plotly.offline as pl
import plotly.graph_objs as go

### functions

def getFileName(*args):
    filename.set(filedialog.askopenfilename())
    return

def graph(*args):
    data = pd.read_csv(filename.get(), header=(0 if headerInFile.get() else None), prefix="col-")
    pl.plot([go.Scatter(x=data[data.columns[0]], y=data[data.columns[1]], mode="markers", marker=dict(size=4))])
    return

### import csv window
root = Tk()

## setup variables
filename = StringVar()
filename.set("")
headerInFile = BooleanVar()
headerInFile.set(True)

## setup view
root.title("Visualization UI")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
mainFrame = ttk.Frame(root, padding="5")
mainFrame.grid(column=0, row=0, sticky=(N,S,E,W))
mainFrame.columnconfigure(2, weight=1)
mainFrame.rowconfigure(5, weight=1)

ttk.Button(mainFrame, text="Choose file", command=getFileName).grid(column=1, row=1, sticky=(N,W))
ttk.Label(mainFrame, text="File Path:").grid(column=1, row=2, sticky=W)
ttk.Label(mainFrame, textvariable=filename).grid(column=1, row=3, columnspan=3, sticky=W, padx=10)
ttk.Checkbutton(mainFrame, text="file has headers in first row", variable=headerInFile).grid(column=1, row=4, columnspan=3, sticky=W)
ttk.Button(mainFrame, text="Next", command=graph).grid(column=3, row=6, sticky=E)

### open the window
root.mainloop()