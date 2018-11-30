import plotly.offline as pl
import plotly.graph_objs as go
import numpy as np
from tkinter import ttk
from tkinter import *
from Graph import Graph

class ChooseColumnsAndGraphFrame:
    def __init__(self, parent, **kwargs):
        self.parent = parent
        self.data = kwargs["data"]

        ##set variables
        self.choices = []
        self.graphChoice = StringVar()
        self.selectedLabels = []
        self.labels = {}
        
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
            b.bind("<Enter>", self.on_enter)
            b.bind("<Leave>", self.on_leave)
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
        if Graph(self.graphChoice.get()) == Graph.SCATTER:
            self.scatterGraph()
        elif Graph(self.graphChoice.get()) == Graph.BAR:
            self.barGraph()
        elif Graph(self.graphChoice.get()) == Graph.LINE:
            self.lineGraph() 
        elif Graph(self.graphChoice.get()) == Graph.SCATTER3D:
            self.scatter3DGraph()
        elif Graph(self.graphChoice.get()) == Graph.HISTOGRAM:
            self.histogramGraph()
        elif(self.graphChoice.get()==5):
            self.bestGraph()

    ## selected Radiobutton for graph
    def graphSelected(self):
        if Graph(self.graphChoice.get()) == Graph.SCATTER:
            self.scatterOption()
        elif Graph(self.graphChoice.get()) == Graph.BAR:
            self.barOption()
        elif Graph(self.graphChoice.get()) == Graph.LINE:
            self.lineOption()
        elif Graph(self.graphChoice.get()) == Graph.SCATTER3D:
            self.scatter3DOption()
        elif Graph(self.graphChoice.get()) == Graph.HISTOGRAM:
            self.histogramOption()

    ## called when features are selected to be graphed
    def featureSelected(self):
        #add or remove to/from selectedLabels
        self.selectedLabels = []
        values = [(i, var.get()) for i, var in self.labels.items()]
        for i,var in values:
            if(var ==1):
                self.selectedLabels.append(i)
        self.listGraphTypes()

    def listGraphTypes(self):
        #get suggested graphs
        self.choices = [i.value for i in list(Graph)]           # will change
        self.graphChoice.set(self.choices[0])

        for val, choice in enumerate(self.choices):
            b = ttk.Radiobutton(self.graphsFrame, text=choice, variable=self.graphChoice, value=choice, command=self.graphSelected)
            b.grid(row=val, column=0, padx = 2, sticky =(N,S,E,W))


    # Active when mouse is hover over Headers
    def on_enter(self,event):
        print(self.data.info())
    def on_leave(self,enter):
        print("Left")
        
    # AxesFrame based on the RadioButton     
    def scatterOption(self,**kwargs):
        self.x_axis = ttk.Label(self.axesFrame,text="x")
        self.x_axis.grid(row=0,column=0)
        self.y_axis = ttk.Label(self.axesFrame,text="y")
        self.y_axis.grid(row=1,column=0)
        self.dotSize = ttk.Label(self.axesFrame,text="Size")
        self.dotSize.grid(row=2,column=0)
        self.color = ttk.Label(self.axesFrame,text="color")
        self.color.grid(row=3,column=0)
    
    
    # All the Graph functions    
    def scatterGraph(self, **kwargs): 
        pl.plot([go.Scatter(x=self.data[self.selectedLabels[0]], y=self.data[self.selectedLabels[1]], 
                mode="markers", marker=dict(size=4))])
        return
    
    def barGraph(self, **kwargs):
        pl.plot([go.Bar(x=self.data[self.selectedLabels[0]], y=self.data[self.selectedLabels[1]])])
        return 
    
    def lineGraph(self, **kwargs):
        pl.plot([go.Scatter(x=self.data[self.selectedLabels[0]], y=self.data[self.selectedLabels[1]], mode="lines+markers")])
        return
    
    def scatter3DGraph(self, **kwargs):
        x, y, z = np.random.multivariate_normal(np.array([0,0,0]), np.eye(3), 400).transpose()
        pl.plot([go.Scatter3d(x=self.data[self.selectedLabels[0]], y=self.data[self.selectedLabels[1]],z=self.data[self.selectedLabels[2]], 
        mode='markers',
        marker=dict(
        size=5,
        color=x,                # set color to an array/list of desired values
        colorscale='Viridis',   # choose a colorscale
        opacity=0.8
        ))])
        return
    
    def histogramGraph(self, **kwargs):
        pl.plot([go.Histogram(x=self.data[self.selectedLabels[0]])])
    
    def bestGraph(self, **kwargs):
        pl.plot([go.Bar(x=self.data[self.selectedLabels[0]], y=self.data[self.selectedLabels[1]])])
        return
