#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
sys.path.append(os.path.abspath('./'))
sys.path.append(os.path.abspath('../'))
sys.path.append(os.path.abspath('../../'))
import time
import shutil
import argparse
import pytest
from configparser import RawConfigParser
from framework.modules.commonVariables import *

current_dir = os.path.dirname(os.path.realpath(__file__))

def get_arguments():
    project_choices = ['demo']
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--env", action='store', dest='environment', default='dev', choices=['demo', 'dev', 'qa'], help='-e <environment>')
    parser.add_argument("--config", action='store', dest='config_path', help='--config <config_path>')
    parser.add_argument("-o", "--output", action='store', dest='output_type', default='both', choices=['html', 'allure', 'both'], help='-o <output>')
    parser.add_argument("-t", "--test", action='store', dest='test', help='-t <testCase>')
    parser.add_argument("-k", "--pattern", action='append', dest='patterns', help='-k methodname or pattern')
    parser.add_argument("-p", "--project", action='store', dest='project', choices=project_choices, required=True, help=f"-p ({project_choices})")
    arguments = parser.parse_args()
    arguments.project = arguments.project.lower()
    return arguments


class Trigger_Functional_Tests:

    def __init__(self, arguments, project):
        self.arguments = arguments
        self.project = project
        self.new_log_path = f"{framework_log_dir}{os.sep}{date}_{Time}-{project}.log"
        self.html_output = f"{framework_log_dir}{os.sep}{date}-{Time}-{project}.html"

        if self.arguments.environment:
            os.environ['environment'] = str(arguments.environment)
        if self.arguments.config_path:
            os.environ['config_path'] = str(arguments.config_path)
        else:
            os.environ['config_path']  = os.path.abspath(f"config.ini")

        self.config = RawConfigParser()
        self.config.read(os.environ['config_path'])    
        self.command = f"python -m pytest"


    def generate_command(self):
        if self.arguments.output_type == "both":  # Run html and allure reporting
            self.command += f" --html={self.html_output} --self-contained-html --alluredir={allure_dir} --clean-alluredir"
        elif self.arguments.output_type == "html":  # Run html reporting
            self.command += f" --html={self.html_output} --self-contained-html"
        elif self.arguments.output_type == "allure":  # Run allure reporting
            self.command += f" --alluredir={allure_dir} --clean-alluredir"
    
        self.command += f" -vs --log-file=\"{self.new_log_path}\" ./testSuites/{self.project}_tests"
        if self.arguments.test:
            if not self.arguments.test.endswith('.py'):
                self.arguments.test += ".py"
            self.command += f"{os.sep}{self.arguments.test} -sv"
        if self.arguments.patterns:
            for pattern in self.arguments.patterns:
                self.command += f" -k {pattern}"


    def setup(self):
        self.new_log_path = self.new_log_path.replace('.log', f"_{self.arguments.environment}.log")
        self.html_output = self.html_output.replace(".html", f"_{self.arguments.environment}.html")
        self.command = self.command.replace(".html", f"_{self.arguments.environment}.html")
        print(f"\nCurrent Dir: {current_dir}")
        print(f"Config Path: {os.environ['config_path']}")
        print(f"root dir: {root_dir}")
        print(f"Log Path: {self.new_log_path}")
        print(f"html Report: {self.html_output}")


    def execute_pytest(self):
        print(f"\n\nCommand:\n{self.command}\n")
        os.system(self.command)  # Run returned command


    def teardown(self):
        os.system(f"allure generate {allure_dir} --clean -o {log_dir}{os.sep}report")
        os.system(f"allure open -p 8675 {log_dir}{os.sep}report")

        pycache_paths = ['__pyache__/', './testSuites/__pycache__/', f"./testSuites/{self.project}_tests/__pycache__/"]
        for path in pycache_paths:
            try:
                shutil.rmtree(path)  # Cleanup pycache
            except Exception as e:
                pass
            

if __name__ == "__main__":
    arguments = get_arguments()
    trigger = Trigger_Functional_Tests(arguments, arguments.project)
    trigger.setup()
    trigger.generate_command()
    trigger.execute_pytest()
    trigger.teardown()
