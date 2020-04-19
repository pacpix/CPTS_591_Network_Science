"""
Justin Stachofsky
Dr. Gebremedhin
CPTS 591
5 May 2020
Create gml file from GitHub html pages
"""

# stdlib
import csv
import os
import glob

# Third Party Libraries
from bs4 import BeautifulSoup as bs
import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms import bipartite
import numpy as np
import pandas as pd

# CSV Filenames
social_nodes_file = 'social_nodes.csv'
technical_nodes_file = 'technical_nodes.csv'
connections_file = 'connections.csv'
technical_connections_file = 'technical_connections.csv'


# Main program flow
def main():

    # Build csv of individual connections and csv of unique nodes
    create_csv_files()
    # Creates graph and writes it to gml file
    create_gml_file()


# Adds technical node to technical node connections
def append_technical_connections():

    with open(connections_file, 'a') as confile:
        with open(technical_connections_file, 'r') as techfile:
            csv_reader = csv.reader(techfile)
            for row in csv_reader:
                # Connects repo to repo
                csv_writer = csv.writer(confile, delimiter=',')
                csv_writer.writerow(row)


# Append lines to connections csv
def append_to_connections_csv(repo_node, contributor_list):

    with open(connections_file, 'a') as csv_file:
        # Connects developer to repo
        csv_writer = csv.writer(csv_file, delimiter=',')
        for contributor in contributor_list:
            csv_writer.writerow([contributor, repo_node])


# Append lines to nodes csv
def append_to_nodes_csv(repo_node, contributor_list):

    with open(technical_nodes_file, 'a') as csv_file:
        # Add repo node
        csv_writer = csv.writer(csv_file, delimiter=',')
        csv_writer.writerow([repo_node])

    with open(social_nodes_file, 'a') as csv_file:
        # Add contributor nodes
        csv_writer = csv.writer(csv_file, delimiter=',')
        for contributor in contributor_list:
            csv_writer.writerow([contributor])


# Create CSV of connections
def create_csv_files():

    # Add title row to social nodes csv file
    with open(social_nodes_file, mode='w+') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        csv_writer.writerow(['Name'])

    # Add title row to technical nodes csv file
    with open(technical_nodes_file, mode='w+') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        csv_writer.writerow(['Name'])

    # Add title row to connections csv file
    with open(connections_file, mode='w+') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        csv_writer.writerow(['Source_Node', 'Destination_Node'])

    # Path to htm files with contributor lists
    path = os.getcwd() + '/Repository_Contributors_2020-04-13/*.htm'

    # Glob is list of htm files at path
    for htm in glob.glob(path):
        repo = get_repo_name(htm)
        contributors = get_repo_contributors(htm)
        append_to_nodes_csv(repo, contributors)
        append_to_connections_csv(repo, contributors)

    # Remove duplicate nodes from csv
    remove_duplicate_nodes(social_nodes_file)
    remove_duplicate_nodes(technical_nodes_file)

    # Remove bot users from nodes and connections
    remove_bot_users(social_nodes_file)
    remove_bot_users(connections_file)

    # Add technical connections manually
    append_technical_connections()


def create_gml_file():

    # Create lists of social nodes, technical nodes, and connections
    with open(social_nodes_file, mode='r') as sn_file:
        next(sn_file)
        social_nodes = [line.rstrip('\n') for line in sn_file]

    with open(technical_nodes_file, mode='r') as tn_file:
        next(tn_file)
        technical_nodes = [line.rstrip('\n') for line in tn_file]

    with open(connections_file, mode='r') as con_file:
        csv_reader = csv.reader(con_file)
        next(csv_reader)
        connections = [tuple(row) for row in csv_reader]

    # Create graph add nodes and edges
    st_graph = nx.DiGraph()
    st_graph.add_nodes_from(social_nodes, bipartite=0)
    st_graph.add_nodes_from(technical_nodes, bipartite=1)
    st_graph.add_edges_from(connections)

    # Write network to gml file
    nx.write_gml(st_graph, 'st_graph.gml')


# Get list of repo contributors from htm file
def get_repo_contributors(fname):

    # The contributor names are in the 'alt' attribute of each img tag
    with open(fname, 'r') as file:
        contents = file.read()
        soup = bs(contents, features='lxml')
        contributors = [img.get('alt') for img in soup.find_all(
            'img', {'class': 'avatar mr-2', 'alt': True})]

    return contributors


# Get repo name from file name
def get_repo_name(fname):

    # Get file name without path and extension
    repo = os.path.basename(fname)
    repo = os.path.splitext(repo)[0]

    return repo

# Remove bot users from nodes and connections
def remove_bot_users(bot_file):

    bot_users = ['@dependabot', '@jake-the-bot', '@jongleberry-bot', 
                '@persistbot', '@dependabot-preview', '@vue-bot']

    with open(bot_file, 'r') as infile, open('temp.csv', 'w+') as outfile:
        for line in infile:
            if not any(bot in line for bot in bot_users):
                outfile.write(line)
    
    os.system('mv temp.csv %s' %str(bot_file))

# Remove duplicate nodes from nodes csv
def remove_duplicate_nodes(dupe_file):

    csv_file = pd.read_csv(dupe_file)
    csv_file.drop_duplicates(inplace=True)
    csv_file.to_csv(dupe_file, index=False)


# Start program exection at main
if __name__ == '__main__':
    main()
