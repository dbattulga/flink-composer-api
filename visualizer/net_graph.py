import io
import networkx as nx
import matplotlib.pyplot as plt
from bokeh.plotting import from_networkx
from bokeh.palettes import Spectral11
from bokeh.models import (BoxZoomTool, Circle, HoverTool, SaveTool,
                          MultiLine, Plot, Range1d, ResetTool, PanTool)


def draw_graph(shelf):
    G = nx.DiGraph(directed=True)

    keys = list(shelf.keys())
    for key in keys:
        G.add_node(shelf[key]['jobname'],
               jobname=shelf[key]['jobname'],
                version = shelf[key]['version'],
                jarid = shelf[key]['jarid'],
                jobid = shelf[key]['jobid'],
                location = shelf[key]['location'],
                mqtt = shelf[key]['mqtt'],
                source = shelf[key]['source'],
                sink = shelf[key]['sink'],
                entry_class = shelf[key]['class']
               )
        jobs = list(shelf.keys())
        for job in jobs:
            if shelf[job]['source'] == shelf[key]['sink']:
                G.add_edge(shelf[key]['jobname'], shelf[job]['jobname'])

    node_color = Spectral11[2]
    edge_color = 'black'


    # Show with Bokeh
    plot = Plot(plot_width=1000, plot_height=800, x_range=Range1d(-1.1, 1.1), y_range=Range1d(-1.1, 1.1))
    plot.title.text = "Job Graph"
    # what to show on hover
    node_hover_tool = HoverTool(tooltips=[("jobname", "@jobname"), ("version", "@version"), ("location", "@location"), ("mqtt", "@mqtt"),
                                          ("source topic", "@source"), ("sink topic", "@sink")])

    fruits = ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']

    # what tools to show on the side
    plot.add_tools(node_hover_tool, BoxZoomTool(), ResetTool(), SaveTool(), PanTool())
    # set up the graph to show, scale up and down when initially drawn
    graph_viz = from_networkx(G, nx.spring_layout, scale=1, center=(0, 0))
    # visibility of nodes and edges
    graph_viz.node_renderer.glyph = Circle(size=25, fill_color=node_color)
    graph_viz.edge_renderer.glyph = MultiLine(line_color=edge_color, line_alpha=0.8, line_width=1)
    # append the graph to plotting
    plot.renderers.append(graph_viz)
    plot.legend.location = "top_left"

    return plot


def draw_directed(shelf):
    #plt.figure(dpi=1200)
    G = nx.DiGraph(directed=True)
    keys = list(shelf.keys())
    labels = {}
    for key in keys:
        labels[shelf[key]['jobname']] = shelf[key]['jobname']
        G.add_node(shelf[key]['jobname'],
                   jobname=shelf[key]['jobname'],
                   version=shelf[key]['version'],
                   jarid=shelf[key]['jarid'],
                   jobid=shelf[key]['jobid'],
                   location=shelf[key]['location'],
                   mqtt=shelf[key]['mqtt'],
                   source=shelf[key]['source'],
                   sink=shelf[key]['sink'],
                   entry_class=shelf[key]['class']
                   )
        jobs = list(shelf.keys())
        for job in jobs:
            if shelf[job]['source'] == shelf[key]['sink']:
                G.add_edge(shelf[key]['jobname'], shelf[job]['jobname'])

    pos = nx.spring_layout(G, k=0.15, iterations=20)

    instance_list = []
    for key in keys:
        if shelf[key]['location'] not in instance_list:
            instance_list.append(shelf[key]['location'])

    count = 0
    for instance in instance_list:
        nodelist = []
        for key in keys:
            if shelf[key]['location'] == instance:
                nodelist.append(shelf[key]['jobname'])
        nx.draw_networkx_nodes(G, pos=pos, nodelist=nodelist, node_color=Spectral11[count], label=instance, node_size=500, alpha=0.8)
        count += 1

    nx.draw_networkx_edges(G, pos=pos, width=1.0, alpha=0.5)
    nx.draw_networkx_labels(G, pos=pos, labels=labels, font_size=14, alpha=0.8)
    plt.legend(scatterpoints=1)


    img = io.BytesIO()  # file-like object for the image
    plt.savefig(img)  # save the image to the stream
    img.seek(0)  # writing moved the cursor to the end of the file, reset
    plt.clf()  # clear pyplot
    return img
