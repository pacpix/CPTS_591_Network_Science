"""
Julia Stachofsky
Dr. Gebremedhin
CPTS 591
9 March 2020
Assignment 2
"""

# stdlib
import os

# Third party libraries
import igraph as ig
import numpy as np
import numpy.linalg as la
import matplotlib.pyplot as plt


# Main program flow
def main():

    # Create networks from gml datasets (#1)
    n_political = ig.Graph.Read(
        f=os.getcwd() + '/Datasets/polblogs.gml', format='gml')
    n_neural = ig.Graph.Read(
        f=os.getcwd() + '/Datasets/celegansneural.gml', format='gml')
    n_internet = ig.Graph.Read(
        f=os.getcwd() + '/Datasets/as-22july06.gml', format='gml')
    n_lesmis = ig.Graph.Read(
        f=os.getcwd() + '/Datasets/lesmis.gml', format='gml')

    # Calculate centrality measures
    calculate_centrality_measures(n_political, 'Political Blogs')
    calculate_centrality_measures(n_neural, 'Neural Network')
    calculate_centrality_measures(n_internet, 'Internet')
    calculate_centrality_measures(n_lesmis, 'Les Miserables')

    # Create random graphs, Erdos-Renyi and Barabasi-Albert (#2)
    n_er1 = ig.Graph.Erdos_Renyi(n=20, p=0.01)
    n_er2 = ig.Graph.Erdos_Renyi(n=40, p=0.01)
    n_ba1 = ig.Graph.Barabasi(n=20)
    n_ba2 = ig.Graph.Barabasi(n=40)

    # Calculate descriptive statistics
    calculate_descriptive_statistics(n_er1, 'Erdos_Renyi_20')
    calculate_descriptive_statistics(n_er2, 'Erdos_Renyi_40')
    calculate_descriptive_statistics(n_ba1, 'Barabasi_Albert_20')
    calculate_descriptive_statistics(n_ba2, 'Barabasi_Albert_40')

    # Create plot of eigenvectors
    plot_eigenvectors(n_er1, 'Erdos_Renyi_20')
    plot_eigenvectors(n_ba1, 'Barabasi_Albert_20')


# Problem 1 centrality measures
# Degree, Eccentricity, Closeness, Betweeness
# Katz Index, PageRank, Kleinberg's Authority Score
# Kleinberg's Hub Score
def calculate_centrality_measures(network, network_name):

    # "_" are self reference method calls

    vs_degree = network.vs.select(_degree=max(network.degree()))['label']
    vs_eccentric = network.vs.select(
        _eccentricity=max(network.eccentricity()))['label']
    vs_closeness = network.vs.select(
        _closeness=max(network.closeness()))['label']

    # Need to check if directed or not for these methods
    if network.is_directed():
        vs_betweenness = network.vs.select(
            _betweenness=max(network.betweenness()))['label']
        vs_katz = network.vs.select(_eigenvector_centrality=max(
            network.eigenvector_centrality()))['label']
        vs_pagerank = network.vs.select(_personalized_pagerank=max(
            network.personalized_pagerank()))['label']
    else:
        vs_betweenness = network.vs.select(_betweenness=max(
            network.betweenness(directed=False)))['label']
        vs_katz = network.vs.select(_eigenvector_centrality=max(
            network.eigenvector_centrality(directed=False)))['label']
        vs_pagerank = network.vs.select(_personalized_pagerank=max(
            network.personalized_pagerank(directed=False)))['label']

    # Get list of authority scores, find max index, grab label at index
    auth = network.authority_score()
    vs_authority = network.vs[auth.index(max(auth))]['label']

    # Get list of hub scores, find max index, grab label at index
    hub = network.hub_score()
    vs_hub = network.vs[hub.index(max(hub))]['label']

    print(network_name + ': ', vs_degree, vs_eccentric, vs_closeness,
          vs_betweenness, vs_katz, vs_pagerank, vs_authority, vs_hub, '\n')


# Problem 2 Parst 1 and 2 statistics
# n = number of nodes, m = number of edges
# dmin = min degree, dmax = max degree
# l_avg = average path length, D = diameter
# ccg = global clustering coefficient
# eig_2nd = second smallest eigenvalue, eig_max = largest eigenvalue
def calculate_descriptive_statistics(network, network_name):

    n = network.vcount()
    m = network.ecount()
    dmin = min(network.degree())
    dmax = network.maxdegree()
    l_avg = network.average_path_length(directed=False)
    D = network.diameter(directed=False)
    ccg = network.transitivity_undirected()

    # Store the eigenvalues and eigenvectors of laplacian matrix
    values, vectors = la.eig(network.laplacian())

    # For second smallest, sort eigenvalues and select value at index 1
    values = sorted(values)
    eigval_2nd = values[1]
    eigval_max = max(values)

    print(network_name + ': ', n, m, dmin, dmax,
          l_avg, D, ccg, eigval_2nd, eigval_max, '\n')


# Problem 2 Part 3
# Plots the eigenvector for eigval_max and eigval_2nd
def plot_eigenvectors(network, network_name):

    # Store the eigenvalues and eigenvectors of laplacian matrix
    values, vectors = la.eig(network.laplacian())

    # Get vector for largest eigenvalue
    eigvec_max = vectors[:, list(values).index(max(values))]

    # Get vector for second smallest eigenvalue
    values = sorted(values)
    eigvec_2nd = vectors[:, list(values).index(values[1])]

    # Create scatter plot
    plt.title(network_name)
    plt.xlabel('Vertex ID')
    plt.ylabel('Eigenvector Value')
    plt.scatter(np.arange(0, 20, 1), eigvec_max, color='blue')
    plt.scatter(np.arange(0, 20, 1), eigvec_2nd, color='green')
    plt.show()


# Start program exection at main
if __name__ == '__main__':
    main()
