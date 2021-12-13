import argparse
from pathlib import Path
import os
import sys

from github2pandas_manager.config_parser import YAML_RequestDefinition
from github2pandas_manager import utilities

sys.path.append(os.path.join(sys.path[0],'FeedbackGeneration'))
from FeedbackGenerator import FeedbackGenerator

def main(request_params):
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
    main(request_params=request_params)