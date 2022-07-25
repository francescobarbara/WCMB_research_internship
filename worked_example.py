#TOY EXAMPLE with 100 datapoints

import numpy as np
import pandas as pd
import networkx as nx
from collections import deque
import matplotlib.pyplot as plt
import seaborn as sns
import bisect

# Importing data
df = pd.read_csv(r'C:\Users\angus\OneDrive\Desktop\cancer_urop\17989_cancer_immuneSubset.csv')
df.sort_values(['x', 'y'], inplace = True)
#keeping the first 10 rows
df = df.iloc[:100]

'''x_coordinate, y_coordinate, radius = df['x'].iloc[0], df['y'].iloc[0], 150'''


G = create_graph(df, 30)

len(G.edges())
