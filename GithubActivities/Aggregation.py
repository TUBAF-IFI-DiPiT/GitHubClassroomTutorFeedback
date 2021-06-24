from pathlib import Path
import pandas as pd
import pickle
import sys
from github2pandas.issues import Issues
from github2pandas.pull_requests import PullRequests
from github2pandas.version import Version
from github2pandas.workflows import Workflows
from github2pandas.utility import Utility
from github2pandas.git_releases import GitReleases
from Utilities import getrepofolder

class RawDataAggregator():

    def __init__(self, dataHandler):
        self.raw_pdUsers = pd.DataFrame()
        self.raw_pdCommits = pd.DataFrame()
        self.raw_pdEdits = pd.DataFrame()
        self.raw_pdReleases = pd.DataFrame()
        self.raw_pdIssues = pd.DataFrame()
        self.raw_pdBranches = pd.DataFrame()
        self.raw_pdPullRequests = pd.DataFrame()
        self.dataHandler = dataHandler
        self.relevant_repos = []
        self.getTeamNameFunction = None
        self.getTaskNameFunction = None
        self.aggregateRepoList()

    def run(self):
        self.aggregateData()
        self.save_raw_data()

    def aggregateRepoList(self):
        git_repo_owner = self.dataHandler.pro_conf.git_repo_owner
        relevant_repos = []
        for repo_name in self.dataHandler.pro_conf.repos:
            git_repo_name = repo_name
            print(git_repo_owner, git_repo_name)
            repo = Utility.get_repo(git_repo_owner, git_repo_name, 
                                    self.dataHandler.pro_conf.github_token, 
                                    self.dataHandler.pro_conf.basic_folder)
            relevant_repos.append(repo)
        self.relevant_repos = relevant_repos

    def set_team_name_extractor_function(self, f):
        self.getTeamNameFunction = f


    def set_task_name_extractor_function(self, f):
        self.getTaskNameFunction = f

    def aggregateData(self):

        for repo in self.relevant_repos:
            repo_folder = getrepofolder(repo, self.dataHandler.pro_conf.basic_folder)
            if self.getTeamNameFunction:
                team_name = self.getTeamNameFunction(repo, self.dataHandler)
            else:
                sys.exit("Missing getTeamNameFunction Function!")
            if self.getTaskNameFunction:
                task_name = self.getTaskNameFunction(repo, self.dataHandler)
            else:
                sys.exit("Missing getTeamNameFunction Function!")

            Version.no_of_proceses = 4
            Version.clone_repository(repo=repo, data_root_dir=repo_folder, 
                                     github_token=self.dataHandler.pro_conf.github_token)
            Version.generate_version_pandas_tables(repo = repo, data_root_dir=repo_folder)

            team_users = Utility.get_users(repo_folder)
            team_users['team'] = team_name
            self.raw_pdUsers = self.raw_pdUsers.append(team_users, ignore_index=True)
            
            team_commits = Version.get_version(repo_folder)
            team_commits['team'] = team_name
            team_commits['task'] = task_name
            self.raw_pdCommits = self.raw_pdCommits.append(team_commits, ignore_index=True)
            
            team_edits = Version.get_version(repo_folder, Version.VERSION_EDITS)
            team_edits['team'] = team_name
            team_edits['task'] = task_name
            self.raw_pdEdits = self.raw_pdEdits.append(team_edits, ignore_index=True)
            
            GitReleases.generate_git_releases_pandas_tables(repo, repo_folder)
            git_releases = GitReleases.get_git_releases(repo_folder) 
            git_releases['team'] = team_name
            git_releases['task'] = task_name
            self.raw_pdReleases = self.raw_pdReleases.append(git_releases, ignore_index=True)

            Issues.generate_issue_pandas_tables(repo, repo_folder)
            git_issues = GitReleases.get_git_releases(repo_folder) 
            git_issues['team'] = team_name
            git_issues['task'] = task_name
            self.raw_pdIssues = self.raw_pdIssues.append(git_issues, ignore_index=True)

            git_branches = Version.get_version(repo_folder, filename=Version.VERSION_BRANCHES)
            git_branches['team'] = team_name
            git_branches['task'] = task_name
            self.raw_pdBranches = self.raw_pdBranches.append(git_branches, ignore_index=True)

            PullRequests.generate_pull_request_pandas_tables(repo, repo_folder)
            git_pullrequests = PullRequests.get_pull_requests(repo_folder)
            git_pullrequests['team'] = team_name
            git_pullrequests['task'] = task_name
            self.raw_pdPullRequests = self.raw_pdPullRequests.append(git_pullrequests, ignore_index=True)        
            
        self.raw_pdUsers.drop(["email"], axis = 1, inplace = True)
        self.raw_pdUsers.drop_duplicates(subset=['anonym_uuid', 'id', 'login', 'team'], inplace = True)
        self.raw_pdCommits.drop(["committer_timezone"], axis = 1, inplace = True)

        self.save_raw_data()

    def save_raw_data(self):
        self.dataHandler.pickle_File_To_Raw_Data_Folder(self.raw_pdCommits, "raw_pdCommits.p")
        self.dataHandler.pickle_File_To_Raw_Data_Folder(self.raw_pdUsers, "raw_pdUsers.p")
        self.dataHandler.pickle_File_To_Raw_Data_Folder(self.raw_pdReleases, "raw_pdReleases.p")
        self.dataHandler.pickle_File_To_Raw_Data_Folder(self.raw_pdEdits, "raw_pdEdits.p")
        self.dataHandler.pickle_File_To_Raw_Data_Folder(self.raw_pdPullRequests, "raw_pdPullRequests.p")
        self.dataHandler.pickle_File_To_Raw_Data_Folder(self.raw_pdBranches, "raw_pdBranches.p")
        self.dataHandler.pickle_File_To_Raw_Data_Folder(self.raw_pdIssues, "raw_pdIssues.p")  

    def __str__(self):
        output = "\n"
        output += "---------------------------------------\n"
        output += "Raw Data Aggregation\n"
        output += f"{len(self.relevant_repos)} repos found! \n"
        output += "---------------------------------------\n" 
        return output

    def load_raw_data(self):
        self.raw_pdCommits = self.dataHandler.unpickle_From_Raw_Data_Folder("raw_pdCommits.p")
        self.raw_pdUsers = self.dataHandler.unpickle_From_Raw_Data_Folder("raw_pdUsers.p")
        self.raw_pdReleases = self.dataHandler.unpickle_From_Raw_Data_Folder("raw_pdReleases.p")
        self.raw_pdEdits = self.dataHandler.unpickle_From_Raw_Data_Folder("raw_pdEdits.p")
        self.raw_pdIssues = self.dataHandler.unpickle_From_Raw_Data_Folder("raw_pdIssues.p")
        self.raw_pdBranches = self.dataHandler.unpickle_From_Raw_Data_Folder("raw_pdBranches.p")
        self.raw_pdPullRequests = self.dataHandler.unpickle_From_Raw_Data_Folder("raw_pdPullRequests.p")