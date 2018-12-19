import plotly.offline as pl
import plotly.graph_objs as go
import numpy as np

from Graph import Graph

def getGraphs(data, labels):
    tempdata = data[labels[1:]]
    floatNumber = tempdata.get_dtype_counts().get("float64")
    floatNumber = 0 if floatNumber is None else floatNumber
    stringNumber = tempdata.get_dtype_counts().get("object")
    stringNumber = 0 if stringNumber is None else stringNumber
    intNumber = tempdata.get_dtype_counts().get("int64")
    intNumber = 0 if intNumber is None else intNumber

    numNumber = floatNumber + intNumber

    #print(tempdata.get_dtype_counts())

    graphList = []
    if stringNumber == 0:
        if numNumber == 1:
            graphList = [Graph.HISTOGRAM,Graph.BOXPLOT]
        if numNumber == 2:
            graphList = [Graph.SCATTER, Graph.LINE, Graph.BAR, Graph.HISTOGRAM2D, Graph.SCATTERMAP]
        if numNumber == 3:
            graphList = [Graph.SCATTER, Graph.SCATTERMAP, Graph.SCATTER3D, Graph.BAR]
        if numNumber == 4:
            graphList = [Graph.SCATTER, Graph.SCATTERMAP, Graph.SCATTER3D,]
        if numNumber == 5:
            graphList = [Graph.SCATTER3D]
    if stringNumber == 1:
        if numNumber == 0:
            graphList = [Graph.PIE]
        if numNumber == 1:
            graphList = [Graph.BAR, Graph.BOXPLOT, Graph.PIE]
        if numNumber == 2:
            graphList = [Graph.BAR, Graph.SCATTER, Graph.SCATTERMAP]
        if numNumber == 3:
            graphList = [Graph.SCATTER, Graph.SCATTER3D, Graph.SCATTERMAP]
        if numNumber == 4:
            graphList = [Graph.SCATTER3D]
    if stringNumber == 2:
        if numNumber == 1:
            graphList = [Graph.BAR]
    
    return [i.value for i in graphList]

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
        options = ["y", "[category]"]
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
        traces = [go.Scatter(
            x=data[labels["x"].get()],
            y=data[labels["y"].get()], 
            mode="markers",
            marker=dict(
                size = size
            )
        )]
        fig = dict(data=traces, layout=dict(
            title = labels["y"].get() + " vs. " + labels["x"].get(),
            yaxis = dict(title=labels["y"].get()),
            xaxis = dict(title=labels["x"].get())
        ))
    elif data[labels["[color]"].get()].dtype == np.object:
        ## find unique labels in the column set to "color"    
        fig = dict(
            data=[ go.Scatter(
                    x= data[ data[labels["[color]"].get()]==colorLabel ][labels["x"].get()],
                    y= data[ data[labels["[color]"].get()]==colorLabel ][labels["y"].get()],
                    name=colorLabel,
                    mode='markers',
                    marker=dict(
                        size=size
                    )
                 ) for colorLabel in data[labels["[color]"].get()].unique() ],
            layout=dict(
                title = labels["y"].get() + " vs. " + labels["x"].get(),
                yaxis = dict(title=labels["y"].get()),
                xaxis = dict(title=labels["x"].get())
            )
        )
    else:
        traces = [go.Scatter(
            x=data[labels["x"].get()],
            y=data[labels["y"].get()], 
            mode="markers",
            marker=dict(
                size = size,
                color = data[labels["[color]"].get()],
                showscale = True,
                colorbar=dict(
                    title=labels["[color]"].get()
                )
            )
        )]
        fig = dict(data=traces, layout=dict(
            title = labels["y"].get() + " vs. " + labels["x"].get(),
            yaxis = dict(title=labels["y"].get()),
            xaxis = dict(title=labels["x"].get())
        ))

    pl.plot(fig)
    return

def barGraph(data, labels):
    if labels["[color]"].get() == "":
        traces = [go.Bar(
            x=data[labels["category"].get()],
            y=data[labels["y"].get()]
        )]
        fig = dict(data=traces, layout=dict(
            title = labels["y"].get() + " vs. " + labels["category"].get(),
            yaxis = dict(title=labels["y"].get()),
            xaxis = dict(title=labels["category"].get())
        ))
    elif data[labels["[color]"].get()].dtype == np.object:
        ## find unique labels in the column set to "color"    
        fig = dict(
            data=[ go.Bar(
                x=data[labels["category"].get()],
                y=data[labels["y"].get()]
            ) for colorLabel in data[labels["[color]"].get()].unique() ],
            layout=dict(
                title = labels["y"].get() + " vs. " + labels["category"].get(),
                yaxis = dict(title=labels["y"].get()),
                xaxis = dict(title=labels["category"].get())
            )
        )
    else:
        traces = [go.Bar(
            x=data[labels["category"].get()],
            y=data[labels["y"].get()],
            marker=dict(
                color = data[labels["[color]"].get()],
                showscale = True,
                colorbar=dict(
                    title=labels["[color]"].get()
                )
            )
        )]
        fig = dict(data=traces, layout=dict(
            title = labels["y"].get() + " vs. " + labels["category"].get(),
            yaxis = dict(title=labels["y"].get()),
            xaxis = dict(title=labels["category"].get())
        ))

    pl.plot(fig)
    return

def lineGraph(data, labels):
    traces = [go.Scatter(x=data[labels["x"].get()], y=data[labels["y"].get()], mode="lines+markers")]
    fig = dict(data=traces, layout=dict(
        title = labels["y"].get() + " vs. " + labels["x"].get(),
        yaxis = dict(title=labels["y"].get()),
        xaxis = dict(title=labels["x"].get())
    ))
    pl.plot(fig)
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
        traces = [go.Scatter3d(
            x=data[labels["x"].get()],
            y=data[labels["y"].get()],
            z=data[labels["z"].get()], 
            mode="markers",
            marker=dict(
                size = size,
                opacity=0.8
            )
        )]
        fig = dict(data=traces, layout=dict(
            title = labels["z"].get() + " vs. " + labels["y"].get() + " vs. " + labels["x"].get(),
            scene = dict(
                yaxis = dict(title=labels["y"].get()),
                xaxis = dict(title=labels["x"].get()),
                zaxis = dict(title=labels["z"].get())
            )
        ))
    elif data[labels["[color]"].get()].dtype == np.object:
        ## find unique labels in the column set to "color"    
        fig = dict(
            data=[ go.Scatter3d(
                    x=data[ data[labels["[color]"].get()]==colorLabel ][labels["x"].get()],
                    y=data[ data[labels["[color]"].get()]==colorLabel ][labels["y"].get()],
                    z=data[ data[labels["[color]"].get()]==colorLabel ][labels["z"].get()],
                    name=colorLabel,
                    mode="markers",
                    marker=dict(
                        size = size,
                        opacity=0.8
                    )
                ) for colorLabel in data[labels["[color]"].get()].unique() ],
            layout=dict(
                title = labels["z"].get() + " vs. " + labels["y"].get() + " vs. " + labels["x"].get(),
                scene = dict(
                    yaxis = dict(title=labels["y"].get()),
                    xaxis = dict(title=labels["x"].get()),
                    zaxis = dict(title=labels["z"].get())
                )
            )
        )
    else:
        traces = [go.Scatter3d(
            x=data[labels["x"].get()],
            y=data[labels["y"].get()],
            z=data[labels["z"].get()],
            mode="markers",
            marker=dict(
                size = size,
                color = data[labels["[color]"].get()],
                showscale = True,
                opacity=0.8,
                colorbar=dict(
                    title=labels["[color]"].get()
                )
            )
        )]
        fig = dict(data=traces, layout=dict(
            title = labels["z"].get() + " vs. " + labels["y"].get() + " vs. " + labels["x"].get(),
            scene = dict(
                yaxis = dict(title=labels["y"].get()),
                xaxis = dict(title=labels["x"].get()),
                zaxis = dict(title=labels["z"].get())
            )
        ))

    pl.plot(fig)
    return

def histogramGraph(data, labels):
    traces = [go.Histogram(x=data[labels["x"].get()])]
    fig = dict(data=traces, layout=dict(
        title = "Histogram of " + labels["x"].get(),
        xaxis = dict(title=labels["x"].get()),
        yaxis = dict(title="Count")
    ))
    pl.plot(fig)
    return

def histogram2dGraph(data, labels):
    traces = [go.Histogram2d(
        x=data[labels["x"].get()],
        y=data[labels["y"].get()],
        colorscale='Cividis',
        colorbar=dict(
            title="Count"
        )
    )]
    fig = dict(data=traces, layout=dict(
        title = "Histogram of " + labels["y"].get() + " vs. " + labels["x"].get(),
        yaxis = dict(title=labels["y"].get()),
        xaxis = dict(title=labels["x"].get())
    ))
    pl.plot(fig)
    return

def boxPlotGraph(data,labels):
    if labels["[category]"].get() != "":
        traces = [ go.Box(
            y=data[data[labels["[category]"].get()]==name][labels["y"].get()],
            name=name
        ) for name in data[labels["[category]"].get()].unique() ]
        fig = dict(data=traces, layout=dict(
            title = "Boxplot of " + labels["y"].get(),
            yaxis = dict(title=labels["y"].get())
        ))
    else:
        traces = [go.Box(
            y=data[labels["y"].get()],
            name=" "
        )]
        fig = dict(data=traces, layout=dict(
            title = "Boxplot of " + labels["y"].get(),
            yaxis = dict(title=labels["y"].get())
        ))

    pl.plot(fig)
    return

def pieGraph(data,labels):
    if labels["[values]"].get() != "":
        categories=data[labels["category"].get()]
        values=data[labels["[values]"].get()]
    else:
        values = data[labels["category"].get()].value_counts()
        categories = values.keys()

    fig = dict(
        data = [go.Pie(
            labels=categories,
            values=values
        )],
        layout = dict(
            title = "Pie chart of " + labels["category"].get()
        ))

    pl.plot(fig)
    return
    
def scatterMapGraph(data,labels):
    # set to color data if defined, otherwise adjusted size
    if labels["[size]"].get() == "":
        size = 10
    else:
        sizeData = data[labels["[size]"].get()]
        size = np.interp(sizeData, (sizeData.min(), sizeData.max()), (8, 26))
    
    geo = dict(
        scope="world",
        resolution=50,
        showland = True,
        landcolor = "rgb(231, 234, 232)",
        showsubunits = True,
        subunitcolor = "rgb(255, 255, 255)",
        showcountries = True,
        countrycolor = "rgb(255, 255, 255)",
        showlakes = True,
        lakecolor = "rgb(255, 255, 255)",
        showcoastlines=True,
        coastlinecolor="rgb(255, 255, 255)",
        projection=dict(
            type="equirectangular"
        )
    )

    # set to color data if defined, otherwise default
    if labels["[color]"].get() == "":
        traces = [go.Scattergeo(
            lon=data[labels["longitude"].get()],
            lat=data[labels["latitude"].get()],
            mode = 'markers',
            marker = dict(
                size = size,
                opacity = 0.8,
                line = dict(
                    width=1,
                    color='rgba(50, 50, 50)'
                )
            )
        )]
        fig = dict(data=traces, layout=dict(
            #title = "",
            geo=geo
        ))
    elif data[labels["[color]"].get()].dtype == np.object:
        ## find unique labels in the column set to "color"
        fig = dict(
            data=[ go.Scattergeo(
                    lon=data[ data[labels["[color]"].get()]==colorLabel ][labels["longitude"].get()],
                    lat=data[ data[labels["[color]"].get()]==colorLabel ][labels["latitude"].get()],
                    name=colorLabel,
                    mode = 'markers',
                    marker = dict(
                        size = size,
                        opacity = 0.8,
                        line = dict(
                            width=1.5,
                            color='rgba(50, 50, 50)'
                        )
                    )
                ) for colorLabel in data[labels["[color]"].get()].unique() ],
            layout=dict(
                #title = "",
                geo=geo
            )
        )
    else:
        traces = [go.Scattergeo(
            lon=data[labels["longitude"].get()],
            lat=data[labels["latitude"].get()],
            mode = 'markers',
            marker = dict(
                size = size,
                opacity = 0.8,
                color = data[labels["[color]"].get()],
                showscale = True,
                colorbar=dict(
                    title=labels["[color]"].get()
                ),
                line = dict(
                    width=1.5,
                    color='rgba(50, 50, 50)'
                )
            )
        )]
        fig = dict(data=traces, layout=dict(
            #title = "",
            geo=geo
        ))

    pl.plot(fig)
    return
