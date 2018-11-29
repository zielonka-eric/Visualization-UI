import plotly.offline as pl
import plotly.graph_objs as go
import numpy as np
from tkinter import ttk
from tkinter import*

class ChooseColumnsAndGraphFrame:
    def __init__(self, parent, **kwargs):
        self.parent = parent
        self.data = kwargs["data"]

        ##set variables
        self.choices = [("Scatter"),("Bar"),("Line"),("Scatter3D"),("Histogram"),("Best Choice")]
        self.my_var = IntVar()
        self.selectedLabels = []
        self.labels={}
        r =1;
        j = 1;
        
        ## GUI Components
        ## Columns 
        self.columnsFrame = ttk.LabelFrame(self.parent, padding="5",text='Headers')
        self.graphsFrame = ttk.LabelFrame(self.parent, padding="5",text='Graph')
        self.axesFrame = ttk.LabelFrame(self.parent, padding="5",text='Changes')
        self.buttonFrame = ttk.Frame(self.parent,padding = "5")
        self.columnsFrame.grid(column=0, row=0, sticky=(N,S,E,W))
        self.graphsFrame.grid(column=1, row=0, sticky=(N,S,E,W))
        self.axesFrame.grid(column=2, row=0, sticky=(N,S,E,W))
        self.buttonFrame.grid(column=2,row =5,sticky =(N,S,E,W))
        
        ## Headers
        for i in self.data.keys(): 
            var = IntVar()
            self.b = ttk.Checkbutton(self.columnsFrame, text=i,variable = var)
            self.b.grid(column =0, row = j,sticky =(N,S,E,W))
            self.b.bind("<Enter>", self.on_enter)
            self.b.bind("<Leave>", self.on_leave)
            j += 1
            self.labels[i] = var
        
        ## Graph   
        for val, choice in enumerate(self.choices):
            Radiobutton(self.graphsFrame, text=choice,indicatoron = 0,padx = 2,variable=self.my_var, value=val,command=self.selected).grid(row=r, column =2,sticky =(N,S,E,W))
            r+=1
            print(val)
        ## Buttons    
        ttk.Button(self.buttonFrame, text='Graph',command =self.process).grid(row=j+r, sticky=W, pady=4)
        ttk.Button(self.buttonFrame, text='Quit', command= self.parent.destroy).grid(row=j+r, column =1, sticky=W, pady=4)
    
    ### functions
    
    # Active when Graph buttton is pressed
    def process(self, **kwargs):
       values = [(i, var.get()) for i, var in self.labels.items()]
       for i,var in values:
           if(var ==1):
                self.selectedLabels.append(i)
       if(self.my_var.get()==0):
            self.scatterGraph()
       elif(self.my_var.get()==1):
            self.barGraph()
       elif(self.my_var.get()==2):
            self.lineGraph() 
       elif(self.my_var.get()==3):
            self.scatter3DGraph()
       elif(self.my_var.get()==4):
            self.histogramGraph()
       elif(self.my_var.get()==5):
            self.bestGraph()
            
    ## selected Radiobutton 
    def selected(self):
     if self.my_var.get()==0:
        self.scatterOption()
     elif self.my_var.get()==1:
        self.barOption()
     elif self.my_var.get()==2:
        self.lineOption()
     elif self.my_var.get()==3:
        self.scatter3DOption()
     elif self.my_var.get()==4:
        self.histogramOption()
     elif self.my_var.get()==5:
         self.bestOption()
     
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
    
    
    
          
    
    
   
    
        
        
        
    
    
    
    
    
    
   
   
   
    
    


    

 