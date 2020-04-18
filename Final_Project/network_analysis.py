"""
Justin Stachofsky
Dr. Gebremedhin
CPTS 591
5 May 2020
Analyze network from generated gml file
"""

# Third Party Libraries
import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms import bipartite

gml_file = 'st_graph.gml'

# Main program flow


def main():

    # Read in file created with create_gml_dataset.py
    st_graph = nx.read_gml(gml_file)

    # Since graph is directed, need to create two sets of nodes manually
    # Most bipartite algorithms require passing a nodeset with the graph
    top_nodes = {n for n, d in st_graph.nodes(
        data=True) if d['bipartite'] == 0}
    bottom_nodes = set(st_graph) - top_nodes

    # Calculate statistics for network
    basic_algorithms(st_graph, bottom_nodes)
    centrality_algorithms(st_graph, bottom_nodes)
    print('Spectral Bipartivity: ', bipartite.spectral_bipartivity(st_graph))
    print('Robins Alexander Bipartite Clustering Coeficient: ',
          bipartite.robins_alexander_clustering(st_graph))

    # Create degree distributions
    plot_degree_distributions(st_graph, bottom_nodes)


# Basic statistics about the network
def basic_algorithms(graph, node_set):

    # Calculate number of nodes (n)
    print('Nodes: ', len(graph))
    # Calculate number of links (m)
    print('Edges: ', graph.number_of_edges())
    # Calculate number of connected components (cstrong and cweak)
    print('Strongly Connected Components: ',
          nx.number_strongly_connected_components(graph))
    print('Weakly Connected Components: ',
          nx.number_weakly_connected_components(graph))
    # Calculate average path length (l)
    print('Average Path Length: ', nx.average_shortest_path_length(graph))
    # Calculate density of graph
    print('Density: ', bipartite.density(graph, node_set))


# Centrality statistics about the network
def centrality_algorithms(graph, node_set):

    # Centrality functions return a dictionary of values
    # Calculate the maximum and print node name with value
    # Value stays the same for closness centrality, but the node itself changes
    centrality_dict = bipartite.closeness_centrality(graph, node_set)
    print('Closeness Centrality: ', max(centrality_dict,
                                        key=centrality_dict.get), max(centrality_dict.values()))
    centrality_dict = bipartite.degree_centrality(graph, node_set)
    print('Degree Centrality: ', max(centrality_dict,
                                     key=centrality_dict.get), max(centrality_dict.values()))
    centrality_dict = bipartite.betweenness_centrality(graph, node_set)
    print('Betweenness Centrality: ', max(centrality_dict,
                                          key=centrality_dict.get), max(centrality_dict.values()))


# Plot bipartite degree distributions
def plot_degree_distributions(graph, node_set):

    # Get set of nodes
    social, technical = bipartite.degrees(graph, node_set)

    print(social)

    # Extract values only
    social = [lis[1] for lis in social]
    technical = [lis[1] for lis in technical]
    sociotechnical = social + technical

    # Formatting for historgram
    plt.xlabel('k')
    plt.ylabel('p(k)')

    # density=True normalizes histogram
    plt.hist(social, density=True)
    plt.title('Social Degree Distribution')
    plt.show()

    plt.hist(technical, density=True)
    plt.title('Technical Degree Distribution')
    plt.show()

    plt.hist(sociotechnical, density=True)
    plt.title('Sociotechnical Degree Distribution')
    plt.show()


# Start program exection at main
if __name__ == '__main__':
    main()
