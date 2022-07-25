import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
import bisect

# Importing data
df = pd.read_csv(r'C:\Users\angus\OneDrive\Desktop\cancer_urop\17989_cancer_immuneSubset.csv')
# Trivial data exploration
df['TextLabel'].value_counts()
df = df.iloc[:10,:]

# Important bit: sorting the dataframe w.r.t. 'x', so that find_neighbors has
# runtime of O(log(n)) - where n = df.shape[0]
df.sort_values(['x', 'y'], inplace = True)


def plot_cell(df, point_size = 0.01, color_variable = 'TextLabel', \
              size_of_legend = 5, location_of_legend = 'upper right'):
    # Generates a plot for the cells using the column 'color_variable' to choose
    # different colours.
    # Note: I'd suggest picking a fixed 'location_of_legend', because if seaborn
    # tries to find the optimal location for the legend, that takes a lot of time
    # when we have a lot of data
    cell_plot = sns.scatterplot(data = df, x = 'x', y = 'y', hue = 'TextLabel', s = point_size)
    cell_plot.legend(fontsize = size_of_legend, loc = location_of_legend)
    plt.show()


def find_neighbors(x_coordinate, y_coordinate, radius):#add df here
    # Inputs: the (x,y) coordinates of a cell; the radius to use as threshold
    # to establish an edge between 2 cells
    # Output: returns the indices of cells (as Pandas.core.indexes) that are 
    # at distance at most 'radius' from the original cell 
    
    # Clearly any valid index must have x coordinate between the two values below
    x_leftmost_val = x_coordinate - radius
    x_rightmost_val = x_coordinate + radius
    
    # The idea is to use binary search (as we have sorted the dataframe!)
    # to find the indices that delimit the portion of df with candidate neighbors
    # and then use that slice of df 
    #these are entries of the index pd.Series
    left_cell_ID = bisect.bisect_left(df['x'], x_leftmost_val)
    right_cell_ID = bisect.bisect_right(df['x'], x_rightmost_val)  
    
    print(right_cell_ID)
    
    left_index = df.index.get_loc(left_cell_ID)
    right_index = df.index.get_loc(right_cell_ID - 1)
    temp_df = df.iloc[left_index:right_index]
       
    neigh_indices = temp_df[((temp_df['x'] - x_coordinate)**2 + (temp_df['y'] - y_coordinate)**2) <= (radius**2)].index
    #This is an object of type Pandas.core.indexes.numeric.Int64Index
    return neigh_indices
    

nn = find_neighbors(5000, 40000, 500)

x_coordinate, y_coordinate, radius = 2766, 42475, 1000





l = pd.Series([1,2,4,5,7,8])
i = bisect.bisect_left(l, 3)





#sanity check. It's working
plt.figure()
sns.scatterplot(valid_df['x'], valid_df['y'])
plt.figure()
sns.scatterplot(df['x'],df['y'])
