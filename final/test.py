import networkx as nx
import matplotlib.pyplot as plt
import pylab


class AnnoteFinder:  # thanks to http://www.scipy.org/Cookbook/Matplotlib/Interactive_Plotting
    """
    callback for matplotlib to visit a node (display an annotation) when points are clicked on.  The
    point which is closest to the click and within xtol and ytol is identified.
    """

    def __init__(self, xdata, ydata, annotes2, axis=None, xtol=None, ytol=None):
        self.data = zip(xdata, ydata, annotes2)
        if xtol is None:
            xtol = ((max(xdata) - min(xdata)) / float(len(xdata))) / 2
        if ytol is None:
            ytol = ((max(ydata) - min(ydata)) / float(len(ydata))) / 2
        self.xtol = xtol
        self.ytol = ytol
        if axis is None:
            axis = pylab.gca()
        self.axis = axis
        self.drawnAnnotations = {}
        self.links = []

    def __call__(self, event):
        if event.inaxes:
            clickX = event.xdata
            clickY = event.ydata
            if self.axis is None or self.axis == event.inaxes:
                annotes2 = []
                for x2, y2, a in self.data:
                    if clickX - self.xtol < x2 < clickX + self.xtol and clickY - self.ytol < y2 < clickY + self.ytol:
                        dx, dy = x2 - clickX, y2 - clickY
                        annotes2.append((dx * dx + dy * dy, x2, y2, a))
                if annotes2:
                    annotes2.sort()  # to select the nearest node
                    distance, x2, y2, annote = annotes2[0]
                    self.visitnode(annote)

    def visitNode(self, annote):  # Visit the selected node
        # do something with the annote value
        print("visitNode", annote)


fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_title('select nodes to navigate there')

G = nx.MultiDiGraph()  # directed graph G = nx.wheel_graph(5)

pos = nx.spring_layout(G)  # the layout gives us the nodes position
x, y, annotes = [], [], []
for key in pos:
    d = pos[key]
    annotes.append(key)
    x.append(d[0])
    y.append(d[1])
    nx.draw(G, pos, font_size=8)

af = AnnoteFinder(x, y, annotes)
fig.canvas.mpl_connect('button_press_event', af)

plt.show()