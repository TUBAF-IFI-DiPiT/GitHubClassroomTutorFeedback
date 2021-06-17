from github2pandas.issues import Issues
from github2pandas.pull_requests import PullRequests
from github2pandas.version import Version
from github2pandas.workflows import Workflows
from github2pandas.utility import Utility
from github2pandas.git_releases import GitReleases
from pathlib import Path
import pandas as pd
import os
from DataHandling import DataHandling
from Utilities import getrepofolder, getTeamName, getTaskName


def aggregateRepoList(dataHandler, github_token):

    relevant_repos = Utility.get_repos(github_token, 
                                        dataHandler.basic_folder,
                                        dataHandler.whitelist_pattern,
                                        dataHandler.blacklist_pattern)
    return relevant_repos

if __name__ == "__main__":
    project_folder_name = "data/"
    project_parameter_file = "parameter.yml"
    dataHandler = DataHandling(project_folder_name, project_parameter_file)
    github_token = os.environ['TOKEN']
    relevant_repos = aggregateRepoList(dataHandler, github_token)
    print("{} repos found!".format(len(relevant_repos)))

