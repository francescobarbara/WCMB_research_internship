import numpy as np
import pandas as pd
import networkx as nx
from scipy.spatial import Delaunay
from scipy.spatial import distance


def delaunay_graph(df, radius = 15, return_df = False):
    '''
    Parameters
    ----------
    df : pandas DataFrame
        It should have at least three columns labelled as 'x', 'y', 'IntegerLabel'
    radius : float, optional
        Indicates the threshold distance above which connections cannot be formed
    return_df : bool, optional
        Whether, along with the networkx graph, you also want to return the original dataframe
        Generally useless

    Returns
    -------
    networkx Graph object
        This function computes the Delaunay triangulation for the points given in df
        Then it builds a graph by connecting vertices that share an edge in the Delaunay
        triangulation and are at most at a distance 'radius' between each other.
        Each edge created, is assigned a weight equal to the Euclidean distance between
        its two extremes.

    '''
    
    if not (('x' in df.columns) and ('y' in df.columns) and ('IntegerLabel' in df.columns)):
        raise ValueError("df should have at least three columns labelled as 'x', 'y', 'IntegerLabel'")
       
    # We reset the index to keep consistency with scipy.Delaunay (which works 
    # with numpy arrays)
    df.reset_index(inplace = True, drop = True)
    
    cell_types = df['IntegerLabel'].unique()
    # Initializing the graph object
    G = nx.Graph()
    
    # Adding nodes to G with their cell_type as an attribute
    for cell_type in cell_types:
        G.add_nodes_from(df[df['IntegerLabel'] == cell_type].index, cell_type = cell_type)
    
    points = np.array(df.loc[:, ['x', 'y']])
    tri = Delaunay(points)
    
    count = 0
    
    for triplet in tri.simplices:
        a, b, c = triplet
        if distance.euclidean(points[a], points[b]) <= radius:
            G.add_edge(a, b, weight = distance.euclidean(points[a], points[b]))
        if distance.euclidean(points[a], points[c]) <= radius:
            G.add_edge(a, c, weight = distance.euclidean(points[a], points[c])) 
        if distance.euclidean(points[b], points[c]) <= radius:
            G.add_edge(b, c, weight = distance.euclidean(points[b], points[c])) 
        
        if count%100000 ==0:
            print(count)    
        count += 1
        
    if return_df:       
        return G, df
    
    return G


