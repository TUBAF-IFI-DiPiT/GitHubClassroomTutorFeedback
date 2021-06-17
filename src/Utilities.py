from pathlib import Path

def getrepofolder(repo, basic_folder):
    data_root_dir = Path(basic_folder, repo.full_name.split('/')[-1])
    return data_root_dir

def getTeamName(repo, whitelist):
    repo_name = repo.full_name.split('/')[-1]
    team_name = "".join(repo_name.split('-')[1:])
    return team_name
    
def getTaskName(repo):
    repo_name = repo.full_name.split('/')[-1]
    return int(repo_name.split('_')[1].replace("aufgabe", ""))

def annoymizeDataFrame(raw_df, teams_dict, authors_dict):
    df = raw_df.copy()
    if 'author' in df.columns:
        df['authorKey'] = df['author'].apply(lambda s: authors_dict.get(s) if s in authors_dict else s)
    if 'team' in df.columns:
        df['teamKey'] = df['team'].apply(lambda s: teams_dict.get(s) if s in teams_dict else s)
    return df