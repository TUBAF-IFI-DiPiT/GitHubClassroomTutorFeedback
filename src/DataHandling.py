import yaml
from pathlib import Path
import pickle

class DataHandling:

    def __init__(self, project_folder_name, project_parameter_file):
        print("Loading parameter file ... " + project_folder_name + project_parameter_file)
        with open(project_folder_name + project_parameter_file, "r") as f:
            parameter_yml = yaml.load(f, Loader=yaml.FullLoader)

        self.repos = dict((key,d[key]) for d in parameter_yml["repos"] for key in d)
        self.whitelist_pattern = self.repos.keys()
        self.blacklist_pattern = parameter_yml["blacklist"]

        self.basic_folder = Path(project_folder_name, 
                            parameter_yml["rawDataFolder"])
        self.rawDataFolder = Path(project_folder_name, 
                            parameter_yml["extractedDataFolder"])
        self.rawDataFolder.mkdir(parents=True, exist_ok=True)

        self.preprocDataFolder = Path(project_folder_name, 
                            parameter_yml["preprocessedDataFolder"])
        self.preprocDataFolder.mkdir(parents=True, exist_ok=True)        
  
    def pickle_File(self, dataFrame, path):
        with path.open('wb') as fp:
            pickle.dump(dataFrame, fp)
        
    def pickle_File_To_Raw_Data_Folder(self, dataFrame, filename):
        path = Path.joinpath(self.rawDataFolder, filename)
        self.pickle_File(dataFrame, path)

    def pickle_File_To_Preproc_Data_Folder(self, dataFrame, filename):
        path = Path.joinpath(self.preprocDataFolder, filename)
        self.pickle_File(dataFrame, path)        
        
    def unpickle_file(self, path):
        with path.open('rb') as fp:
            content = pickle.load(fp)
        return content
    
    def unpickle_From_Raw_Data_Folder(self, filename):
        path = Path.joinpath(self.rawDataFolder, filename)
        return self.unpickle_file(path)
    
    def unpickle_From_Preproc_Data_Folder(self, filename):
        path = Path.joinpath(self.preprocDataFolder, filename)
        return self.unpickle_file(path)