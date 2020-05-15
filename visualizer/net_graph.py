# libraries
import io
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from flask import send_file

# ------- DIRECTED
def draw_directed():

    #df = pd.DataFrame({'from': ['D', 'A', 'B', 'C', 'A'], 'to': ['A', 'D', 'A', 'E', 'C']})
    df = pd.DataFrame({'from': ['A', 'B', 'C', 'A'], 'to': ['B', 'C', 'D', 'C']})

    G = nx.from_pandas_edgelist(df, 'from', 'to', create_using=nx.DiGraph())

    nx.draw(G, with_labels=True, node_size=1500, alpha=0.3, arrows=True) # is plt.draw()
    plt.title("Directed")

    img = io.BytesIO()  # file-like object for the image
    plt.savefig(img)  # save the image to the stream
    img.seek(0)  # writing moved the cursor to the end of the file, reset
    plt.clf()  # clear pyplot
    return img


# ------- UNDIRECTED
def draw_undirected():
    df = pd.DataFrame({'from': ['D', 'A', 'B', 'C', 'A'], 'to': ['A', 'D', 'A', 'E', 'C']})

    G = nx.from_pandas_edgelist(df, 'from', 'to', create_using=nx.Graph())

    nx.draw(G, with_labels=True, node_size=1500, alpha=0.3, arrows=True)
    plt.title("UN-Directed")

    img = io.BytesIO()  # file-like object for the image
    plt.savefig(img)  # save the image to the stream
    img.seek(0)  # writing moved the cursor to the end of the file, reset
    plt.clf()  # clear pyplot
    return img
