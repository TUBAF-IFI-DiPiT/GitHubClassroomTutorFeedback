import os
import sys
sys.path.append(os.path.join(sys.path[0],'..','..','GithubActivities'))
from DataHandling import DataManager
from Aggregation import RawDataAggregator
from FeedbackGeneration import FeedbackGenerator

def getTeamName(repo, datahandler):
    repo_name = repo.full_name.split('/')[-1]
    team_name = "".join(repo_name.split('-')[1:])
    return team_name
    
def getTaskName(repo, datahandler):
    repo_name = repo.full_name.split('/')[-1]
    return int(repo_name.split('_')[1].replace("aufgabe", ""))

def main():
    dm = DataManager()
    dm.pro_conf.set_github_token(os.environ['EXT_TOKEN'])
    print(dm)
    rda = RawDataAggregator(dm)
    rda.set_team_name_extractor_function(getTeamName)
    rda.set_task_name_extractor_function(getTaskName)
    rda.run()
    print(rda)
    fg = FeedbackGenerator(dm)
    print(fg)
    fg.run_notebooks()
    fg.map_results_on_feedback()
    
if __name__ == "__main__":
    main()