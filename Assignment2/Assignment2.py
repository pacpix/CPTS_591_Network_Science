"""
Justin Stachofsky
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
import matplotlib.pyplot as plt


# Main program flow
def main():

    # Create networks from gml datasets
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


# Problem 1 centrality measures
# Degree, Eccentricity, Closeness, Betweeness
# Katz Index, PageRank, Kleinberg's Authority Score
# Kleinberg's Hub Score
def calculate_centrality_measures(network, network_name):

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


# Start program exection at main
if __name__ == '__main__':
    main()
