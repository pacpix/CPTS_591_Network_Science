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
import numpy as np

# Filenames
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

    # Create degree distributions and visualize network
    #plot_degree_distributions(st_graph, bottom_nodes)
    visualize_network(st_graph, top_nodes, bottom_nodes)


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

    # Extract values only
    social = [lis[1] for lis in social]
    technical = [lis[1] for lis in technical]
    sociotechnical = social + technical

    print('Social Nodes: ', len(social))
    print('Technical Nodes: ', len(technical))

    # Weights used to normalize the distribution such that bars add to 1
    social_weights = np.ones_like(social) / len(social)
    technical_weights = np.ones_like(technical) / len(technical)
    sociotechnical_weights = np.ones_like(sociotechnical) / len(sociotechnical)

    plt.hist(social, weights=social_weights)
    plt.title('Social Degree Distribution')
    plt.xlabel('k')
    plt.ylabel('p(k)')
    plt.show()

    plt.hist(technical, weights=technical_weights)
    plt.title('Technical Degree Distribution')
    plt.xlabel('k')
    plt.ylabel('p(k)')
    plt.show()

    plt.hist(sociotechnical, weights=sociotechnical_weights)
    plt.title('Sociotechnical Degree Distribution')
    plt.xlabel('k')
    plt.ylabel('p(k)')
    plt.show()


def visualize_network(graph, social_nodes, technical_nodes):
    
    # Need to create subset of technical node labels
    # Not showing social node labels
    labels = {}
    for node in graph.nodes():
        if node in technical_nodes:
            labels[node] = node

    # Formats graph layout
    # k equation is optimal spacing between nodes
    pos = nx.spring_layout(
        graph, k=.3*1/np.sqrt(len(graph.nodes())), iterations=20)

    # Draw nodes, edges, and labels
    nx.draw_networkx_nodes(graph, pos, nodelist=technical_nodes,
                           node_size=500, node_color='cyan', node_shape='s',
                           edgecolors='black', label='repository')
    nx.draw_networkx_nodes(graph, pos, nodelist=social_nodes, alpha=.5,
                           node_size=15, node_color='blue', node_shape='o',
                           edgecolors='black', label='Developer')
    nx.draw_networkx_edges(graph, pos, alpha=.5, edge_color='purple')
    nx.draw_networkx_labels(graph, pos, labels,
                            font_size=5, font_weight='bold',
                            font_color='black')
    plt.show()


# Start program exection at main
if __name__ == '__main__':
    main()
