def getTeamName(complete_repo_name):
    repo_name = complete_repo_name.split('/')[-1]
    team_name = "".join(repo_name.split('-')[1:])
    return team_name

def getTaskName(complete_repo_name):
    repo_name = complete_repo_name.split('/')[-1]
    return int(repo_name.split('_')[1].replace("aufgabe", ""))