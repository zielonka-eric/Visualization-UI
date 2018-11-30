import plotly.offline as pl
import plotly.graph_objs as go
import numpy as np

from Graph import Graph

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

def scatterGraph(data, labels):
    # set to color data if defined, otherwise adjusted size
    if labels["size"].get() == "":
        #calculate an optimal size for markers
        size = -2 * np.log(len(data.index) /100000)
        if size < 2: size = 2
        if size > 10: size = 10
    else:
        sizeData = data[labels["size"].get()]
        size = np.interp(sizeData, (sizeData.min(), sizeData.max()), (4, 14))
    
    # set to color data if defined, otherwise default
    if labels["color"].get() == "":
        color = '#1f77b4'
        scale = False
    elif data[labels["color"].get()].dtype == np.object:
        pass
    else:
        color = data[labels["color"].get()]
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
    pl.plot([go.Bar(x=data[labels[0]], y=data[labels[1]])])
    return 

def lineGraph(data, labels):
    pl.plot([go.Scatter(x=data[labels[0]], y=data[labels[1]], mode="lines+markers")])
    return

def scatter3DGraph(data, labels):
    x, y, z = np.random.multivariate_normal(np.array([0,0,0]), np.eye(3), 400).transpose()
    pl.plot([go.Scatter3d(x=data[labels[0]], y=data[labels[1]],z=data[labels[2]], 
    mode='markers',
    marker=dict(
    size=5,
    color=x,                # set color to an array/list of desired values
    colorscale='Viridis',   # choose a colorscale
    opacity=0.8
    ))])
    return

def histogramGraph(data, labels):
    pl.plot([go.Histogram(x=data[labels[0]])])

def bestGraph(data, labels):
    pl.plot([go.Bar(x=data[labels[0]], y=data[labels[1]])])
    return
