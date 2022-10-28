"""
Julia Stachofsky
Dr. Gebremedhin
CPTS 591
18 February 2020
Assignment 1
"""

# stdlib
import os

# Third party libraries
import igraph as ig
import numpy as np
import matplotlib.pyplot as plt


# Main program flow
def main():

    # Create networks from three gml datasets
    n_political = ig.Graph.Read(
        f=os.getcwd() + "/Datasets/polblogs.gml", format="gml")
    n_neural = ig.Graph.Read(
        f=os.getcwd() + "/Datasets/celegansneural.gml", format="gml")
    n_internet = ig.Graph.Read(
        f=os.getcwd() + "/Datasets/as-22july06.gml", format="gml")

    # Create Erdos-Renyi random networks
    n_er1 = ig.Graph.Erdos_Renyi(n=2000, p=0.01)
    n_er2 = ig.Graph.Erdos_Renyi(n=2000, p=0.005)
    n_er3 = ig.Graph.Erdos_Renyi(n=2000, p=0.0025)

    # Additional network(Question 4)
    n_lesmis = ig.Graph.Read(
        f=os.getcwd() + "/Datasets/lesmis.gml", format="gml")

    # Calculate descriptive statistics
    calculate_network_statistics(n_political, 'Political Blogs')
    calculate_network_statistics(n_neural, 'Neural Network')
    calculate_network_statistics(n_internet, 'Internet')
    calculate_network_statistics(n_er1, 'Erdos_Renyi #1')
    calculate_network_statistics(n_er2, 'Erdos_Renyi #2')
    calculate_network_statistics(n_er3, 'Erdos_Renyi #3')
    calculate_network_statistics(n_lesmis, 'Les Miserables')

    # Plot degree distributions
    plot_degree_distribution(n_political, 'Political Blogs')
    plot_degree_distribution(n_neural, 'Neural Network')
    plot_degree_distribution(n_internet, 'Internet')
    plot_degree_distribution(n_er1, 'Erdos_Renyi #1')
    plot_degree_distribution(n_er2, 'Erdos_Renyi #2')
    plot_degree_distribution(n_er3, 'Erdos_Renyi #3')
    plot_degree_distribution(n_lesmis, 'Les Miserables')

    # Plot path length distributions
    plot_pathlength_distribution(n_political, 'Political Blogs')
    plot_pathlength_distribution(n_neural, 'Neural Network')
    plot_pathlength_distribution(n_internet, 'Internet')
    plot_pathlength_distribution(n_er1, 'Erdos_Renyi #1')
    plot_pathlength_distribution(n_er1, 'Erdos_Renyi #2')
    plot_pathlength_distribution(n_er1, 'Erdos_Renyi #3')
    plot_pathlength_distribution(n_lesmis, 'Les Miserables')


# Used to calculate descriptive statistics (Question 1)
# n = number of nodes, m = number of links, c = number of connected components
# d = maximum degree, l_avg = average path length, L = diameter
# ccl = avg local clustering coefficient, ccg = global clustering coefficient
# If directed, calculate strong and week connected components for c
def calculate_network_statistics(network, network_name):

    n = network.vcount()
    m = network.ecount()

    if not network.is_directed():
        nettype = 'Undirected'
        c = len(network.components())
        L = network.diameter(directed=False)
        l_avg = network.average_path_length(directed=False)
    else:
        nettype = 'Directed'
        c_strong = len(network.components(mode='STRONG'))
        c_weak = len(network.components(mode='WEAK'))
        L = network.diameter()
        l_avg = network.average_path_length()

    d = network.maxdegree()
    ccl = network.transitivity_avglocal_undirected()
    ccg = network.transitivity_undirected()

    print(network_name + ':')
    if not network.is_directed():
        print(nettype, n, m, c, L, l_avg, d, ccl, ccg, '\n')
    else:
        print(nettype, n, m, c_strong, c_weak, L, l_avg, d, ccl, ccg, '\n')


# Used to plot pk k plot of degree distribution (Question 2)
def plot_degree_distribution(network, network_name):

    # density=True normalizes histogram
    plt.hist(network.degree(), density=True)

    # Formatting for historgram
    plt.xlabel('k')
    plt.ylabel('p(k)')
    plt.title(network_name)
    plt.show()


# Used to plot pl l plot of pathlength (Question 3)
# Supposedly network.path_length_hist returns a tuple
# However I only get a histogram object
# Thus cannot plot with matplotlib
def plot_pathlength_distribution(network, network_name):

    print(network_name)
    if not network.is_directed():
        print(network.path_length_hist(directed=False), '\n')
    else:
        print(network.path_length_hist(directed=True), '\n')


# Start program exection at main
if __name__ == "__main__":
    main()
