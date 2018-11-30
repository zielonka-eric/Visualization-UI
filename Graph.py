from enum import Enum

class Graph(Enum):
    SCATTER = "Scatter Plot"
    BAR = "Bar"
    LINE = "Line"
    SCATTER3D = "3D Scatter Plot"
    HISTOGRAM = "Histogram"
    HISTOGRAM2D = "2D Histogram"
    BOXPLOT = "Boxplot"
    PIE = "Pie"
    SCATTERMAP = "Scatter Plot Map"