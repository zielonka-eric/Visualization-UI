from tkinter import ttk
from tkinter import *
import ToolTip as tt
from Graph import Graph
import Plotter

class ChooseColumnsAndGraphFrame:
    def __init__(self, parent, **kwargs):
        self.parent = parent
        self.data = kwargs["data"]

        ##set variables
        self.choices = []               #the possible graphs for the features selected
        self.graphChoice = StringVar()  #the graph chosen by the user
        self.selectedLabels = []        #the features chosen by the user
        self.labels = {}                #holds all features in dataset
        self.selectedAxes = {}          #the chosen features matched up with the chosen axes
        
        ## GUI Components
        ## Columns 
        self.columnsFrame = ttk.LabelFrame(self.parent, padding="5",text='Headers')
        self.graphsFrame = ttk.LabelFrame(self.parent, padding="5",text='Graph')
        self.axesFrame = ttk.LabelFrame(self.parent, padding="5",text='Changes')
        self.buttonFrame = ttk.Frame(self.parent,padding = "5")
        self.columnsFrame.grid(column=0, row=0, sticky=(N,S,E,W))
        self.graphsFrame.grid(column=1, row=0, sticky=(N,S,E,W))
        self.axesFrame.grid(column=2, row=0, sticky=(N,S,E,W))
        self.buttonFrame.grid(column=2, row=1, sticky=E)
        
        ## Headers
        for j, name in enumerate(self.data.keys()): 
            var = IntVar()
            b = ttk.Checkbutton(self.columnsFrame, text=name, variable = var, command=self.featureSelected)
            b.grid(column=0, row=j, sticky=(N,S,E,W))
            if self.data[name].ftypes == "object:dense":
                self.typeName = "String"
            elif self.data[name].ftypes == "int64:dense":
                self.typeName = "Int"
            elif self.data[name].ftypes == "float64:dense":
                self.typeName = "Float"
            self.info = "Type: " + self.typeName +"\n Length:" +  str(len(self.data[name]))
            tt.ToolTip(b,self.info)
            self.labels[name] = var
        
        ## Graph
        self.listGraphTypes()

        ## set up the axes choices
        self.graphSelected()
        
        ## Buttons    
        ttk.Button(self.buttonFrame, text='Graph',command =self.process).grid(row=0, column=0, sticky=E, pady=4)
        ttk.Button(self.buttonFrame, text='Quit', command= self.parent.destroy).grid(row=0, column=1, sticky=E, pady=4)
    
    ### functions
    
    # Active when Graph buttton is pressed
    def process(self, **kwargs):
        Plotter.graph(Graph(self.graphChoice.get()), self.data, self.selectedAxes)

    ## selected Radiobutton for graph
    def graphSelected(self):
        self.updateOptions()

    ## called when features are selected to be graphed
    def featureSelected(self):
        #add or remove to/from selectedLabels
        self.selectedLabels = [""]              # start with default blank value if user wants to remove a choice they previously selected 
        values = [(i, var.get()) for i, var in self.labels.items()]
        for i,var in values:
            if(var ==1):
                self.selectedLabels.append(i)
        self.listGraphTypes()

    def listGraphTypes(self):
        #get suggested graphs
        self.choices = Plotter.getGraphs(self.data, self.selectedLabels)
        self.graphChoice.set(self.choices[0])

        for val, choice in enumerate(self.choices):
            b = ttk.Radiobutton(self.graphsFrame, text=choice, variable=self.graphChoice, value=choice, command=self.graphSelected)
            b.grid(row=val, column=0, padx = 2, sticky =(N,S,E,W))
        self.updateOptions()                    # to populate values in axes frame

        
    # AxesFrame based on the RadioButton     
    def updateOptions(self, **kwargs):
        #remove all options currently in frame
        for widget in self.axesFrame.winfo_children():
            widget.destroy()

        options = Plotter.getOptions(Graph(self.graphChoice.get()))
        self.selectedAxes = {label: StringVar() for label in options}

        for i, label in enumerate(options):
            ttk.Label(self.axesFrame,text=label).grid(row=i,column=0)
            ttk.Combobox(self.axesFrame, textvariable=self.selectedAxes[label], values=self.selectedLabels, state="readonly").grid(row=i, column=1)
