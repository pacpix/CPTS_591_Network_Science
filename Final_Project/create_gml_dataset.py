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

# Main program flow
def main():
    
    create_connections_csv()


# Create CSV of connections
def create_connections_csv():

    # Path to htm files with contributor lists
    path = os.getcwd() + '/Repository_Contributors_2020-04-13/*.htm'

    # Glob is list of htm files at path
    for htm in glob.glob(path):
        repo = get_repo_name(htm)
        contributors = get_repo_contributors(htm)
        print(repo)
        print(contributors)
        print('+++++++++++++++++++++++++')

# Get repo name from file name
def get_repo_name(fname):
    
    # Get file name without path
    # Return file name without extension
    repo = os.path.basename(fname)
    return os.path.splitext(repo)[0]

# Get list of repo contributors from htm file
def get_repo_contributors(fname):
    
    # The contributor names are in the 'alt' attribute of each img tag
    with open(fname, 'r') as file:
        contents = file.read()
        soup = bs(contents, features='lxml')
        contributors = [img.get('alt') for img in soup.find_all('img', {'class':'avatar mr-2', 'alt':True})]
    
    return contributors
 

# Start program exection at main
if __name__ == '__main__':
    main()
