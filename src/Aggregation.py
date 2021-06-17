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
    
    git_repo_owner = dataHandler.git_repo_owner

    relevant_repos = []
    for repo_name in dataHandler.repos:
        git_repo_name = repo_name
        git_repo_name = "softwareentwicklung_aufgabe3_sose2021_mb-camo"
        git_repo_owner = "Ifi-Softwareentwicklung-SoSe2021"
        print(git_repo_owner, git_repo_name)
        repo = Utility.get_repo(git_repo_owner, git_repo_name, github_token, dataHandler.basic_folder)
        relevant_repos.append(repo)
    return relevant_repos


def aggregateData(relevant_repos, dataHandler):
    raw_pdUsers = pd.DataFrame()
    raw_pdCommits = pd.DataFrame()
    raw_pdEdits = pd.DataFrame()
    raw_pdReleases = pd.DataFrame()
    raw_pdIssues = pd.DataFrame()
    raw_pdBranches = pd.DataFrame()
    raw_pdPullRequests = pd.DataFrame()

    for repo in relevant_repos:
        repo_folder = getrepofolder(repo, dataHandler.basic_folder)
        Version.no_of_proceses = 4
        Version.clone_repository(repo=repo, data_root_dir=repo_folder, github_token=github_token)
        Version.generate_version_pandas_tables(repo = repo, data_root_dir=repo_folder)

        team_users = Utility.get_users(repo_folder)
        team_users['team'] = getTeamName(repo, dataHandler.whitelist_pattern)
        raw_pdUsers = raw_pdUsers.append(team_users, ignore_index=True)
        
        team_commits = Version.get_version(repo_folder)
        team_commits['team'] = getTeamName(repo, dataHandler.whitelist_pattern)
        team_commits['task'] = getTaskName(repo)
        raw_pdCommits = raw_pdCommits.append(team_commits, ignore_index=True)
        
        team_edits = Version.get_version(repo_folder, Version.VERSION_EDITS)
        team_edits['team'] = getTeamName(repo, dataHandler.whitelist_pattern)
        team_edits['task'] = getTaskName(repo)
        raw_pdEdits = raw_pdEdits.append(team_edits, ignore_index=True)
        
        GitReleases.generate_git_releases_pandas_tables(repo, repo_folder)
        git_releases = GitReleases.get_git_releases(repo_folder) 
        git_releases['team'] = getTeamName(repo, dataHandler.whitelist_pattern)
        git_releases['task'] = getTaskName(repo)
        raw_pdReleases = raw_pdReleases.append(git_releases, ignore_index=True)

        Issues.generate_issue_pandas_tables(repo, repo_folder)
        git_issues = GitReleases.get_git_releases(repo_folder) 
        git_issues['team'] = getTeamName(repo, dataHandler.whitelist_pattern)
        git_issues['task'] = getTaskName(repo)
        raw_pdIssues = raw_pdIssues.append(git_issues, ignore_index=True)

        git_branches = Version.get_version(repo_folder, filename=Version.VERSION_BRANCHES)
        git_branches['team'] = getTeamName(repo, dataHandler.whitelist_pattern)
        git_branches['task'] = getTaskName(repo)
        raw_pdBranches = raw_pdBranches.append(git_branches, ignore_index=True)

        PullRequests.generate_pull_request_pandas_tables(repo, repo_folder)
        git_pullrequests = PullRequests.get_pull_requests(repo_folder)
        git_pullrequests['team'] = getTeamName(repo, dataHandler.whitelist_pattern)
        git_pullrequests['task'] = getTaskName(repo)
        raw_pdPullRequests = raw_pdPullRequests.append(git_pullrequests, ignore_index=True)        
        
    raw_pdUsers.drop(["email"], axis = 1, inplace = True)
    raw_pdUsers.drop_duplicates(subset=['anonym_uuid', 'id', 'login', 'team'], inplace = True)
    raw_pdCommits.drop(["committer_timezone"], axis = 1, inplace = True)

    dataHandler.pickle_File_To_Raw_Data_Folder(raw_pdCommits, "raw_pdCommits.p")
    dataHandler.pickle_File_To_Raw_Data_Folder(raw_pdUsers, "raw_pdUsers.p")
    dataHandler.pickle_File_To_Raw_Data_Folder(raw_pdReleases, "raw_pdReleases.p")
    dataHandler.pickle_File_To_Raw_Data_Folder(raw_pdEdits, "raw_pdEdits.p")
    dataHandler.pickle_File_To_Raw_Data_Folder(raw_pdIssues, "raw_pdIssues.p")
    dataHandler.pickle_File_To_Raw_Data_Folder(raw_pdBranches, "raw_pdBranches.p")
    dataHandler.pickle_File_To_Raw_Data_Folder(raw_pdPullRequests, "raw_pdPullRequests.p")

if __name__ == "__main__":
    project_folder_name = "data/"
    project_parameter_file = "parameter.yml"

    dataHandler = DataHandling(project_folder_name, project_parameter_file)
    github_token = os.environ['TOKEN']
    relevant_repos = aggregateRepoList(dataHandler, github_token)
    print("{} repos found!".format(len(relevant_repos)))

    aggregateData(relevant_repos=relevant_repos, dataHandler=dataHandler)


