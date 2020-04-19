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
import numpy as np

# Filenames
gml_file = 'st_graph.gml'


# Main program flow
def main():

    # Read in file created with create_gml_dataset.py
    st_graph = nx.read_gml(gml_file)

    # Get node subsets 
    social_nodes = {n for n, d in st_graph.nodes(data=True) if d['repo']==0}
    technical_nodes = set(st_graph) - social_nodes

    # Calculate statistics for network
    basic_algorithms(st_graph)
    centrality_algorithms(st_graph)

    # Create degree distributions and visualize network
    #plot_degree_distributions(st_graph, social_nodes, technical_nodes)
    visualize_network(st_graph, social_nodes, technical_nodes)


# Basic statistics about the network
def basic_algorithms(graph):

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
    # Calculate maximum degree (d)
    degree_list = [lis[1] for lis in nx.degree(graph)]
    print('Maximum Degree: ', max(degree_list))
    # Calculate density of graph
    print('Density: ', nx.density(graph))


# Centrality statistics about the network
def centrality_algorithms(graph):

    # Centrality functions return a dictionary of values
    # Calculate the maximum and print node name with value
    # Value stays the same for closness centrality, but the node itself changes
    centrality_dict = nx.degree_centrality(graph)
    print('Degree Centrality: ', max(centrality_dict,
                                    key=centrality_dict.get), max(centrality_dict.values()))
    centrality_dict = nx.in_degree_centrality(graph)
    print('In Degree Centrality: ', max(centrality_dict,
                                    key=centrality_dict.get), max(centrality_dict.values()))
    centrality_dict = nx.out_degree_centrality(graph)
    print('Out Degree Centrality: ', max(centrality_dict,
                                    key=centrality_dict.get), max(centrality_dict.values()))
    centrality_dict = nx.eigenvector_centrality_numpy(graph)
    print('Eigenvector Centrality: ', max(centrality_dict,
                                    key=centrality_dict.get), max(centrality_dict.values()))
    centrality_dict = nx.katz_centrality(graph)
    print('Katz Centrality: ', max(centrality_dict,
                                    key=centrality_dict.get), max(centrality_dict.values()))
    centrality_dict = nx.closeness_centrality(graph)
    print('Closeness Centrality: ', max(centrality_dict,
                                    key=centrality_dict.get), max(centrality_dict.values()))
    centrality_dict = nx.betweenness_centrality(graph)
    print('Betweenness Centrality: ', max(centrality_dict,
                                    key=centrality_dict.get), max(centrality_dict.values()))


# Plot degree distributions
def plot_degree_distributions(graph, social_nodes, technical_nodes):

    # Get degrees for subset
    social_deg = nx.degree(graph, social_nodes)
    technical_deg = nx.degree(graph, technical_nodes)
    
    # Extract values only
    social_deg = [lis[1] for lis in social_deg]
    technical_deg = [lis[1] for lis in technical_deg]
    sociotechnical_deg = social_deg + technical_deg

    print('Social Nodes: ', len(social_deg))
    print('Technical Nodes: ', len(technical_deg))

    # Weights used to normalize the distribution such that bars add to 1
    social_weights = np.ones_like(social_deg) / len(social_deg)
    technical_weights = np.ones_like(technical_deg) / len(technical_deg)
    sociotechnical_weights = np.ones_like(sociotechnical_deg) / len(sociotechnical_deg)

    plt.hist(social_deg, weights=social_weights)
    plt.title('Social Degree Distribution')
    plt.xlabel('k')
    plt.ylabel('p(k)')
    plt.show()

    plt.hist(technical_deg, weights=technical_weights)
    plt.title('Technical Degree Distribution')
    plt.xlabel('k')
    plt.ylabel('p(k)')
    plt.show()

    plt.hist(sociotechnical_deg, weights=sociotechnical_weights)
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
    
    pos = nx.kamada_kawai_layout(graph)
    
    # Draw nodes, edges, and labels
    nx.draw_networkx_nodes(graph, pos, nodelist=technical_nodes,
                           node_size=500, node_color='cyan', node_shape='s',
                           edgecolors='black', label='repository')
    nx.draw_networkx_nodes(graph, pos, nodelist=social_nodes, alpha=.5,
                           node_size=25, node_color='purple', node_shape='o',
                           edgecolors='black', label='Developer')
    nx.draw_networkx_edges(graph, pos, alpha=.5, edge_color='black')
    nx.draw_networkx_labels(graph, pos, labels,
                            font_size=5, font_weight='bold',
                            font_color='black')
    plt.show()


# Start program exection at main
if __name__ == '__main__':
    main()
