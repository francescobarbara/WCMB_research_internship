import networkx as nx
from collections import deque

def create_ebunch(cell_index, neighbors_indices):
    queue = deque()
    for index in neighbors_indices:
        queue.append((cell_index, index))
    return queue


def create_graph(df, radius = 100):
    #finding the cell_types that will be attributes of the ndoes
    cell_types = df['IntegerLabel'].unique()
    #initializing the graph object
    G = nx.Graph()
    for cell_type in cell_types:
        G.add_nodes_from(df[df['IntegerLabel'] == cell_type].index, cell_type = cell_type)
    
    count = 0
    for cell_index in df.index:
        count += 1
        if count%10000 ==0:
            print(count)
        x_coordinate, y_coordinate = df.loc[cell_index, 'x'], df.loc[cell_index, 'y']
        neighbors_indices = find_neighbors(x_coordinate, y_coordinate, radius)
        #create tuples
        edge_list = create_ebunch(cell_index, neighbors_indices)
        G.add_edges_from(edge_list)
    return G
    
graph = create_graph(df, 100)
