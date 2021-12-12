import subprocess
from subprocess import check_call
from datetime import datetime
import re
import os

class FeedbackGenerator():

    def __init__(self, parameter):
        self.parameter = parameter

    def run_notebooks(self):
        for notebook in self.parameter.processing_notebooks:
            cmd = "pipenv run jupyter nbconvert --to notebook --execute"
            cmd += f" {self.parameter.processing_notebooks_folder}"
            cmd += f"{notebook}"
            process = subprocess.run(cmd.split(' '))
            process.returncode

    def map_results_on_feedback(self):
        with open(self.parameter.feedback_template_file) as f:
            template = f.read()

        dateTimeObj = datetime.now()
        template = template.replace('<S_TimeStamp>', str(dateTimeObj))  

        pattern = re.compile("<\w+.png>|<\w+.txt>")
        for tag in re.findall(pattern, template):
            file_type = tag[1:-1].split(".")[-1]
            file_name = tag[1:-1]

            print(os.getcwd())
            content_path = self.parameter.processing_notebooks_folder + file_name
            print("--------")
            print(content_path)
            if file_type=="txt":
               with open(content_path) as f:
                   content = f.read()
               template = template.replace(tag, content)
            if file_type=="png":
               content = f"![image]({content_path})"
               template = template.replace(tag, content)

        with open(self.parameter.feedback_result_file, "w") as f:
            f.write(template)

    def __str__(self):
        output = "\n"
        output += "---------------------------------------\n"
        output += "Feedback Generator\n"
        for notebook in self.parameter.processing_notebooks:
            output += f"{notebook}\n"
        output += "---------------------------------------\n" 
        return output