import yaml
import sys
from pathlib import Path
import pickle
import argparse
import Utilities

class ProjectConfiguration:

    def __init__(self, project_parameter_file):

        with open(project_parameter_file, "r") as f:
            parameter_yml = yaml.load(f, Loader=yaml.FullLoader)

        self.project_name = parameter_yml["project_name"]
        # Generating folder structure
        self.project_folder_name = parameter_yml["project_folder"]

        self.basic_folder = Path(self.project_folder_name, 
                            parameter_yml["rawDataFolder"])
        self.rawDataFolder = Path(self.project_folder_name, 
                            parameter_yml["extractedDataFolder"])
        self.rawDataFolder.mkdir(parents=True, exist_ok=True)

        self.preprocDataFolder = Path(self.project_folder_name, 
                            parameter_yml["preprocessedDataFolder"])
        self.preprocDataFolder.mkdir(parents=True, exist_ok=True)      

        # Generate repo list
        self.repos = parameter_yml["repos"]
        #self.repos = dict((key,d[key]) for d in parameter_yml["repos"] for key in d)
        #self.whitelist_pattern = self.repos.keys()
        
        self.repo_black_pattern = parameter_yml["repo_black_pattern"]
        self.repo_white_pattern = parameter_yml["repo_white_pattern"]

        self.git_repo_owner = parameter_yml["git_repo_owner"]
        self.github_token = ""
        self.github_users_black_list = parameter_yml["github_users_black_list"]

        self.processing_notebooks = parameter_yml["processing_notebooks"]
        self.processing_notebooks_folder = parameter_yml["processing_notebooks_folder"]

        self.feedback_template_file = parameter_yml["feedback_template_file"]
        self.feedback_result_file = parameter_yml["feedback_result_file"]

    def set_github_token(self, github_token):
        self.github_token = github_token

    def __str__(self):
        output = "\n"
        output += "---------------------------------------\n"
        output += "Project Configuration\n"
        output += "Project name  : " + self.project_name + "\n" 
        output += "Project folder: " + self.project_folder_name + "\n" 
        output += "---------------------------------------\n" 
        return output


class ProjectConfigurationFromCommandline(ProjectConfiguration):

    def __init__(self):
        parsed_args = self.parse_arguments()
        self.project_parameter_file = parsed_args.path
        super().__init__(self.project_parameter_file)

    def parse_arguments(self):
        parser = argparse.ArgumentParser(description='Process command line arguments.')
        parser.add_argument('-path', type=Utilities.check_file_path, help= 'paste path to .yml config file')
        return parser.parse_args()

class DataManager():

    def __init__(self, parameter_file_name = None):
        if parameter_file_name:
            if Utilities.check_file_path(parameter_file_name):
                self.pro_conf = ProjectConfiguration(parameter_file_name)
        else:
            if len(sys.argv) > 1:
                self.pro_conf = ProjectConfigurationFromCommandline()
            else:
                sys.exit("No valid configuration parameter file")

    def __str__(self):
        return self.pro_conf.__str__()

    def pickle_File(self, dataFrame, path):
        with path.open('wb') as fp:
            pickle.dump(dataFrame, fp)
        
    def pickle_File_To_Raw_Data_Folder(self, dataFrame, filename):
        path = Path.joinpath(self.pro_conf.rawDataFolder, filename)
        self.pickle_File(dataFrame, path)

    def pickle_File_To_Preproc_Data_Folder(self, dataFrame, filename):
        path = Path.joinpath(self.pro_conf.preprocDataFolder, filename)
        self.pickle_File(dataFrame, path)        
        
    def unpickle_file(self, path):
        with path.open('rb') as fp:
            content = pickle.load(fp)
        return content
    
    def unpickle_From_Raw_Data_Folder(self, filename):
        path = Path.joinpath(self.pro_conf.rawDataFolder, filename)
        return self.unpickle_file(path)
    
    def unpickle_From_Preproc_Data_Folder(self, filename):
        path = Path.joinpath(self.pro_conf.preprocDataFolder, filename)
        return self.unpickle_file(path)