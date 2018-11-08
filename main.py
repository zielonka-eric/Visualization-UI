from tkinter import *
from tkinter import ttk, filedialog
import pandas as pd
import plotly.offline as pl
import plotly.graph_objs as go

class ImportCSVFrame:
    def __init__(self, parent):
        self.parent = parent

        self.frame = ttk.Frame(root, padding="5")
        self.frame.grid(column=0, row=0, sticky=(N,S,E,W))
        self.frame.columnconfigure(2, weight=1)
        self.frame.rowconfigure(5, weight=1)

        ## setup variables
        self.filename = StringVar()
        self.filename.set("")
        self.headerInFile = BooleanVar()
        self.headerInFile.set(True)

        ## GUI Components
        ttk.Button(self.frame, text="Choose file", command=self.getFileName).grid(column=1, row=1, sticky=(N,W))
        ttk.Label(self.frame, text="File Path:").grid(column=1, row=2, sticky=W)
        ttk.Label(self.frame, textvariable=self.filename).grid(column=1, row=3, columnspan=3, sticky=W, padx=10)
        ttk.Checkbutton(self.frame, text="file has headers in first row", variable=self.headerInFile).grid(column=1, row=4, columnspan=3, sticky=W)
        ttk.Button(self.frame, text="Next", command=self.process).grid(column=3, row=6, sticky=E)

    ### functions

    def getFileName(self, **kwargs):
        self.filename.set(filedialog.askopenfilename())
        return

    def process(self, **kwargs):
        data = pd.read_csv(self.filename.get(), header=(0 if self.headerInFile.get() else None), prefix="col-")
        pl.plot([go.Scatter(x=data[data.columns[0]], y=data[data.columns[1]], mode="markers", marker=dict(size=4))])
        return

if __name__ == "__main__":
    root = Tk()
    root.title("Visualization UI")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1) 

    ImportCSVFrame(root)
    root.mainloop()
    