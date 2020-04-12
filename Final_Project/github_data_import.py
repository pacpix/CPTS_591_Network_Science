"""
Justin Stachofsky
Dr. Gebremedhin
CPTS 591
5 May 2020
Import data from GitHub
"""

# File with API credentials
import config

# Third Party Libraries
from github import Github

# Main program flow
def main():
    gh = Github(config.token)

    for repo in gh.get_user().get_repos():
        print(repo.name)

# Start program exection at main
if __name__ == '__main__':
    main()
