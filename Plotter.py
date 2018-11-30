import plotly.offline as pl
import plotly.graph_objs as go
import numpy as np

from Graph import Graph

def getGraphs():
    pass

def getOptions(graphChoice):
    options = []
    if graphChoice == Graph.SCATTER:
        options = ["x", "y", "[color]", "[size]"]
    elif graphChoice == Graph.BAR:
        options = ["category", "y", "[color]"]
    elif graphChoice == Graph.LINE:
        options = ["x", "y"]
    elif graphChoice == Graph.SCATTER3D:
        options = ["x", "y", "z", "[color]", "[size]"]
    elif graphChoice == Graph.HISTOGRAM:
        options = ["x"]
    elif graphChoice == Graph.HISTOGRAM2D:
        options = ["x", "y"]
    elif graphChoice == Graph.BOXPLOT:
        options = ["category", "y"]
    elif graphChoice == Graph.PIE:
        options = ["category", "[values]"]
    elif graphChoice == Graph.SCATTERMAP:
        options = ["latitude", "longitude", "[color]", "[size]"]
    return options

def graph(graphChoice, data, labels):
    if graphChoice == Graph.SCATTER:
        scatterGraph(data, labels)
    elif graphChoice == Graph.BAR:
        barGraph(data, labels)
    elif graphChoice == Graph.LINE:
        lineGraph(data, labels) 
    elif graphChoice == Graph.SCATTER3D:
        scatter3DGraph(data, labels)
    elif graphChoice == Graph.HISTOGRAM:
        histogramGraph(data, labels)
    elif graphChoice == Graph.HISTOGRAM2D:
        histogram2dGraph(data, labels)
    elif graphChoice == Graph.BOXPLOT:
        boxPlotGraph(data, labels)
    elif graphChoice == Graph.PIE:
        pieGraph(data,labels)
    elif graphChoice == Graph.SCATTERMAP:
        scatterMapGraph(data,labels)

def scatterGraph(data, labels):
    # set to color data if defined, otherwise adjusted size
    if labels["[size]"].get() == "":
        #calculate an optimal size for markers
        size = -2 * np.log(len(data.index) /100000)
        if size < 2: size = 2
        if size > 10: size = 10
    else:
        sizeData = data[labels["[size]"].get()]
        size = np.interp(sizeData, (sizeData.min(), sizeData.max()), (4, 14))
    
    # set to color data if defined, otherwise default
    if labels["[color]"].get() == "":
        color = '#1f77b4'
        scale = False
    elif data[labels["[color]"].get()].dtype == np.object:
        pass
    else:
        color = data[labels["[color]"].get()]
        scale = True
    
    pl.plot([go.Scatter(
        x=data[labels["x"].get()],
        y=data[labels["y"].get()], 
        mode="markers",
        marker=dict(
            size = size,
            color = color,
            showscale = scale
        )
    )])
    return

def barGraph(data, labels):
    pl.plot([go.Bar(x=data[labels["category"].get()], y=data[labels["y"].get()])])
    return

def lineGraph(data, labels):
    pl.plot([go.Scatter(x=data[labels["x"]], y=data[labels["y"]], mode="lines+markers")])
    return

def scatter3DGraph(data, labels):
    # set to color data if defined, otherwise adjusted size
    if labels["[size]"].get() == "":
        #calculate an optimal size for markers
        size = -2 * np.log(len(data.index) /100000)
        if size < 2: size = 2
        if size > 10: size = 10
    else:
        sizeData = data[labels["[size]"].get()]
        size = np.interp(sizeData, (sizeData.min(), sizeData.max()), (4, 14))
    
    # set to color data if defined, otherwise default
    if labels["[color]"].get() == "":
        color = '#1f77b4'
        scale = False
    elif data[labels["[color]"].get()].dtype == np.object:
        pass
    else:
        color = data[labels["[color]"].get()]
        scale = True
    
    pl.plot([go.Scatter3d(
        x=data[labels["x"].get()],
        y=data[labels["y"].get()],
        z=data[labels["z"].get()],
        mode='markers',
        marker=dict(
            size=size,
            color=color,
            showscale=scale,
            opacity=0.8
        )
    )])
    return

def histogramGraph(data, labels):
    pl.plot([go.Histogram(x=data[labels[0]])])

def histogram2dGraph(data, labels):
    pl.plot([go.Histogram2d(
    x=data[labels[0]],
    y=data[labels[1]],
    colorscale='YlGnBu',
    zmax=10,
    nbinsx=14,
    nbinsy=14,
    zauto=False,
)])

def boxPlotGraph(data,labels):
    pl.plot([go.Box(x=data[labels[0]])])

def pieGraph(data,labels):
    pl.plot([go.Pie(label=data[labels[0]],values=data[labels[1]])])
    
def scatterMapGraph(data,labels):
    print ("Coming Soon")
