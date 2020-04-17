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
import networkx as nx
from bs4 import BeautifulSoup as bs
import pandas as pd

# Main program flow
def main():
    
    # Build csv of individual connections and csv of unique nodes
    create_csv_files()
    
    
# Create CSV of connections
def create_csv_files():

    # Add title row to nodes csv file
    with open('unique_nodes.csv', mode='w+') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        csv_writer.writerow(['Name', 'Technical'])
    
    # Add title row to connections csv file
    with open('connections.csv', mode='w+') as csv_file:
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
    
    # Remove duplicate nodes from nodes csv
    remove_duplicate_nodes()

    # Add technical connections manually
    append_technical_connections()
    

# Append lines to connections csv 
def append_to_connections_csv(repo_node, contributor_list):

    with open('connections.csv', 'a') as csv_file:
        # Connects developer to repo
        csv_writer = csv.writer(csv_file, delimiter=',') 
        for contributor in contributor_list:
            csv_writer.writerow([contributor, repo_node])


# Append lines to nodes csv 
def append_to_nodes_csv(repo_node, contributor_list):

    with open('unique_nodes.csv', 'a') as csv_file:
        # Add repo node
        csv_writer = csv.writer(csv_file, delimiter=',') 
        csv_writer.writerow([repo_node, 1])
        
        # Add contributor nodes
        for contributor in contributor_list:
            csv_writer.writerow([contributor, 0])


def append_technical_connections():
    
    with open('connections.csv', 'a') as confile:
        with open('technical_connections.csv', 'r') as techfile:
            csv_reader = csv.reader(techfile)
            for row in csv_reader:
                # Connects repo to repo
                csv_writer = csv.writer(confile, delimiter=',') 
                csv_writer.writerow(row)


# Get list of repo contributors from htm file
def get_repo_contributors(fname):
    
    # The contributor names are in the 'alt' attribute of each img tag
    with open(fname, 'r') as file:
        contents = file.read()
        soup = bs(contents, features='lxml')
        contributors = [img.get('alt') for img in soup.find_all('img', {'class':'avatar mr-2', 'alt':True})]
    
    return contributors


# Get repo name from file name
def get_repo_name(fname):
    
    # Get file name without path and extension
    repo = os.path.basename(fname)
    repo = os.path.splitext(repo)[0]
    
    return repo


# Remove duplicate nodes from nodes csv
def remove_duplicate_nodes():

    csv_file = pd.read_csv('unique_nodes.csv')
    csv_file.drop_duplicates(inplace=True)
    csv_file.to_csv('unique_nodes.csv', index=False)


# Start program exection at main
if __name__ == '__main__':
    main()
