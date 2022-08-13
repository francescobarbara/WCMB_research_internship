# TOY EXAMPLE FOR A DELAUNAY GRAPH

# Run script containing 'delaunay graph'
runfile(r'C:\Users\angus\OneDrive\Desktop\cancer_urop\network_generation\delaunay_network_generation\delaunay_network_generator.py')

# Importing data
df = pd.read_csv(r'C:\Users\angus\OneDrive\Desktop\cancer_urop\17989_cancer_immuneSubset.csv')

#Runtime down to 1-2 minutes!
G = delaunay_graph(df, radius = 15, return_df = False)

#Saving the graph as a pickle file
path = 'add_path_here'
nx.write_gpickle(G, path + 'toy_data_network_10_microns.pickle')
