from tkinter import *
from tkinter import ttk, filedialog
import pandas as pd
import Visualize as vis

class ImportCSVFrame:
    def __init__(self, parent, **kwargs):
        self.parent = parent

        self.frame = ttk.Frame(self.parent, padding="5")
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
        
        # transition to next frame
        NameColumnsFrame(self.parent, data=data)
        self.frame.destroy()
        return

class NameColumnsFrame:
    def __init__(self, parent, **kwargs):
        self.parent = parent
        self.data = kwargs["data"]

        self.frame = ttk.Frame(self.parent, padding="5")
        self.frame.grid(column=0, row=0, sticky=(N,S,E,W))
        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(1, weight=1)

        ## setup variables
        self.originalColumnNames = list(self.data.columns.values)
        self.newColumnNames = []

        ## GUI Components
        ttk.Label(self.frame, text="Rename the columns (optional)").grid(column=0, row=0, sticky=(N,W))
        innerFrame = ttk.Frame(self.frame, padding="5")
        innerFrame.grid(column=0, row=1, columnspan=3, sticky=(N,W,E,S))
        ttk.Button(self.frame, text="Next", command=self.process).grid(column=3, row=3, sticky=E)

        self.populateFrame(innerFrame)

    ### functions

    def populateFrame(self, frame, **kwargs):
        for i, column in enumerate(self.originalColumnNames):
            var = StringVar()
            var.set(column)
            self.newColumnNames.append(var)

            #text box
            Entry(frame, textvariable=var).grid(column=i, row=0, padx=10, pady=4)

            #example data
            for j in range(0, 8):
                try:
                    ttk.Label(frame, text=self.data.loc[j, column]).grid(column=i, row=j+1, padx=10, pady=2)
                except KeyError:
                    #file is shorter than 8 lines long
                    break
        return

    def process(self, **kwargs):
        #rename the columns in `data`
        newColumnNamesList = [name.get() for name in self.newColumnNames]
        self.data.rename(columns=dict(zip(self.originalColumnNames, newColumnNamesList)), inplace=True)

        # transition to next frame
        vis.ChooseColumnsAndGraphFrame(self.parent, data=self.data)
        self.frame.destroy()
        return



if __name__ == "__main__":
    root = Tk()
    root.title("Visualization UI")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1) 

    ImportCSVFrame(root)
    root.mainloop()