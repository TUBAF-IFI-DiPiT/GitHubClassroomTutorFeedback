from pathlib import Path
import argparse
import os

def getrepofolder(repo, basic_folder):
    data_root_dir = Path(basic_folder, repo.full_name.split('/')[-1])
    return data_root_dir

def annoymizeDataFrame(raw_df, teams_dict, authors_dict):
    df = raw_df.copy()
    if 'author' in df.columns:
        df['authorKey'] = df['author'].apply(lambda s: authors_dict.get(s) if s in authors_dict else s)
    if 'team' in df.columns:
        df['teamKey'] = df['team'].apply(lambda s: teams_dict.get(s) if s in teams_dict else s)
    return df

def check_file_path(file_path_name):
    if os.path.isfile(file_path_name):
        return file_path_name
    else:
        raise argparse.ArgumentTypeError(f"{file_path_name} is not a valid file")
