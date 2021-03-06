import argparse
from pathlib import Path
import os
import sys

from github2pandas_manager.config_parser import YAML_RequestDefinition
from github2pandas_manager import utilities

sys.path.append(os.path.join(sys.path[0],'FeedbackGeneration'))
from FeedbackGenerator import FeedbackGenerator

from github2pandas_manager.config_parser import YAML_RequestDefinition
from github2pandas_manager.repository_handler import RequestHandlerFactory
from github2pandas_manager.data_extractor import Github_data_extractor
from github2pandas_manager.data_merger import Github_data_merger
from github2pandas_manager import utilities

def call_github2pandas_manager(request_params, github_token):
    project_folder = Path(request_params.parameters.project_folder)
    project_folder.mkdir(parents=True, exist_ok=True)

    request_handler = \
        RequestHandlerFactory.get_request_handler(
                github_token=github_token,
                request_params=request_params
            )

    print(f"{len(request_handler.repository_list)} machting repositories found.")

    if len(request_handler.repository_list) > 0:
        data_extractor = Github_data_extractor.start(
                github_token=github_token,
                request_handler=request_handler
        )
        
        df = Github_data_merger.merge(
            request_handler=request_handler
            )

def call_feedback_generation(request_params):
    project_folder = Path(request_params.parameters.project_folder)
    if not project_folder:
        print("Project folder and data set does not exist!")
    fg = FeedbackGenerator(request_params.parameters)
    print(fg)
    fg.run_notebooks()
    fg.map_results_on_feedback()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process command line arguments.')
    parser.add_argument('-path', dest='config_file',
                        type=utilities.check_file_path,
                        required=True,
                        help='paste path to .yml config file')

    arguments = parser.parse_args()
    request_params = YAML_RequestDefinition(arguments.config_file)
    
    if "TOKEN" in os.environ:
        print("Token found!")
    
    github_token = os.environ['TOKEN']

    call_github2pandas_manager(request_params=request_params, 
                               github_token=github_token)
    
    call_feedback_generation(request_params=request_params)
