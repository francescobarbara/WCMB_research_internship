import numpy as np
import pandas as pd
import networkx as nx
from collections import deque
import matplotlib.pyplot as plt
import seaborn as sns
import bisect


def plot_cell(df, point_size = 0.01, color_variable = 'TextLabel', \
              size_of_legend = 5, location_of_legend = 'upper right'):
    # Generates a plot for the cells using the column 'color_variable' to choose
    # different colours.
    # Note: I'd suggest picking a fixed 'location_of_legend', because if seaborn
    # tries to find the optimal location for the legend, that takes a lot of time
    # when we have a lot of data
    
    #setting a high-resolution
    plt.rcParams['figure.dpi'] = 300
    plt.rcParams['savefig.dpi'] = 300
    fig, ax = plt.subplots()
    ax1 = sns.scatterplot(data = df, x = 'x', y = 'y', hue = 'TextLabel', s = point_size)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)



def find_neighbors(x_coordinate, y_coordinate, radius, x_array, df):
    # Inputs: the (x,y) coordinates of a cell; the radius to use as threshold
    # to establish an edge between 2 cells; x_array is a np.array for df['x']
    # Output: returns the indices of cells (as Pandas.core.indexes) that are 
    # at distance at most 'radius' from the original cell 
    
      
    x_leftmost_val = x_coordinate - radius
    x_rightmost_val = x_coordinate + radius
    # The idea is to use binary search (as we have sorted the dataframe!)
    # to find the indices that delimit the portion of df with candidate neighbors
    # and then use that slice of df 
    
        
    left_index = np.searchsorted(x_array, x_leftmost_val, side='left')
    right_index = np.searchsorted(x_array, x_rightmost_val, side='right')
    temp_df = df.iloc[left_index:right_index]
       
    neigh_indices = temp_df[((temp_df['x'] - x_coordinate)**2 + (temp_df['y'] - y_coordinate)**2) <= (radius**2)].index
    #This is an object of type Pandas.core.indexes.numeric.Int64Index
    return neigh_indices
    

def create_ebunch(cell_index, neighbors_indices):
    # Given a cell_index and the indices of its neighbors, it returns
    # a list of tuples (cell_index, neighbor_index) which is meant to be fed to
    # the add_nodes_from() method of networkx
    queue = deque()
    for index in neighbors_indices:
        queue.append((cell_index, index))
    return queue


def create_graph(df, radius = 100, return_df = False):
    
    # Important bit: sorting the dataframe w.r.t. 'x', so that find_neighbors has
    # runtime of O(log(n)) - where n = df.shape[0]
    df.sort_values(['x', 'y'], inplace = True)
    
    # This is just a np version of the column
    x_array = np.array(df['x'])
    # Finding the cell_types that will be attributes of the nodes
    cell_types = df['IntegerLabel'].unique()
    # Initializing the graph object
    G = nx.Graph()
    
    # Adding nodes to G with their cell_type as an attribute
    for cell_type in cell_types:
        G.add_nodes_from(df[df['IntegerLabel'] == cell_type].index, cell_type = cell_type)
    
    count = 0
    for cell_index in df.index:
        
        x_coordinate, y_coordinate = df.loc[cell_index, 'x'], df.loc[cell_index, 'y']
        neighbors_indices = find_neighbors(x_coordinate, y_coordinate, radius, x_array, df)
        
        # Create tuples (i.e. edges) to be added to G
        edge_list = create_ebunch(cell_index, neighbors_indices)
        G.add_edges_from(edge_list)
        
        # Removing the self-loop that was created in previous line
        G.remove_edge(cell_index, cell_index)
        
        count += 1
        if count%10000 ==0:
            print(count)
    if return_df:       
        return G, df
    return G